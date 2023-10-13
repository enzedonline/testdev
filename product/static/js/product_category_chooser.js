class productCategoryChooser {
    constructor(id) {
        this.chooser = {};
        this.initHTMLElements(id);
        window.p = this.chooser;
    }

    initHTMLElements(id) {
        // Wagtail admin form elements
        this.chooser.wrapper = document.querySelector(`.product-category-chooser-${id}`);
        this.chooser.formSelect = this.chooser.wrapper.querySelector(`#${id}`)
        this.chooser.chosenItem = this.chooser.wrapper.querySelector('.product-category-chooser-chosen');
        this.chooser.openModalBtn = this.chooser.wrapper.querySelector('.open-modal-button');

        // modal form elements
        this.chooser.modal = this.chooser.wrapper.querySelector('.product-category-chooser-modal');
        this.chooser.modalForm = this.chooser.modal.querySelector('.modal-form');
        this.chooser.modalSelect = this.chooser.modal.querySelector('.selection-panel');
        this.chooser.searchInput = this.chooser.modal.querySelector('.modal-search');
        this.chooser.dismissModalBtn = this.chooser.modal.querySelector('.modal-dismiss');
        this.chooser.categoryLists = this.chooser.modal.querySelectorAll('.department');
        this.chooser.listItems = this.chooser.modal.querySelectorAll('.category-label');

        // used to restore last open department after clearing filter
        this.chooser.openDepartment = null;

        // open modal form method
        this.chooser.openModalBtn.addEventListener('click', () => {
            this.chooser.modal.style.display = 'block';
            this.chooser.modalSelect.querySelectorAll('div.department[aria-expanded="true"]').forEach(department => {
                department.setAttribute('aria-expanded', 'false');
            });
            this.filterItems(true);
            this.showActiveCategory();
        });

        this.chooser.modal.addEventListener('click', event => {
            const clickedItem = event.target;
            if (clickedItem.closest('.department-banner')) {
                // expand/collapse department
                const clickedDepartment = clickedItem.closest('.department');
                this.chooser.categoryLists.forEach(department => {
                    if (department == clickedDepartment) {
                        // toggle department value so collapses if currently open
                        department.setAttribute('aria-expanded', department.getAttribute('aria-expanded') !== 'true');
                    } else {
                        // collapse all other departments
                        department.setAttribute('aria-expanded', 'false');
                    }
                });
                if (clickedDepartment.getAttribute('aria-expanded') === 'true') {
                    // only remember clickedDepartment if no search filter
                    if (!this.chooser.searchInput.value) {
                        this.chooser.openDepartment = clickedDepartment;
                    }
                    // ensure expanded department is visible
                    if (this.chooser.modalSelect.clientHeight > clickedDepartment.clientHeight) {
                        const modalSelectBottom = this.chooser.modalSelect.scrollTop + this.chooser.modalSelect.clientHeight;
                        const departmentBottom = clickedDepartment.offsetTop + clickedDepartment.offsetHeight;
                        if (modalSelectBottom <= departmentBottom){
                            clickedDepartment.scrollIntoView({ block: 'end', behavior: 'smooth' });
                        }
                    } else {
                        clickedDepartment.scrollIntoView({ block: 'start', behavior: 'smooth' });
                    }
                } else {
                    this.chooser.openDepartment = null;
                }

            } else if (clickedItem.matches('.category-label')) {
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
            this.filterItems();
        });

    }

    // set selected item on Admin page
    setChosenItem(clickedItem) {
        const categoryID = clickedItem.getAttribute('data-category-id');
        const categoryDepartment = clickedItem.closest('div.department').getAttribute('data-department-name')
        this.chooser.formSelect.value = categoryID;
        this.chooser.chosenItem.innerText = `${categoryDepartment} - ${clickedItem.innerText}`;
        this.chooser.chosenItem.classList.remove('hide');
        this.chooser.openModalBtn.querySelector('.select-category').classList.add('hide')
        this.chooser.openModalBtn.querySelector('.change-category').classList.remove('hide')
    }

    showActiveCategory() {
        this.chooser.modalSelect.querySelectorAll('li.active').forEach(item => {
            item.classList.remove('active');
        })
        const activeCategory = this.chooser.modalSelect.querySelector(`li[data-category-id="${this.chooser.formSelect.value}"]`);
        if (activeCategory) {
            activeCategory.classList.add('active');
            this.chooser.openDepartment = activeCategory.closest('div.department')
            this.chooser.openDepartment.setAttribute('aria-expanded', 'true');
        }
    }

    // filter items
    filterItems(clear = false) {
        if (clear || this.chooser.searchInput.value === '') {
            // clear search value, show all categories, collapse all departments except last active if not null
            this.chooser.searchInput.value = '';
            this.chooser.modalSelect.querySelectorAll('.hide').forEach(item => {
                item.classList.remove('hide');
            });
            this.chooser.categoryLists.forEach(department => {
                department.setAttribute('aria-expanded', 'false');
                if (this.chooser.openDepartment) {
                    this.chooser.openDepartment.setAttribute('aria-expanded', 'true');
                }
            });
        } else {
            // display partial matches, expand all departments with results, hide those without
            this.chooser.modalSelect.querySelectorAll('[aria-expanded="false"').forEach(department => {
                department.setAttribute('aria-expanded', 'true');
            });
            const searchText = this.chooser.searchInput.value.trim().toLowerCase();
            // display or hide modal list item containers where item has partial match with search text
            this.chooser.listItems.forEach(item => {
                // item.style.display = item.textContent.toLowerCase().includes(searchText) ? 'block' : 'none';
                (item.textContent.toLowerCase().includes(searchText)) ? item.classList.remove('hide') : item.classList.add('hide');
            });
            // hide any empty categories
            this.chooser.categoryLists.forEach(department => {
                (department.querySelectorAll('li:not(.hide)').length == 0) ? department.classList.add('hide') : department.classList.remove('hide');
            });
        }
    }

    dismissModal() {
        this.chooser.modal.style.display = 'none';
    }

}
