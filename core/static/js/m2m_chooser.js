class M2MChooser {
    constructor(id) {
        this.initHTMLElements(id);
        this.showChosenItems()
    }

    initHTMLElements(id) {
        // Wagtail admin form elements
        this.wrapper = document.querySelector(`.m2mchooser-${id}`);
        this.formSelect = this.wrapper.querySelector(`#${id}`)
        this.chosenItems = this.wrapper.querySelector('.m2m-chooser-chosen');
        this.openModalBtn = this.wrapper.querySelector('.m2m-chooser-open-modal-button');
        // modal form elements
        this.modal = this.wrapper.querySelector('.m2m-chooser-modal');
        this.modalForm = this.wrapper.querySelector('.m2m-chooser-modal-form');
        this.modalSelect = this.wrapper.querySelector('.m2m-chooser-modal-select');
        this.searchInput = this.wrapper.querySelector('.m2m-chooser-modal-search');
        this.submitModalBtn = this.wrapper.querySelector('.m2m-chooser-modal-submit');
        this.dismissModalBtn = this.wrapper.querySelector('.m2m-chooser-modal-dismiss');
        this.listItems = null;

        // open modal form method
        this.openModalBtn.addEventListener('click', () => {
            this.updateModalSelectOptions();
            this.modal.style.display = 'block';
            this.listItems = Array.from(this.modalSelect.getElementsByClassName("m2m-chooser-modal-option"));
        });

        // toggle selected modal list items on click
        // items with 'button-secondary' class will be considered unselected
        this.modalSelect.addEventListener('click', event => {
            const clickedItem = event.target;
            if (clickedItem.matches('.m2m-chooser-modal-option')) {
                clickedItem.classList.toggle('button-secondary');
            }
        });

        // modal form submit
        this.submitModalBtn.addEventListener('click', event => {
            event.preventDefault();
            // set selected attributes on Wagtail select option elements
            Array.from(this.modalSelect.getElementsByClassName("m2m-chooser-modal-option")).forEach(modalItem => {
                const originalOption = this.formSelect.querySelector(`option[value="${modalItem.value}"]`);
                if (originalOption && !modalItem.classList.contains("button-secondary")) {
                    originalOption.setAttribute('selected', "");
                } else if (originalOption && modalItem.classList.contains("button-secondary")) {
                    originalOption.removeAttribute('selected');
                }
            });
            // rebuild displayed selected items on underlying admin form
            this.showChosenItems();
            // hide modal
            this.dismissModal();
        });

        this.dismissModalBtn.addEventListener('click', () => {
            // hide modal with no actions
            this.dismissModal();
        });

        // Dismiss modal if clicked outside of form area
        this.modal.addEventListener("click", (event) => {
            if (!this.modalForm.contains(event.target)) {
                this.dismissModal();
            }
        });

        this.searchInput.addEventListener('input', () => {
            const searchText = this.searchInput.value.trim().toLowerCase();
            // display or hide modal list item containers where item has partial match with search text
            this.listItems.forEach(item => {
                item.parentNode.style.display = item.textContent.toLowerCase().includes(searchText) ? 'block' : 'none';
            });
        });

    }

    // display selected options in Wagtail <select> element in style of tagged items 
    showChosenItems() {
        this.chosenItems.innerHTML = "";
        Array.from(this.formSelect.options).forEach(option => {
            if (option.selected) {
                const newItem = document.createElement('li');
                newItem.classList.add("tagit-choice", "tagit-choice-editable", "m2m-chooser-selected-item");
                newItem.innerText = option.text;
                this.chosenItems.appendChild(newItem);
            }
        });
    }

    // fill modal list from Wagtail select element
    updateModalSelectOptions() {
        const fragment = document.createDocumentFragment();
        Array.from(this.formSelect.options).forEach(option => {
            const newOptionContainer = document.createElement('ul');
            newOptionContainer.className = "m2m-chooser-modal-option-container";
            const newListItem = document.createElement('li');
            newListItem.textContent = option.text;
            newListItem.value = option.value;
            newListItem.classList.add("button", "m2m-chooser-modal-option");
            if (!option.selected) {
                newListItem.classList.add("button-secondary");
            }
            newOptionContainer.appendChild(newListItem);
            fragment.appendChild(newOptionContainer);
        });
        this.modalSelect.innerHTML = '';
        this.modalSelect.appendChild(fragment);
    }

    dismissModal() {
        this.modal.style.display = 'none';
        this.modalSelect.innerHTML = "";
    }

}
