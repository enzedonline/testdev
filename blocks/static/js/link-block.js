// js/link-this.linkBlock.js

class LinkBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        this.meta.link_types.forEach(link_type => {
            this.childBlockDefs.find(obj => obj.name === link_type).meta.required = true;
        })
        if (this.meta.url_link_text_required){
            this.childBlockDefs.find(obj => obj.name === 'link_text').meta.required = true;
        }
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );
        // initialise class var with structblock element
        this.linkBlock = { structBlock: block.container[0] };
        this.initialiseBlock(prefix);
        return block;
    };

    initialiseBlock(prefix) {
        this.setupTabs(prefix);
        this.setupLinkTypePanels();
        // Link text section and required mark
        this.linkBlock.linkTextSection = this.linkBlock.structBlock.querySelector('[data-contentpath="link_text"]');
        this.linkBlock.linkTextRequiredMark = this.linkBlock.linkTextSection.querySelector("label.w-field__label>span.w-required-mark")
        // Listen for tab click events
        this.linkBlock.tabs.linkTypeSection.addEventListener('click', event => this.handleTabClick(event));
        // Show panels for initially selected tab, or first tab by default
        this.showPanels(this.linkBlock.tabs.buttons.find(button => button.checked) || this.linkBlock.tabs.buttons[0]);
    }

    setupTabs(prefix) {
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

        // Hide redundant field label for 'link type' (but leave readable fo rcreen readers), move tabs row up
        this.linkBlock.tabs.linkTypeSection = this.linkBlock.tabs.wrapper.closest('[data-contentpath="link_type"]');
        this.linkBlock.tabs.linkTypeSection.querySelector("label.w-field__label").classList.add('visually-hidden');
    }

    setupLinkTypePanels() {
        // associate child blocks with link type button
        // child blocks should be declared with classname="link-block-tab-item link-type-XX" where XX is the link_type value
        // these classes are added to the data-field element - the child block element is the div[data-contentpath] parent of that
        // set data-parent-tab attribute on child block with value XX 
        this.linkBlock.structBlock.querySelectorAll('div.link-block-tab-item').forEach(element => {
            const childBlock = element.closest('div[data-contentpath]');
            if (childBlock) {
                const linkType = Array.from(element.classList).find(
                    classname => classname.includes("link-type-")
                ).replace(/^link-type-/, '');
                childBlock.setAttribute('data-parent-tab', linkType);
            }
        });
        // configure 'not selected' option if applicable
        this.setupNotSelected();
        // cache all tab item child blocks
        this.tabItems = this.linkBlock.structBlock.querySelectorAll('div[data-parent-tab]');
    }

    setupNotSelected() {
        // If link block required=False, relabel the 'not selected' button which has value===''
        // 'Not selected' label is '---------' by default, replace text with this.meta.no_link_label 
        // Associate not_selected StaticBlock with the 'not selected' button which has value===''
        if (!this.meta.required) {
            const noLinkSelectedButton = this.linkBlock.tabs.buttons.find(button => button.value === '');
            // Radio button label text is a text node - replacing text on text node only preserves innerHTML (the <input> element) 
            const emptyLabel = noLinkSelectedButton.closest('label');
            emptyLabel.childNodes.forEach(node => {
                if (node.nodeType === Node.TEXT_NODE) {
                    node.textContent = this.meta.no_link_label;
                    return false; // Exit the loop 
                }
            });
            const noLinkSelectedText = this.linkBlock.structBlock.querySelector('div[data-contentpath="not_selected"]')
            noLinkSelectedText.setAttribute('data-parent-tab', '');
        }
    }

    showPanels(activeTab) {
        // When tab with value='XX' clicked, only those child blocks with data-parent-tab='XX' are visible
        this.tabItems.forEach(div => {
            div.style.display = (div.dataset.parentTab === activeTab.value) ? 'block' : 'none';
        });
        // set the active tab styling
        this.linkBlock.tabs.buttons.forEach(button => {
            button.closest('div.link-block-tab').classList.toggle('active', button === activeTab);
            button.ariaSelected = (button === activeTab) ? "true" : "false";
        });
        // link text visible whenever active tab has a value (link type chosen)
        this.linkBlock.linkTextSection.style.display = (activeTab.value === '') ? "none" : "block";
        // required mark for link tet only shown if url_link_text_required set in blockDef.meta and URL Link is active tab
        if (this.meta.url_link_text_required){
            this.linkBlock.linkTextRequiredMark.style.display = (
                activeTab.value === 'url_link' && this.meta.url_link_text_required
                ) ? "inline" : "none";
        }
    }

    handleTabClick(event) {
        event.stopPropagation();
        let clickedTab = event.target.closest('input[type="radio"]');
        if (clickedTab) {
            this.showPanels(clickedTab);
        }
    }

}

window.telepath.register('blocks.models.LinkBlock', LinkBlockDefinition);
