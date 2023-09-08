class M2MChooser {
    constructor(id) {
        this.chooser = {};
        this.initHTMLElements(id);
        this.showChosenItems();
    }

    initHTMLElements(id) {
        // Wagtail admin form elements
        this.chooser.wrapper = document.querySelector(`.m2mchooser-${id}`);
        this.chooser.formSelect = this.chooser.wrapper.querySelector(`#${id}`)
        this.chooser.chosenItems = this.chooser.wrapper.querySelector('.m2m-chooser-chosen');
        this.chooser.openModalBtn = this.chooser.wrapper.querySelector('.m2m-chooser-open-modal-button');

        // modal form elements
        this.chooser.modal = this.chooser.wrapper.querySelector('.m2m-chooser-modal');
        this.chooser.modalForm = this.chooser.wrapper.querySelector('.m2m-chooser-modal-form');
        this.chooser.modalSelect = this.chooser.wrapper.querySelector('.m2m-chooser-modal-select');
        this.chooser.searchInput = this.chooser.wrapper.querySelector('.m2m-chooser-modal-search');
        this.chooser.submitModalBtn = this.chooser.wrapper.querySelector('.m2m-chooser-modal-submit');
        this.chooser.dismissModalBtn = this.chooser.wrapper.querySelector('.m2m-chooser-modal-dismiss');
        this.chooser.listItems = null;

        // open modal form method
        this.chooser.openModalBtn.addEventListener('click', () => {
            this.updateModalSelectOptions();
            this.chooser.modal.style.display = 'block';
            this.chooser.listItems = Array.from(this.chooser.modalSelect.getElementsByClassName("m2m-chooser-modal-option"));
        });

        // toggle selected modal list items on click
        // items with 'button-secondary' class will be considered unselected
        this.chooser.modalSelect.addEventListener('click', event => {
            const clickedItem = event.target;
            if (clickedItem.matches('.m2m-chooser-modal-option')) {
                clickedItem.classList.toggle('button-secondary');
            }
        });

        // modal form submit
        this.chooser.submitModalBtn.addEventListener('click', event => {
            event.preventDefault();
            // set selected attributes on Wagtail select option elements
            Array.from(this.chooser.modalSelect.getElementsByClassName("m2m-chooser-modal-option")).forEach(modalItem => {
                const originalOption = this.chooser.formSelect.querySelector(`option[value="${modalItem.value}"]`);
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

        this.chooser.dismissModalBtn.addEventListener('click', () => {
            // hide modal with no actions
            this.dismissModal();
        });

        // Dismiss modal if clicked outside of form area
        this.chooser.modal.addEventListener("click", (event) => {
            if (!this.chooser.modalForm.contains(event.target)) {
                this.dismissModal();
            }
        });

        this.chooser.searchInput.addEventListener('input', () => {
            const searchText = this.chooser.searchInput.value.trim().toLowerCase();
            // display or hide modal list item containers where item has partial match with search text
            this.chooser.listItems.forEach(item => {
                item.parentNode.style.display = item.textContent.toLowerCase().includes(searchText) ? 'block' : 'none';
            });
        });

    }

    // display selected options in Wagtail <select> element in style of tagged items 
    showChosenItems() {
        this.chooser.chosenItems.innerHTML = "";
        Array.from(this.chooser.formSelect.options).forEach(option => {
            if (option.selected) {
                const newItem = document.createElement('li');
                newItem.classList.add("tagit-choice", "tagit-choice-editable", "m2m-chooser-selected-item");
                newItem.innerText = option.text;
                this.chooser.chosenItems.appendChild(newItem);
            }
        });
    }

    // fill modal list from Wagtail select element
    updateModalSelectOptions() {
        const fragment = document.createDocumentFragment();
        Array.from(this.chooser.formSelect.options).forEach(option => {
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
        this.chooser.modalSelect.innerHTML = '';
        this.chooser.modalSelect.appendChild(fragment);
    }

    dismissModal() {
        this.chooser.modal.style.display = 'none';
        this.chooser.modalSelect.innerHTML = "";
    }

}
