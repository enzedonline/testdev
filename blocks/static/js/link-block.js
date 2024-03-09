// js/linkBlock.js

class LinkBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        // for each link type, mark the path field as required
        this.meta.link_types.forEach(link_type => {
            this.childBlockDefs.find(obj => obj.name === link_type).meta.required = true;
        })
        // add required mark for link text if url_link_text_required===true
        // required mark conditionally show if link_type==='url_link'
        if (this.meta.url_link_text_required){
            this.childBlockDefs.find(obj => obj.name === 'link_text').meta.required = true;
        }
        // Wagtail block render
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
        this.configureTabs(prefix);
        this.configureLinkTypeChildBlocks();
        // Show panels for initially selected tab, or first tab by default
        this.showPanels(
            this.linkBlock.tabs.buttons.find(button => button.checked) || this.linkBlock.tabs.buttons[0]
        );
    }

    configureTabs(prefix) {
        // the div container that wraps the radio button group
        const tabList = this.linkBlock.structBlock.querySelector(`div#${prefix}-link_type`);

        // Modify link type styles - display as tabs
        tabList.role = "tablist";
        tabList.className = "w-tabs__list w-w-full link-block-tablist";
        // the div container that wraps each radio button
        tabList.querySelectorAll('div').forEach(div => { 
            div.className = "link-block-tab";
        });
        // the radio button labels
        tabList.querySelectorAll('label').forEach(label => { 
            label.className = "w-tabs__tab";
        });

        // Cache link type radio input elements
        this.linkBlock.tabs = { buttons: [...tabList.querySelectorAll('input[type="radio"]')] };

        // Hide redundant field label for 'link type' (but leave readable for screen readers)
        const linkTypeChildBlock = tabList.closest('[data-contentpath="link_type"]');
        linkTypeChildBlock.querySelector("label.w-field__label").classList.add('visually-hidden');

        // Listen for tab click events
        linkTypeChildBlock.addEventListener('click', event => this.handleTabClick(event));
    }

    configureLinkTypeChildBlocks() {
        // associate child blocks with link type button
        // child blocks should be declared with data-link-block-type='XX' where XX is the link_type value
        // the child block element is the div[data-contentpath] parent of the element with data-link-block-type
        // this 'XX' value is copied to the child-block container as data-parent-tab='XX'
        // this attribute is used to show/hide child blocks on tab click
        this.linkBlock.structBlock.querySelectorAll('[data-link-block-type]').forEach(element => {
            const childBlock = element.closest('div[data-contentpath]');
            if (childBlock) {
                childBlock.setAttribute('data-parent-tab', element.dataset.linkBlockType);
            }
        });
        // If optional link, associate not_selected StaticBlock with the 'not selected' tab 
        // null choice radio button has value==='' so data-parent-tab='')
        const noLinkSelectedText = this.linkBlock.structBlock.querySelector('div[data-contentpath="not_selected"]')
        if (noLinkSelectedText) { 
            noLinkSelectedText.setAttribute('data-parent-tab', ''); 
        }
        // cache all tab item child blocks
        this.linkBlock.tabs.tabItems = this.linkBlock.structBlock.querySelectorAll('div[data-parent-tab]');
        // Cache link text child block and required mark
        this.linkBlock.linkTextSection = this.linkBlock.structBlock.querySelector(
            '[data-contentpath="link_text"]'
        );
        this.linkBlock.linkTextRequiredMark = this.linkBlock.linkTextSection.querySelector(
            "label.w-field__label>span.w-required-mark"
        )
    }

    showPanels(activeTab) {
        // When tab with value='XX' clicked, only those child blocks with data-parent-tab='XX' are visible
        this.linkBlock.tabs.tabItems.forEach(div => {
            div.style.display = (div.dataset.parentTab === activeTab.value) ? 'block' : 'none';
        });
        // set the active tab styling
        this.linkBlock.tabs.buttons.forEach(button => {
            button.closest('div.link-block-tab').classList.toggle('active', button === activeTab);
            button.ariaSelected = (button === activeTab) ? "true" : "false";
        });
        // link text visible whenever active tab has a value (link type chosen)
        this.linkBlock.linkTextSection.style.display = (activeTab.value === '') ? "none" : "block";
        // show required mark for link_text if url_link_text_required set in blockDef.meta and URL Link is active tab
        if (this.meta.url_link_text_required){
            this.linkBlock.linkTextRequiredMark.style.display = (
                activeTab.value === 'url_link' && this.meta.url_link_text_required
                ) ? "inline" : "none";
        }
    }

    handleTabClick(event) {
        event.stopPropagation();
        // find associated button - allows click on label and containing tab div
        let clickedTab = event.target.closest('div.link-block-tab');
        if (clickedTab) {
            let radioButton = clickedTab.querySelector('input[type="radio"]');
            if (radioButton) {
                this.showPanels(radioButton);
            }
        }
    }

}

window.telepath.register('blocks.links.LinkBlock', LinkBlockDefinition);
