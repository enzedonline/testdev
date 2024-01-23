class subCategoryChooser {
    constructor(id) {
        this.chooser = {};
        this.initHTMLElements(id);
    }

    initHTMLElements(id) {
        // Wagtail admin form elements
        this.chooser.wrapper = document.querySelector(`[data-subcategory-chooser="${id}"]`);
        this.chooser.formInput = this.chooser.wrapper.querySelector(`#${id}`)
        this.chooser.chosenItem = this.chooser.wrapper.querySelector('.subcategory-chooser-chosen');
        this.chooser.openModalBtn = this.chooser.wrapper.querySelector('.open-modal-button');
        this.chooser.clearChoiceBtn = this.chooser.wrapper.querySelector('.clear-choice-button');

        // modal form elements
        this.chooser.modal = this.chooser.wrapper.querySelector('.subcategory-chooser-modal');
        this.chooser.modalForm = this.chooser.modal.querySelector('.modal-form');
        this.chooser.modalSelect = this.chooser.modal.querySelector('.selection-panel');
        this.chooser.searchInput = this.chooser.modal.querySelector('.modal-search');
        this.chooser.dismissModalBtn = this.chooser.modal.querySelector('.modal-dismiss');
        this.chooser.categoryLists = this.chooser.modal.querySelectorAll('.category');
        this.chooser.listItems = this.chooser.modal.querySelectorAll('.subcategory-label');

        // used to restore last open category after clearing filter
        this.chooser.openCategory = null;

        // open modal form method
        this.chooser.openModalBtn.addEventListener('click', () => {
            this.chooser.modal.style.display = 'block';
            this.chooser.modalSelect.querySelectorAll('div.category[aria-expanded="true"]').forEach(category => {
                category.setAttribute('aria-expanded', 'false');
            });
            // clear any filters
            this.filterItems(true);
            // if pre-chosen subcategory show item and set style
            this.showActiveSubCategory();
        });

        // clear chosen value from panel button
        this.chooser.clearChoiceBtn.addEventListener('click', () => {
            this.clearChosenItem();
        });

        // modal click events
        this.chooser.modal.addEventListener('click', event => {
            const clickedItem = event.target;

            if (clickedItem.closest('.category-banner')) {
                // expand/collapse category
                const clickedCategory = clickedItem.closest('.category');
                this.chooser.categoryLists.forEach(category => {
                    if (category == clickedCategory) {
                        // toggle category value so collapses if currently open
                        category.setAttribute('aria-expanded', category.getAttribute('aria-expanded') !== 'true');
                    } else {
                        // collapse all other categorys
                        category.setAttribute('aria-expanded', 'false');
                    }
                });
                if (clickedCategory.getAttribute('aria-expanded') === 'true') {
                    // only remember clickedCategory if no search filter
                    if (!this.chooser.searchInput.value) {
                        this.chooser.openCategory = clickedCategory;
                    }
                    // ensure expanded category is visible
                    if (this.chooser.modalSelect.clientHeight > clickedCategory.clientHeight) {
                        const modalSelectBottom = this.chooser.modalSelect.scrollTop + this.chooser.modalSelect.clientHeight;
                        const categoryBottom = clickedCategory.offsetTop + clickedCategory.offsetHeight;
                        if (modalSelectBottom <= categoryBottom){
                            clickedCategory.scrollIntoView({ block: 'end', behavior: 'smooth' });
                        }
                    } else {
                        clickedCategory.scrollIntoView({ block: 'start', behavior: 'smooth' });
                    }
                } else {
                    this.chooser.openCategory = null;
                }

            } else if (clickedItem.matches('.subcategory-label')) {
                // category selected - set select value and dismiss modal
                this.setChosenItem(clickedItem);
                this.dismissModal();

            } else if (clickedItem.closest('.modal-search-dismiss')) {
                // clear search filter
                this.filterItems(true);

            } else if (clickedItem.closest('.modal-dismiss') || !this.chooser.modalForm.contains(clickedItem)) {
                // dismiss button or area outside of modal clicked
                this.dismissModal();
            }
        });

        this.chooser.searchInput.addEventListener('input', () => {
            // filter category list
            this.filterItems();
        });

    }

    // set chosen item on Admin page
    setChosenItem(clickedItem) {
        const subcategoryID = clickedItem.getAttribute('data-subcategory-id');
        const category = clickedItem.closest('div.category').getAttribute('data-category-name');
        // set input widget value and display text for chosen item (category - subcategory)
        this.chooser.formInput.value = subcategoryID;
        this.chooser.chosenItem.innerText = `${category} - ${clickedItem.innerText}`;
        // change from 'add new' mode to 'edit/clear/display' mode
        this.chooser.chosenItem.classList.remove('hide');
        this.chooser.openModalBtn.querySelector('.add-subcategory').classList.add('hide');
        this.chooser.openModalBtn.querySelector('.change-subcategory').classList.remove('hide');
        this.chooser.clearChoiceBtn.querySelector('.clear-subcategory').classList.remove('hide');
    }

    clearChosenItem() {
        // clear chosen value and display text
        this.chooser.formInput.value = '';
        this.chooser.chosenItem.innerText = '';
        this.chooser.chosenItem.classList.add('hide');
        this.chooser.openModalBtn.querySelector('.add-subcategory').classList.remove('hide');
        this.chooser.openModalBtn.querySelector('.change-subcategory').classList.add('hide');
        this.chooser.clearChoiceBtn.querySelector('.clear-subcategory').classList.add('hide');
        this.chooser.openCategory = null;
    }

    showActiveSubCategory() {
        // if chosen value already when opening modal, display and highlight item in modal list
        this.chooser.modalSelect.querySelectorAll('li.active').forEach(item => {
            item.classList.remove('active');
        })
        const activeSubCategory = this.chooser.modalSelect.querySelector(`li[data-subcategory-id="${this.chooser.formInput.value}"]`);
        if (activeSubCategory) {
            activeSubCategory.classList.add('active');
            this.chooser.openCategory = activeSubCategory.closest('div.category')
            this.chooser.openCategory.setAttribute('aria-expanded', 'true');
        }
    }

    // filter items
    filterItems(clear = false) {
        if (clear || this.chooser.searchInput.value === '') {
            // clear search value, show all categories, collapse all categorys except last active if not null
            this.chooser.searchInput.value = '';
            this.chooser.modalSelect.querySelectorAll('.hide').forEach(item => {
                item.classList.remove('hide');
            });
            this.chooser.categoryLists.forEach(category => {
                category.setAttribute('aria-expanded', 'false');
                if (this.chooser.openCategory) {
                    this.chooser.openCategory.setAttribute('aria-expanded', 'true');
                }
            });
        } else {
            // display partial matches, expand all categorys with results, hide those without
            this.chooser.modalSelect.querySelectorAll('[aria-expanded="false"').forEach(category => {
                category.setAttribute('aria-expanded', 'true');
            });
            const searchText = this.chooser.searchInput.value.trim().toLowerCase();
            // display or hide modal list item containers where item has partial match with search text
            this.chooser.listItems.forEach(item => {
                // item.style.display = item.textContent.toLowerCase().includes(searchText) ? 'block' : 'none';
                (item.textContent.toLowerCase().includes(searchText)) ? item.classList.remove('hide') : item.classList.add('hide');
            });
            // hide any empty categories
            this.chooser.categoryLists.forEach(category => {
                (category.querySelectorAll('li.subcategory-label:not(.hide)').length == 0) ? category.classList.add('hide') : category.classList.remove('hide');
            });
        }
    }

    dismissModal() {
        this.chooser.modal.style.display = 'none';
    }

}
