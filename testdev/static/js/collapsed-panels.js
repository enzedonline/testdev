/**
 * Class to manage the collapsed state of panels in Wagtail's page and snippet edit forms, using localStorage to persist the state across sessions.
 * It listens for changes to the aria-expanded attribute on panel toggle buttons and updates the stored list of collapsed panels accordingly, restoring the state on page load.
 * The class also includes functionality to optionally purge stale data from localStorage based on a configurable maximum age in months, ensuring that old data doesn't accumulate indefinitely.
 * The current object being edited is determined based on the URL path, supporting both page forms and snippet forms, and the relevant panel IDs are extracted from the toggle buttons' aria-controls attributes.
 * @param {Object} options - Configuration options for the WagtailCollapsedPanels instance.
 * @param {number} options.maxAgeMonths - Optional. The maximum age in months for stored collapsed panel data before it is considered stale and purged. Set to 0 or a negative value to disable purging (0 by default).
 * @example
 * const collapsedPanels = new WagtailCollapsedPanels({ maxAgeMonths: 6 });
 */
class WagtailCollapsedPanels {
    // localStorage keys
    static WAGTAIL_OBJECTS_KEY_PREFIX = 'wagtail:objects';
    static PURGE_DATE_KEY = 'wagtail:collapsed-panels-purge-date';
    // css selectors
    static SELECTORS = {
        form: 'form#w-editor-form, form#page-edit-form',
        toggleButton: 'button.w-panel__toggle',
    }
    // Wagtail Events
    static EVENTS = {
        panelToggle: 'wagtail:panel-toggle',
    }
    // regex patterns to extract object information & id's from URL paths, with different patterns for page forms and snippet forms
    static URL_REGEX = {
        page: /\/admin\/([^/]+)\/(\d+)\/edit\/?$/,
        snippet: /\/admin\/snippets\/([^/]+)\/([^/]+)\/edit\/(\d+)\/?$/,
    }

    #editForm = null;       // The open Wagtail admin form
    #objectKey = null;      // The localStorage key to use for the object instance being edited
    #storedData = {};       // Cached localStorage key value
    #maxAgeMonths = 0;      // Max period since a page was accessed before key considered stale - 0 = never stale

    constructor({ maxAgeMonths = 0 } = {}) {
        this.#maxAgeMonths = maxAgeMonths;
        this.#init();
    }

    /**
     * Initializes the WagtailCollapsedPanels instance by determining the current object being edited, loading any stored collapsed panel data from localStorage, restoring the collapsed state of panels in the DOM, and setting up an event listener to listen for changes to panel toggle buttons. Also calls the #purgeStaleData method to clean up old data if necessary.
     * @returns void
     */
    async #init() {
        // Wait for DOMContentLoaded if the document is still loading to ensure that the form and panels are available in the DOM before attempting to access them
        if (document.readyState === "loading") {
            await new Promise(r => document.addEventListener("DOMContentLoaded", r, { once: true }));
        }
        // Identify the form element for the Wagtail edit page - if not found, do not proceed as this script is only relevant on edit forms
        this.#editForm = document.querySelector(WagtailCollapsedPanels.SELECTORS.form);
        if (!this.#editForm) return; // wagtail edit form not found - do not run on listings, reports etc
        const { modelName, objectId } = this.#getCurrentObject() || {};
        if (!modelName || !objectId) return; // could not determine object being edited - do not run

        this.#objectKey = `${WagtailCollapsedPanels.WAGTAIL_OBJECTS_KEY_PREFIX}:${modelName}:${objectId}`;
        queueMicrotask(() => {
            try {
                this.#storedData = JSON.parse(localStorage.getItem(this.#objectKey) ?? '{}');
            } catch (e) {
                console.warn('Failed to parse stored data for collapsed panels:', e);
                this.#storedData = {};
            }
            this.#storedData.collapsedPanels = new Set(Array.isArray(this.#storedData.collapsedPanels) ? this.#storedData.collapsedPanels : []);
            this.#restorePanels();
            this.#editForm.addEventListener(WagtailCollapsedPanels.EVENTS.panelToggle, this.#wagtailPanelToggleHandler.bind(this));
            this.#purgeStaleData();
        });
    }

    /** Cleans up event listeners and instance properties when the instance is no longer needed. 
     * @returns void
     */
    destroy() {
        this.#editForm?.removeEventListener(WagtailCollapsedPanels.EVENTS.panelToggle, this.#wagtailPanelToggleHandler.bind(this));
        this.#editForm = null;
        this.#objectKey = null;
        this.#storedData = {};
    }

    // Handle the toggle button state change - update localStorage based on whether the panel is being collapsed or expanded
    #wagtailPanelToggleHandler(event) {
        const button = event.target;
        if (!(button instanceof Element && button.matches(WagtailCollapsedPanels.SELECTORS.toggleButton))) return;
        const panelId = button.getAttribute('aria-controls');
        if (!panelId) return;
        if (event.detail?.expanded === false) {
            this.#addPanelToStorage(panelId);
        } else {
            this.#deletePanelFromStorage(panelId);
        }
    }

    // Remove a panel ID from the stored list of collapsed panels and update localStorage accordingly
    #deletePanelFromStorage(panelId) {
        this.#storedData.collapsedPanels.delete(panelId);
        this.#saveData();
    }

    // Add a panel ID to the stored list of collapsed panels if it's not already present and update localStorage
    #addPanelToStorage(panelId) {
        this.#storedData.collapsedPanels.add(panelId);
        this.#saveData();
    }

    // Restore the collapsed state of panels based on the stored list of collapsed panel IDs, updating the DOM accordingly and cleaning up any IDs that no longer exist
    #restorePanels() {
        if (this.#storedData.collapsedPanels?.size === 0) return;
        // Gather all toggle buttons in a single DOM query
        const toggleButtons = this.#editForm.querySelectorAll(WagtailCollapsedPanels.SELECTORS.toggleButton);
        // Create a map for quick lookup by aria-controls
        const buttonMap = new Map();
        toggleButtons.forEach(button => {
            const controls = button.getAttribute('aria-controls');
            if (controls) {
                buttonMap.set(controls, button);
            }
        });
        // Process each stored panel ID
        this.#storedData.collapsedPanels.forEach(panelId => {
            const toggleButton = buttonMap.get(panelId);
            if (toggleButton && toggleButton.getAttribute('aria-expanded') === 'true') {
                try {
                    toggleButton.click(); // simulate a click to toggleButton the panel state
                } catch (e) {
                    console.warn(`Failed to toggle panel ${panelId}:`, e);
                    // Remove from storage if toggle fails
                    this.#storedData.collapsedPanels.delete(panelId);
                }
            } else {
                // panel either no longer exists or is collapsed by default - remove from storage to clean up any redundant IDs
                this.#storedData.collapsedPanels.delete(panelId);
            }
        });
        // Updates accessedAt and ensures data structure is correct in case some panels were removed since the last save, and to clean up any invalid panel IDs that no longer exist in the DOM
        this.#saveData();
    }

    // Save the current state of collapsed panels to localStorage, including the list of collapsed panel IDs and the last accessed date. 
    // If there are no collapsed panels, remove the entry from localStorage to avoid storing empty data.
    #saveData() {
        if (this.#storedData.collapsedPanels?.size > 0) {
            const today =
                globalThis.Temporal
                    ? Temporal.Now.plainDateISO().toString()
                    : new Date().toISOString().slice(0, 10);
            try {
                localStorage.setItem(this.#objectKey, JSON.stringify({
                    accessedAt: today,
                    collapsedPanels: Array.from(this.#storedData.collapsedPanels)
                }));
            } catch (e) {
                console.warn('Failed to save collapsed panels data:', e);
            }
        } else {
            try {
                localStorage.removeItem(this.#objectKey);
            } catch (e) {
                console.warn('Failed to remove collapsed panels data:', e);
            }
        }
    }

    // Determine the current object being edited based on the URL path, supporting both page forms and snippet forms, 
    // and return an object containing the model name and object ID
    #getCurrentObject() {
        const path = window.location.pathname;

        // Check for Page URLs: /admin/{model}/{id}/edit/ (model=page)
        let match = path.match(WagtailCollapsedPanels.URL_REGEX.page);
        if (match) {
            const [, modelName, objectId] = match;
            return { modelName, objectId };
        }

        // Check for Snippet URLs: /admin/snippets/{app}/{model}/edit/{id}/
        match = path.match(WagtailCollapsedPanels.URL_REGEX.snippet);
        if (match) {
            const [, app, model, objectId] = match;
            return { modelName: `${app}-${model}`, objectId };
        }

        return null; // no match
    }

    // Purge stale data from localStorage based on the configured maximum age in months, 
    // removing any entries that haven't been accessed within that timeframe and updating the last purge date to prevent excessive purging
    // This method is called on initialization and will only perform purging if maxAgeMonths is set to a positive value and Temporal API is supported
    // It checks the last purge date stored in localStorage and only proceeds if it's been at least a month since the last purge
    // Call from a MicroTask to avoid blocking loading
    #purgeStaleData() {
        if (!this.#maxAgeMonths || typeof Temporal === 'undefined') return; // Purging is disabled if maxAgeMonths is 0 or negative, or Temporal not supported
        try {
            const today = Temporal.Now.plainDateISO();
            const purgeDateStr = localStorage.getItem(WagtailCollapsedPanels.PURGE_DATE_KEY);
            if (purgeDateStr) {
                // Only proceed with purging if it's been at least a month since the last purge
                const purgeDate = Temporal.PlainDate.from(purgeDateStr);
                if (today.since(purgeDate, { largestUnit: "months" }).months < 1) return;
                // Calculate the expiry date based on the current date minus the maximum age in months
                const expiryDate = today.subtract({ months: this.#maxAgeMonths });
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    if (key?.startsWith(WagtailCollapsedPanels.WAGTAIL_OBJECTS_KEY_PREFIX)) {
                        try {
                            const item = JSON.parse(localStorage.getItem(key));
                            const lastAccessed = Temporal.PlainDate.from(item.accessedAt);
                            if (Temporal.PlainDate.compare(lastAccessed, expiryDate) <= 0) {
                                localStorage.removeItem(key);
                            }
                        } catch (e) {
                            // If parsing fails or lastAccessed missing/wrong format, remove the item as it's likely corrupted
                            localStorage.removeItem(key);
                        }
                    }
                }
            }
            localStorage.setItem(WagtailCollapsedPanels.PURGE_DATE_KEY, today.toString());
        } catch (e) {
            console.warn('Failed to purge stale data:', e);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector(WagtailCollapsedPanels.SELECTORS.form)) {
        new WagtailCollapsedPanels({ maxAgeMonths: 6 });
    }
});