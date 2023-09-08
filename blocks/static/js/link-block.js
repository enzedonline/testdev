// js/link-block.js

class LinkBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );

        const showPanels = (activeTab) => {
            block.tabs.buttons.forEach(button => {
                button.parentNode.parentNode.classList.toggle('active', button === activeTab);
                button.ariaSelected = (button === activeTab) ? "true" : "false";
            });
            for (let panelKey in block.tabs.panels) {
                let panel = block.tabs.panels[panelKey];
                panel.style.display = (panel.getAttribute('data-value') === activeTab.value) ? 'block' : 'none';
            }
            if (block.linkLabelSection) {
                block.linkLabelSection.style.display = (activeTab.value === '') ? "none" : "block";
                block.blankPanel.style.display = (activeTab.value !== '') ? "none" : "block";
            }
        }

        const setupTabsPanels = () => {

            if (block.blockDef.meta.link_types) {
                // hide any tabs not in link_types
                const tabs = [...block.tabs.buttons];
                for (const tab of tabs) {
                    const tabValue = tab.value;

                    // Check if the button value is not empty and not in the 'link_types' array
                    if (tabValue && !block.blockDef.meta.link_types.includes(tabValue)) {
                        // Set the display attribute to 'none'
                        tab.parentElement.parentElement.style.display = 'none';

                        // Remove the tab from the 'tabs' array
                        const index = block.tabs.buttons.indexOf(tab);
                        if (index !== -1) {
                            block.tabs.buttons.splice(index, 1);
                        }
                    }
                }
            }

            block.tabs.panels.internalPageSection.setAttribute('data-value', 'page');
            block.tabs.panels.anchorTargetSection.setAttribute('data-value', 'page');
            block.tabs.panels.urlLinkSection.setAttribute('data-value', 'url');
            block.tabs.panels.documentSection.setAttribute('data-value', 'document');
        }

        const handleTabClick = (event) => {
            event.stopPropagation();
            let clickedTab = event.target.closest('input[type="radio"]');
            if (clickedTab) {
                showPanels(clickedTab);
            }
        }

        const initialiseBlock = () => {
            block.tabs = { buttons: [] };
            block.tabs.panels = {};

            const structBlock = block.container[0];

            // Cache link type wrapper and buttons
            block.tabs.wrapper = structBlock.querySelector(`#${prefix}-link_type`);
            block.tabs.buttons = [...block.tabs.wrapper.querySelectorAll('input[type="radio"]')];

            // Modify link type styles - display as tabs
            block.tabs.wrapper.role = "tablist";
            block.tabs.wrapper.className = "w-tabs__list w-w-full block-tablist";
            block.tabs.wrapper.querySelectorAll('div').forEach(div => {
                div.className = "block-tab";
            });
            block.tabs.wrapper.querySelectorAll('label').forEach(label => {
                label.className = "w-tabs__tab tab tab-box";
            });

            // Get field sections 
            block.linkTypeSection = block.tabs.wrapper.closest('[data-contentpath="link_type"]');
            block.tabs.panels.internalPageSection = structBlock.querySelector('[data-contentpath="internal_page"]');
            block.tabs.panels.anchorTargetSection = structBlock.querySelector('[data-contentpath="anchor_target"]');
            block.tabs.panels.urlLinkSection = structBlock.querySelector('[data-contentpath="url_link"]');
            block.tabs.panels.documentSection = structBlock.querySelector('[data-contentpath="document"]');

            // Hide redundant 'link type' label, move tabs row up
            block.linkTypeSection.querySelector("label.w-field__label").style.display = 'None';
            block.tabs.wrapper.style.marginTop = '-1em';

            // add required mark to link fields labels
            const requiredMark = document.createElement('span');
            requiredMark.innerText = "*";
            requiredMark.className = "w-required-mark";
            block.tabs.panels.internalPageSection.querySelector("label.w-field__label").appendChild(requiredMark);
            block.tabs.panels.urlLinkSection.querySelector("label.w-field__label").appendChild(requiredMark.cloneNode(true));
            block.tabs.panels.documentSection.querySelector("label.w-field__label").appendChild(requiredMark.cloneNode(true));

            // Relabel 'blank' tab when block link type set to required=False
            const emptyValueInputElement = block.tabs.buttons.find(inputElement => inputElement.value === '');
            if (emptyValueInputElement) {
                const emptyLabel = emptyValueInputElement.closest('label');
                emptyLabel.childNodes.forEach(node => {
                    if (node.nodeType === Node.TEXT_NODE) {
                        node.textContent = block.blockDef.meta.no_link_label;
                    }
                });
                block.linkLabelSection = structBlock.querySelector('[data-contentpath="link_label"]');
                block.blankPanel = document.createElement('p');
                block.blankPanel.textContent = block.blockDef.meta.no_link_description;
                block.blankPanel.className = "w-field__label w-field__wrapper";
                structBlock.appendChild(block.blankPanel);
            }

            // look for link button label setting in parent structblock
            block.link_button_label = document.getElementById(`#${prefix}-link_button_label`)
            if (block.link_button_label) {
                block.link_button_label = block.link_button_label.closest('[data-contentpath="link_button_label"]');
            }

            // Listen for tab click events
            block.linkTypeSection.addEventListener('click', event => handleTabClick(event));

            // Link field section visibility to tabs
            setupTabsPanels();

            // Show panels for initially selected tab, or first tab by default
            showPanels(block.tabs.buttons.find(button => button.checked) || block.tabs.buttons[0]);

        }

        initialiseBlock();
        return block;
    }
}

window.telepath.register('blocks.models.LinkBlock', LinkBlockDefinition);
