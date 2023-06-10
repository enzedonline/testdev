const initialiseM2MFieldPanel = (m2m_field_panel) => {
    const originalSelect = document.getElementById(m2m_field_panel.field_id);
    const modal = document.getElementById(`m2m-chooser-modal-${m2m_field_panel.field_id}`);
    const openModalBtn = document.getElementById(`m2m-chooser-open-modal-button-${m2m_field_panel.field_id}`);
    const modalSelect = document.getElementById(`m2m-chooser-modal-select-${m2m_field_panel.field_id}`);
    const chosenItems = document.getElementById(`m2m-chooser-chosen-${m2m_field_panel.field_id}`);
    const searchInput = document.getElementById(`m2m-chooser-modal-search-${m2m_field_panel.field_id}`);
    const submitModalBtn = document.getElementById(`m2m-chooser-modal-submit-${m2m_field_panel.field_id}`);
    const dismissModalBtn = document.getElementById(`m2m-chooser-modal-dismiss-${m2m_field_panel.field_id}`);
    let listItems = null;

    // display selected options in Wagtail select element in tagged items style
    const showChosenItems = () => {
        chosenItems.innerHTML = "";
        Array.from(originalSelect.options).forEach(option => {
            if (option.selected) {
                const newItem = document.createElement('li');
                newItem.classList.add("tagit-choice", "tagit-choice-editable", "m2m-chooser-selected-item");
                newItem.innerText = option.text;
                chosenItems.appendChild(newItem);
            }
        });
    };
    showChosenItems();

    // fill modal list from Wagtail select element
    const updateModalSelectOptions = () => {
        const fragment = document.createDocumentFragment();
        Array.from(originalSelect.options).forEach(option => {
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
        modalSelect.innerHTML = '';
        modalSelect.appendChild(fragment);
    };

    // open modal form method
    openModalBtn.addEventListener('click', () => {
        updateModalSelectOptions();
        modal.style.display = 'block';
        listItems = Array.from(modalSelect.getElementsByClassName("m2m-chooser-modal-option"));
    });

    // toggle selected modal list items on click
    // items with 'button-secondary' class will be considered unselected
    modalSelect.addEventListener('click', event => {
        const clickedItem = event.target;
        if (clickedItem.matches('.m2m-chooser-modal-option')) {
            clickedItem.classList.toggle('button-secondary');
        }
    });

    // modal form submit
    submitModalBtn.addEventListener('click', event => {
        event.preventDefault();
        // set selected attributes on Wagtail select option elements
        Array.from(modalSelect.getElementsByClassName("m2m-chooser-modal-option")).forEach(option => {
            const newOption = originalSelect.querySelector(`option[value="${option.value}"]`);
            if (newOption && !option.classList.contains("button-secondary")) {
                newOption.setAttribute('selected', "");
            } else if (newOption && option.classList.contains("button-secondary")) {
                newOption.removeAttribute('selected');
            }
        });
        // rebuild displayed selected items on underlying admin form
        showChosenItems();
        // hide modal
        modal.style.display = 'none';
    });

    dismissModalBtn.addEventListener('click', () => {
        // hide modal with no actions
        modal.style.display = 'none';
        modalSelect.innerHTML = "";
    });

    searchInput.addEventListener('input', () => {
        const searchText = searchInput.value.trim().toLowerCase();
        // display or hide modal list item containers where item has partial match with search text
        listItems.forEach(item => {
            item.parentNode.style.display = item.textContent.toLowerCase().includes(searchText) ? 'block' : 'none';
        });
    });
};
