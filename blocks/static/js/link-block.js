// js/link-this.linkBlock.js

class LinkBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );
        // initialise class var with structblock element
        this.linkBlock = { structBlock: block.container[0] };
        // arguments paased in LinkBlockAdapter.js_args
        this.settings = block.blockDef.meta
        this.initialiseBlock(prefix);
        return block;
    };

    initialiseBlock(prefix) {

        // Cache link type wrapper and buttons
        this.linkBlock.tabs = { buttons: [], panels: {} };
        this.linkBlock.tabs.wrapper = this.linkBlock.structBlock.querySelector(`div#${prefix}-link_type`);
        this.linkBlock.tabs.buttons = [...this.linkBlock.tabs.wrapper.querySelectorAll('input[type="radio"]')];

        // Modify link type styles - display as tabs
        this.linkBlock.tabs.wrapper.role = "tablist";
        this.linkBlock.tabs.wrapper.className = "w-tabs__list w-w-full link-block-tablist";
        this.linkBlock.tabs.wrapper.querySelectorAll('div').forEach(div => {
            div.className = "link-block-tab";
        });
        this.linkBlock.tabs.wrapper.querySelectorAll('label').forEach(label => {
            label.className = "w-tabs__tab";
        });

        // Get field sections 
        this.linkBlock.tabs.linkTypeSection = this.linkBlock.tabs.wrapper.closest('[data-contentpath="link_type"]');
        this.linkBlock.tabs.panels.internalPageSection = this.linkBlock.structBlock.querySelector('[data-contentpath="internal_page"]');
        this.linkBlock.tabs.panels.anchorTargetSection = this.linkBlock.structBlock.querySelector('[data-contentpath="anchor_target"]');
        this.linkBlock.tabs.panels.urlLinkSection = this.linkBlock.structBlock.querySelector('[data-contentpath="url_link"]');
        this.linkBlock.tabs.panels.documentSection = this.linkBlock.structBlock.querySelector('[data-contentpath="document"]');
        this.linkBlock.tabs.panels.linkTextSection = this.linkBlock.structBlock.querySelector('[data-contentpath="link_text"]');

        // Hide redundant field label for 'link type', move tabs row up
        this.linkBlock.tabs.linkTypeSection.querySelector("label.w-field__label").style.display = 'None';
        this.linkBlock.tabs.wrapper.style.marginTop = '-1em';

        // Configure 'no selection' tab and panel, relate field section visibility to tabs
        this.setupTabsPanels();

        // Show panels for initially selected tab, or first tab by default
        this.showPanels(this.linkBlock.tabs.buttons.find(button => button.checked) || this.linkBlock.tabs.buttons[0]);

    }

    setupTabsPanels () {
        // Initialise tabs and associate panels with respective tabs
        const tabs = [...this.linkBlock.tabs.buttons];

        // hide any tabs not in block settings link_types, configure 'not selected' tab and panel
        for (const tab of tabs) {
            const tabValue = tab.value;
            if (tabValue) { 
                // Check if the button value is not empty and not in the 'link_types' array
                if (!this.settings.link_types.includes(tabValue)) {
                    // Set the display attribute to 'none'
                    tab.parentElement.parentElement.style.display = 'none';

                    // Remove the tab from the 'tabs' array
                    const index = this.linkBlock.tabs.buttons.indexOf(tab);
                    if (index !== -1) {
                        this.linkBlock.tabs.buttons.splice(index, 1);
                    }
                }                        
            } else { // radio button with no value is the 'not selected' button
                const emptyLabel = tab.closest('label');
                // 'Not selected' label is '---------' by default, replace text with no_link_label from this.linkBlock settings
                // Radio button label text is a text node - replacing text on text node only preserves innerHTML (the <input> element) 
                emptyLabel.childNodes.forEach(node => {
                    if (node.nodeType === Node.TEXT_NODE) {
                        node.textContent = this.settings.no_link_label;
                        return false; // Exit the loop 
                    }
                });
                // Create a panel to display when no link has been chosen, use no_link_description from block settings
                this.linkBlock.tabs.panels.notSelectedSection = document.createElement('p');
                this.linkBlock.tabs.panels.notSelectedSection.textContent = this.settings.no_link_description;
                this.linkBlock.tabs.panels.notSelectedSection.className = "w-field__label w-field__wrapper";
                this.linkBlock.structBlock.appendChild(this.linkBlock.tabs.panels.notSelectedSection);
            }
        };

        // add required mark to link fields that are required for each link type
        const requiredMark = document.createElement('span');
        requiredMark.innerText = "*";
        requiredMark.className = "w-required-mark";
        this.linkBlock.tabs.panels.internalPageSection.querySelector("label.w-field__label").appendChild(requiredMark);
        this.linkBlock.tabs.panels.urlLinkSection.querySelector("label.w-field__label").appendChild(requiredMark.cloneNode(true));
        this.linkBlock.tabs.panels.documentSection.querySelector("label.w-field__label").appendChild(requiredMark.cloneNode(true));
        // required mark for link tet only shown if set in settings and URL Link is active tab
        // for page and document links, link text defaults to object title
        this.linkBlock.tabs.linkTextRequiredMark = requiredMark.cloneNode(true)
        this.linkBlock.tabs.panels.linkTextSection.querySelector("label.w-field__label").appendChild(this.linkBlock.tabs.linkTextRequiredMark);

        // link section value to radio button (tab) value - used to show/hide on tab click
        this.linkBlock.tabs.panels.internalPageSection.setAttribute('data-value', 'page');
        this.linkBlock.tabs.panels.anchorTargetSection.setAttribute('data-value', 'page');
        this.linkBlock.tabs.panels.urlLinkSection.setAttribute('data-value', 'url');
        this.linkBlock.tabs.panels.documentSection.setAttribute('data-value', 'document');

        // Listen for tab click events
        this.linkBlock.tabs.linkTypeSection.addEventListener('click', event => this.handleTabClick(event));

    }

    showPanels(activeTab) {
        // set the active tab styling
        this.linkBlock.tabs.buttons.forEach(button => {
            button.closest('div.link-block-tab').classList.toggle('active', button === activeTab);
            button.ariaSelected = (button === activeTab) ? "true" : "false";
        });
        // hide panels not related to the active tab
        for (let panelKey in this.linkBlock.tabs.panels) { 
            let panel = this.linkBlock.tabs.panels[panelKey];
            panel.style.display = (panel.getAttribute('data-value') === activeTab.value) ? 'block' : 'none';
        };
        this.linkBlock.tabs.linkTextRequiredMark.style.display = (activeTab.value === 'url' && this.settings.url_link_text_required)  ? "inline" : "none";
        // link text visible whenever active tab has a value (link type chosen)
        this.linkBlock.tabs.panels.linkTextSection.style.display = (activeTab.value === '') ? "none" : "block";
        // 'not selected' panel visible whenever active tab has no value (no link type chosen)
        this.linkBlock.tabs.panels.notSelectedSection.style.display = (activeTab.value !== '') ? "none" : "block";
    }

    handleTabClick (event) {
        event.stopPropagation();
        let clickedTab = event.target.closest('input[type="radio"]');
        if (clickedTab) {
            this.showPanels(clickedTab);
        }
    }

}

window.telepath.register('blocks.models.LinkBlock', LinkBlockDefinition);
