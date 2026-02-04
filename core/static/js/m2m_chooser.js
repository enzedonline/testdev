class M2MChooser {
    constructor(id) {
        this.initHTMLElements(id);
        this.addEventListeners();
        this.getSelectedItems(); // get selected items from select element
        this.showChosenItems(); // display chosen items list on admin form
    }

    initHTMLElements(id) {
        // Class variables ========================================================================
        this.chooser = {};
        this.chooser.selectedItems = {}; // stores currently selected items in format {'value': 'label'}

        // Wagtail admin form elements ============================================================
        this.chooser.wrapper = document.querySelector(`div.m2mchooser-${id}`);
        this.chooser.formSelect = this.chooser.wrapper.querySelector(`select#${id}`)
        this.chooser.chosenItemsList = this.chooser.wrapper.querySelector('ul.m2m-chooser-chosen');
        this.chooser.openModalBtn = this.chooser.wrapper.querySelector('button[data-button-role="open-modal"]');
        this.chooser.clearChosenBtn = this.chooser.wrapper.querySelector('button[data-button-role="clear-chosen"]');

        // Build a map of option value -> option element for fast lookup =======================
        this.chooser.optionsMap = new Map();
        Array.from(this.chooser.formSelect.options).forEach(opt => this.chooser.optionsMap.set(opt.value, opt));

        // modal form elements ====================================================================
        this.chooser.modal = this.chooser.wrapper.querySelector('div.m2m-chooser-modal');
        this.chooser.modalForm = this.chooser.modal.querySelector('div.modal-form');
        this.chooser.searchInput = this.chooser.modal.querySelector('input.modal-search');
        this.chooser.noResults = this.chooser.modal.querySelector('div.no-results-text');
        this.chooser.listItems = this.chooser.modal.querySelectorAll("li.modal-select-item");

        // chosen item template used to add items to chosenItemsList ==============================
        this.chooser.chosenItemTemplate = document.createElement('li');
        this.chooser.chosenItemTemplate.classList.add('tagit-choice', 'tagit-choice-editable');
        this.chooser.chosenItemTemplate.innerHTML = `
            <span></span>
            <a class="clear-choice-button" role="button" title="Remove">
                <svg class="icon icon-circle-mark">
                    <use href="#icon-circle-xmark"></use>
                </svg>
            </a>
        `;
    }

    addEventListeners() {

    // admin form event listeners ===========================================================================
        // Debounce helper used for search input
        this._filterTimeout = null;

        // clear all chosen values ================================================================
        this.chooser.clearChosenBtn.addEventListener('click', () => {
            this.handleClearChosenItemsClick();
        })

        // remove item from chosen list if clear choice button was clicked ========================
        this.chooser.chosenItemsList.addEventListener('click', (event) => {
            const target = event.target.closest('a.clear-choice-button')
            if (target) {
                this.handleClearChoiceClick(target);
            }
        });

        // open modal form method =================================================================
        this.chooser.openModalBtn.addEventListener('click', () => {
            this.showSelectedModalItems();
            if (this.chooser.searchInput.value) { // clear search form
                this.clearFilter();
            }
            this.chooser.modal.style.display = 'block';
        });

    // modal event listeners ================================================================================

        //  click events ==========================================================================
        this.chooser.modal.addEventListener('click', event => {
            const clickedListItem = event.target.closest('li.modal-select-item');
            const submitBtn = event.target.closest('button[data-button-role="submit-modal"]');
            const clearFilterBtn = event.target.closest('a[data-button-role="clear-filter"]');
            const cancelBtn = event.target.closest('button[data-button-role="cancel-modal"]');

            // toggle modal list items selected status on click ==============================
            if (clickedListItem) {
                const selected = clickedListItem.dataset.selected === 'true' ? 'false' : 'true';
                clickedListItem.dataset.selected = selected;
                clickedListItem.classList.toggle('button-secondary');
            }
            // modal submit ==================================================================
            // get selected values from modal form, rebuild displayed selected items on underlying admin form, hide modal
            else if (submitBtn) {
                event.preventDefault();
                this.getSelectedModalItems();
                this.setChosenItems();
                this.dismissModal();
            }
            // clear search filter ===========================================================
            else if (clearFilterBtn) {
                this.clearFilter();
                this.chooser.searchInput.focus();
            }
            // dismiss button or area outside of modal clicked ===============================
            else if (cancelBtn || !this.chooser.modalForm.contains(event.target)) {
                this.dismissModal();
            }
        });

        // search form input (debounced) =========================================================
        this.chooser.searchInput.addEventListener('input', () => {
            clearTimeout(this._filterTimeout);
            this._filterTimeout = setTimeout(() => this.filterItems(), 150);
        });

    }

    // load selected values and labels from <select> element into selectedItems dictionary ==================
    getSelectedItems() {
        this.chooser.selectedItems = {};
        Array.from(this.chooser.formSelect.selectedOptions).forEach(option => {
            this.chooser.selectedItems[option.value] = option.textContent;
        });
    }

    // populate admin form chosen items list ================================================================
    // get selected options from selectedItems dictionary and display in style of tagged items 
    showChosenItems() {
        this.chooser.chosenItemsList.innerHTML = "";
        const fragment = document.createDocumentFragment();
        Object.keys(this.chooser.selectedItems).forEach(key => {
            const value = this.chooser.selectedItems[key];
            const li = this.chooser.chosenItemTemplate.cloneNode(true);
            li.setAttribute('data-chosen-value', key);
            li.querySelector('span').textContent = value;
            fragment.appendChild(li);
        });
        this.chooser.chosenItemsList.appendChild(fragment);
    }

    // update admin form <select> element from selectedItems dictionary and update chosen item display ======
    // used after modal form submit
    setChosenItems() {
        this.chooser.formSelect.selectedIndex = -1;
        for (const value of Object.keys(this.chooser.selectedItems)) {
            const option = this.chooser.optionsMap.get(value);
            if (option) option.selected = true;
        }
        this.showChosenItems();
    }

    // set selected style attributes on modal list items if they appear in selectedItems dictionary =========
    // used when showing modal to match selected items with chosen items
    showSelectedModalItems() {
        this.chooser.listItems.forEach(li => {
            const key = li.getAttribute('value');
            const shouldSelect = Object.prototype.hasOwnProperty.call(this.chooser.selectedItems, key);
            if (li.dataset.selected !== String(shouldSelect)) {
                li.dataset.selected = String(shouldSelect);
                li.classList.toggle('button-secondary', !shouldSelect);
            }
        });
    }

    // update selectedItems dictionary from modal form selected values =======================================
    getSelectedModalItems() {
        this.chooser.selectedItems = {};
        this.chooser.listItems.forEach(li => {
            if (li.dataset.selected === 'true') {
                const key = li.getAttribute('value');
                const value = li.textContent.trim();
                this.chooser.selectedItems[key] = value;
            }
        });
    }

    // clear all selected items from admin form button ======================================================
    handleClearChoiceClick(button) {
        const chosenListItem = button.closest('li');
        const chosenListItemValue = chosenListItem.getAttribute('data-chosen-value');
        delete this.chooser.selectedItems[chosenListItemValue]
        // use cached map to find the corresponding option
        const opt = this.chooser.optionsMap.get(chosenListItemValue);
        if (opt) opt.selected = false;
        chosenListItem.remove();
    }

    // handle chosen item delete button =====================================================================
    // remove item from chosen list in admin interface & selectedItems, deselect from <select> form element
    handleClearChoiceClick(button) {
        const chosenListItem = button.closest('li');
        const chosenListItemValue = chosenListItem.getAttribute('data-chosen-value');
        delete this.chooser.selectedItems[chosenListItemValue]
        // find the item in the admin form <select> element
        const selectItem = Array.from(
            this.chooser.formSelect.selectedOptions
            ).find(
                option => option.value === chosenListItemValue
            );
        if (selectItem) { 
            selectItem.selected = false 
        };
        chosenListItem.remove();
    }

    // handle search input - case insensitive partial match on list items inner text ========================
    filterItems() {
        const searchText = this.chooser.searchInput.value.trim().toLowerCase();
        if (this.chooser.searchInput.value === '') {
            this.chooser.listItems.forEach(listItem => {
                listItem.classList.remove('hide');
            });
            this.chooser.noResults.classList.add('hide');
        } else {
            // display or hide modal list item containers where item has partial match with search text
            let matchExists = false;
            this.chooser.listItems.forEach(listItem => {
                let match = listItem.textContent.toLowerCase().includes(searchText)
                listItem.classList.toggle('hide', !match);
                matchExists = (matchExists || match);
            });
            // show 'no results' text if no matching records were found
            this.chooser.noResults.classList.toggle('hide', matchExists);
        }
    }

    // clear search input & restore list items display to block
    clearFilter() {
        this.chooser.searchInput.value = '';
        this.filterItems();
    }

    // hide modal
    dismissModal() {
        this.chooser.modal.style.display = 'none';
    }

}
