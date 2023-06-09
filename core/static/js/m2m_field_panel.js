const initialiseM2MFieldPanel = (m2m_field_panel) => {

	// Retrieve the original select element and modal elements
	const originalSelect = document.getElementById(m2m_field_panel.field_id);
	const modal = document.getElementById(`m2m-chooser-modal-${m2m_field_panel.field_id}`);
	const openModalBtn = document.getElementById(`m2m-chooser-open-modal-button-${m2m_field_panel.field_id}`);
	const modalSelect = document.getElementById(`m2m-chooser-modal-select-${m2m_field_panel.field_id}`);
	const chosenItems = document.getElementById(`m2m-chooser-chosen-${m2m_field_panel.field_id}`);
	const searchInput = document.getElementById(`m2m-chooser-modal-search-${m2m_field_panel.field_id}`);
	const submitModalBtn = document.getElementById(`m2m-chooser-modal-submit-${m2m_field_panel.field_id}`);
	const dismissModalBtn = document.getElementById(`m2m-chooser-modal-dismiss-${m2m_field_panel.field_id}`);
	let listItems = null;


	const showChosenItems = () => {
		chosenItems.innerHTML = "";
		Array.from(originalSelect.options).forEach(option => {
			if (option.selected) {
				const newItem = document.createElement('li');
				newItem.classList.add("tagit-choice", "tagit-choice-editable", "m2m-chooser-selected-item");
				newItem.innerText = option.text;
				chosenItems.appendChild(newItem);
			};
		});
	}
	showChosenItems();

	// Add event listener to open the modal form
	openModalBtn.addEventListener('click', function () {
		// Populate the modal select element with options from the original select element
		modalSelect.innerHTML = ""
		Array.from(originalSelect.options).forEach(option => {
			const newOptionContainer = document.createElement('UL');
			newOptionContainer.className = "m2m-chooser-modal-option-container"
			const newListItem = document.createElement('LI');
			newListItem.innerText = option.text;
			newListItem.value = option.value;
			newListItem.classList.add("button", "m2m-chooser-modal-option");
			if (!option.selected) {
				newListItem.classList.add("button-secondary");
			};
			newOptionContainer.appendChild(newListItem);
			modalSelect.appendChild(newOptionContainer);
		});
		modalSelect.addEventListener('click', event => {
			const clickedItem = event.target;
			if (clickedItem.matches('.m2m-chooser-modal-option')) {
				clickedItem.classList.toggle('button-secondary');
			}
		});		
		modal.style.display = 'block';
		listItems = Array.from(modalSelect.children);
	});

	// Handle form submission
	submitModalBtn.addEventListener('click', function (event) {
		event.preventDefault();

		// Clear existing options in the original select element
		originalSelect.innerHTML = '';

		// Update the original select element with the new options from the modal select
		Array.from(modalSelect.getElementsByClassName("m2m-chooser-modal-option")).forEach(option => {
			const newOption = document.createElement('option');
			newOption.value = option.value;
			newOption.textContent = option.textContent;
			if (!option.classList.contains("button-secondary")) {
				newOption.setAttribute('selected', "")
			}
			originalSelect.appendChild(newOption);
		});
		showChosenItems();

		// Close the modal form
		modal.style.display = 'none';
	});

	dismissModalBtn.addEventListener('click', function (event) {
		modal.style.display = 'none';
		modalSelect.innerHTML = ""
	});

	searchInput.addEventListener('input', () => {
		const searchText = searchInput.value.trim().toLowerCase();
		listItems.forEach(item => {
			const itemText = item.textContent.toLowerCase();
			item.style.display = itemText.includes(searchText) ? 'block' : 'none';
		});
	});
}
