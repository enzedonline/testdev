// js/seo-image-chooser-block.js

class CSVTableBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {

    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );
        window.test = this;
        this.csvTableBlock = { structBlock: block.container[0] };
        this.initialiseBlock(prefix);
        return block;
    }

    initialiseBlock(prefix) {
        this.renderTimeout = null;
        this.renderField = this.csvTableBlock.structBlock.querySelector(`#${prefix}-html`)
        this.renderSuccess = this.csvTableBlock.structBlock.querySelector(`#${prefix}-rendered`)
        this.inputElements = {
            'data': this.csvTableBlock.structBlock.querySelector(`#${prefix}-data`),
            'precision': this.csvTableBlock.structBlock.querySelector(`#${prefix}-precision`),
            'column_headers': this.csvTableBlock.structBlock.querySelector(`#${prefix}-column_headers`),
            'row_headers': this.csvTableBlock.structBlock.querySelector(`#${prefix}-row_headers`),
            'compact': this.csvTableBlock.structBlock.querySelector(`#${prefix}-compact`)
        };
        this.dataErrorElement = this.csvTableBlock.structBlock.querySelector('div[data-contentpath="data"]').querySelector('div.w-field__errors')
        Object.values(this.inputElements).forEach(element => {
            if (element) {
                element.addEventListener('input', () => {
                    // Clear any existing timeout
                    clearTimeout(this.renderTimeout);

                    // Set a new timeout to call renderTable after 2 seconds
                    this.renderTimeout = setTimeout(() => {
                        this.renderTable();
                    }, 1000);
                });
            }
        });
        this.renderingMessageDiv = this.csvTableBlock.structBlock.appendChild(document.createElement('div'));
        this.renderingMessageDiv.className = 'csv-table-rendering-message';
        this.renderingMessageDiv.style.display = 'none';
        this.renderingMessageDiv.textContent = 'Rendering CSV Table HTML';
        const svgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svgElement.innerHTML = '<use href="#icon-spinner"></use>';
        this.renderingMessageDiv.appendChild(svgElement);
    }

    renderTable() {
        this.renderSuccess.checked = false;
        this.renderField.value = '';
        this.renderingMessageDiv.classList.add('working');
        this.renderingMessageDiv.style.display = 'block';
        if (!this.footerButtons) {
            this.footerButtons = document.querySelectorAll('footer button')
        }
        this.footerButtons.forEach(button => {
            button.disabled = true; // Disabling each button
        });
        fetch('/blocks/render-csv-table-proxy/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken') // Include CSRF token in headers
            },
            body: new URLSearchParams({
                'data': this.inputElements.data.value,
                'precision': this.inputElements.precision.value,
                'column_headers': this.inputElements.column_headers.checked,
                'row_headers': this.inputElements.row_headers.checked,
                'compact': this.inputElements.compact.checked
            }).toString()
        })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(errorMessage => {
                        throw new Error(errorMessage);
                    });
                }
                return response.text(); 
            })
            .then(data => {
                this.renderField.value = data;
                // clear any error messages
                this.dataErrorElement.querySelectorAll('p').forEach((p) => {
                    p.remove();
                });
                this.dataErrorElement.querySelector('svg').setAttribute('hidden', '');
                this.inputElements.data.classList.remove("csv-table-block-error");
            })
            .catch(error => {
                console.error(error.message);
                this.dataErrorElement.querySelectorAll('p').forEach((p) => {
                    p.remove();
                });
                const errorMessage = document.createElement('p');
                errorMessage.textContent = error.message;
                errorMessage.classList = "error-message csv-table-block-error";
                this.dataErrorElement.appendChild(errorMessage);
                this.dataErrorElement.querySelector('svg').removeAttribute('hidden');
                this.inputElements.data.classList.add("csv-table-block-error");
            })
            .finally(() => {
                this.footerButtons.forEach(button => {
                    button.disabled = false; // Enabling each button
                });
                this.renderSuccess.checked = true;
                this.renderingMessageDiv.classList.remove('working');
                setTimeout(() => {
                    this.renderingMessageDiv.style.display = 'none';
                }, 2500);
            });
    }
}

window.telepath.register('blocks.csv_table.CSVTableBlock', CSVTableBlockDefinition);
