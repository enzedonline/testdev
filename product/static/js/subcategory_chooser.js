// static/js/subcategory_chooser.js

class subcategoryChooser {
    constructor(id) {
        this.chooser = {};
        this.initHTMLElements(id);
    }

    // set up class variables, add event listeners ==========================================================
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
        this.chooser.categories = this.chooser.modal.querySelectorAll('.category');
        this.chooser.subcategories = this.chooser.modal.querySelectorAll('.subcategory-label');

        // open modal form ========================================================================
        this.chooser.openModalBtn.addEventListener('click', () => {
            // used to restore last open category after clearing filter
            this.chooser.openCategory = null;
            // clear any filters and collapse any open categories
            this.clearFilter();
            // show modal
            this.chooser.modal.style.display = 'block';
            // if pre-chosen subcategory show item and set style
            this.showActiveSubCategory();
        });

        // clear chosen value =====================================================================
        this.chooser.clearChoiceBtn.addEventListener('click', () => {
            this.clearChosenItem();
        });

        // modal click events =====================================================================
        this.chooser.modal.addEventListener('click', event => {
            const clickedItem = event.target;

            // expand/collapse category =================================================
            if (clickedItem.closest('.category-banner')) {
                this.handleCategoryClick(clickedItem.closest('.category'));
            }
            // subcategory clicked - set select value and dismiss modal =================
            else if (clickedItem.matches('.subcategory-label')) {
                this.setChosenItem(clickedItem);
                this.dismissModal();
            }
            // clear search filter ======================================================
            else if (clickedItem.closest('.modal-search-dismiss')) {
                this.clearFilter();
            }
            // dismiss button or area outside of modal clicked ==========================
            else if (clickedItem.closest('.modal-dismiss') || !this.chooser.modalForm.contains(clickedItem)) {
                this.dismissModal();
            }
        });

        // filter category list or clear if no input value ========================================
        this.chooser.searchInput.addEventListener('input', () => {
            this.filterItems();
        });

    }

    // expand/collapse category, scroll subcategories into view if expanded =================================
    handleCategoryClick(clickedCategory) {
        this.chooser.categories.forEach(category => {
            // toggle clicked category value so collapses if currently open, collapse all other categories
            if (category == clickedCategory) {
                category.setAttribute('aria-expanded', category.getAttribute('aria-expanded') !== 'true');
            } else {
                category.setAttribute('aria-expanded', 'false');
            }
        });
        if (clickedCategory.getAttribute('aria-expanded') === 'true') {
            // only remember clickedCategory if no search filter
            if (!this.chooser.searchInput.value) {
                this.chooser.openCategory = clickedCategory;
            }
            // ensure expanded category is scrolled into view fully so subcategories are visible
            if (this.chooser.modalSelect.clientHeight > clickedCategory.clientHeight) {
                const modalSelectBottom = this.chooser.modalSelect.scrollTop + this.chooser.modalSelect.clientHeight;
                const categoryBottom = clickedCategory.offsetTop + clickedCategory.offsetHeight;
                if (modalSelectBottom <= categoryBottom) {
                    clickedCategory.scrollIntoView({ block: 'end', behavior: 'smooth' });
                }
            } else {
                clickedCategory.scrollIntoView({ block: 'start', behavior: 'smooth' });
            }
        } else {
            // there are no open categories
            this.chooser.openCategory = null;
        }
    }

    // set chosen item on Admin page ========================================================================
    setChosenItem(clickedItem) {
        const subcategoryID = clickedItem.getAttribute('data-subcategory-id');
        const category = clickedItem.closest('div.category').getAttribute('data-category-name');
        // set input widget value and display text for chosen item (category - subcategory)
        this.chooser.formInput.value = subcategoryID;
        this.chooser.chosenItem.innerText = `${category} - ${clickedItem.innerText}`;
        // admin interface - change from 'add new' mode to 'edit/clear/display' mode
        this.chooser.chosenItem.classList.remove('hide');
        this.chooser.openModalBtn.querySelector('.add-subcategory').classList.add('hide');
        this.chooser.openModalBtn.querySelector('.change-subcategory').classList.remove('hide');
        this.chooser.clearChoiceBtn.querySelector('.clear-subcategory').classList.remove('hide');
    }

    // clear chosen value and display text, revert admin panel to 'add new' mode ============================
    clearChosenItem() {
        this.chooser.formInput.value = '';
        this.chooser.chosenItem.innerText = '';
        this.chooser.chosenItem.classList.add('hide');
        this.chooser.openModalBtn.querySelector('.add-subcategory').classList.remove('hide');
        this.chooser.openModalBtn.querySelector('.change-subcategory').classList.add('hide');
        this.chooser.clearChoiceBtn.querySelector('.clear-subcategory').classList.add('hide');
        this.chooser.openCategory = null;
    }

    // if chosen value already when opening modal, display and highlight item in modal list =================
    showActiveSubCategory() {
        // remove any previous 'active' subcategories in case modal has been opened previously
        this.chooser.modalSelect.querySelectorAll('li.active').forEach(item => {
            item.classList.remove('active');
        })
        // find the subcategory element from the form field input value
        const activeSubCategory = this.chooser.modalSelect.querySelector(
            `li[data-subcategory-id="${this.chooser.formInput.value}"]`
        );
        if (activeSubCategory) {
            // highlight chosen item
            activeSubCategory.classList.add('active');
            // expand parent category
            this.chooser.openCategory = activeSubCategory.closest('div.category')
            this.chooser.openCategory.setAttribute('aria-expanded', 'true');
            // ensure chosen item visible on screen - modal must not be hidden for this
            activeSubCategory.scrollIntoView({ block: 'end' });
        }
    }

    // clear search value ===================================================================================
    clearFilter() {
        this.chooser.searchInput.value = '';
        // unhide all categories and subcategories
        this.chooser.modalSelect.querySelectorAll('.hide').forEach(item => {
            item.classList.remove('hide');
        });
        // show all categories, collapse all categorys except last active if not null
        this.chooser.categories.forEach(category => {
            // collapse all category banners
            category.setAttribute('aria-expanded', 'false');
            // if a category was expanded before search, restore open and scroll to view
            if (this.chooser.openCategory) {
                this.chooser.openCategory.setAttribute('aria-expanded', 'true');
                this.chooser.openCategory.scrollIntoView({ block: 'end' });
            }
        });
    }

    // filter items =========================================================================================
    filterItems() {
        if (this.chooser.searchInput.value === '') {
            this.clearFilter();
        } else {
            // display partial matches, expand all categorys with results, hide those without
            this.chooser.modalSelect.querySelectorAll('[aria-expanded="false"').forEach(category => {
                category.setAttribute('aria-expanded', 'true');
            });
            const searchText = this.chooser.searchInput.value.trim().toLowerCase();
            // display or hide modal list item containers where item has partial match with search text
            this.chooser.subcategories.forEach(subcategory => {
                (subcategory.textContent.toLowerCase().includes(searchText)) 
                    ? subcategory.classList.remove('hide') 
                    : subcategory.classList.add('hide');
            });
            // hide any empty categories
            this.chooser.categories.forEach(category => {
                (category.querySelectorAll('li.subcategory-label:not(.hide)').length == 0) 
                    ? category.classList.add('hide') 
                    : category.classList.remove('hide');
            });
        }
    }

    // hide modal - close button clicked, or click was outside of modal body ================================
    dismissModal() {
        this.chooser.modal.style.display = 'none';
    }

}
