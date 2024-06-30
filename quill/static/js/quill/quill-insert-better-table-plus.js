class InsertBetterTablePlus {
    constructor(quill, options={}) {
        this.quill = quill;
        this.columns = options['maxColumns'] ?? 5;
        this.rows = options['maxRows'] ?? 7;
        if (!Number.isInteger(this.columns) || this.columns <= 0) {
            console.warn('Invalid max_columns value. It should be a positive integer. Setting to default value of 5.');
            this.columns = 5;
        }
        if (!Number.isInteger(this.rows) || this.rows <= 0) {
            console.warn('Invalid max_rows value. It should be a positive integer. Setting to default value of 7.');
            this.rows = 7;
        }
        this.tableClassList = options['tableClassList'] ?? ['table'];
        if (!Array.isArray(this.tableClassList)) {
            if (this.tableClassList.includes(' ')) {
                this.tableClassList = this.tableClassList.split(' ')
            } else {
                this.tableClassList = [this.tableClassList];
            }
        }
        this.toolbar = this.quill.getModule("toolbar");
        if (this.toolbar) {
            this.toolbar.addHandler("insert-better-table-plus", this._toolbarResponse.bind(this));
            this.button = this.toolbar.container.querySelector('span.ql-insert-better-table-plus')
            if (this.button) {
                this._buildDropdownMenu();
            }
        }
    }

    _buildDropdownMenu() {
        const pickerLabel = this.button.querySelector('span.ql-picker-label');
        pickerLabel.innerHTML = this._icon();
        const pickerOptions = this.button.querySelector('span.ql-picker-options');
        pickerOptions.innerHTML = 
            Array.from({ length: this.rows }, (_, r) => 
                Array.from({ length: this.columns }, (_, c) => 
                    `<span tabindex="0" role="button" class="ql-picker-item" 
                        data-row-count="${r + 1}" 
                        data-col-count="${c + 1}" 
                        title="${r + 1}x${c + 1}"></span>`
                )
            ).flat().join('').replace(/\s+/g, ' ').trim();
        pickerOptions.style = `grid-template-columns: repeat(${this.columns}, 1fr);`;
        const pickerItems = pickerOptions.querySelectorAll('span.ql-picker-item');
        pickerItems.forEach(span => {
            span.addEventListener('click', (event) => {
                const betterTablePlus = this.quill.getModule('better-table-plus');
                this.button.classList.remove('ql-expanded');
                pickerLabel.setAttribute('aria-expanded', 'false');
                betterTablePlus.insertTable(
                    Number(event.target.dataset.rowCount),
                    Number(event.target.dataset.colCount)
                );
                // Remove the selected and active classes
                this.button.querySelectorAll('.ql-selected, .ql-active').forEach(el => {
                    el.classList.remove('ql-selected', 'ql-active');
                });
                // add additional table css classes
                const range = this.quill.getSelection(true);
                const currentBlot = this.quill.getLeaf(range.index)[0];
                const addedTable = currentBlot.parent.domNode.closest('table.quill-better-table');
                if (addedTable) {
                    addedTable.classList.add(...this.tableClassList);
                }
            });
            span.addEventListener('mouseenter', (event) => {
                pickerItems.forEach(sibling => {
                    if (
                        Number(sibling.dataset.rowCount) <= Number(event.target.dataset.rowCount) &&
                        Number(sibling.dataset.colCount) <= Number(event.target.dataset.colCount)
                    ) {
                        sibling.classList.add('ql-picker-item-highlight');
                    }
                });
            });
            span.addEventListener('mouseleave', () => {
                pickerOptions.querySelectorAll('.ql-picker-item-highlight').forEach(sibling => {
                    sibling.classList.remove('ql-picker-item-highlight');
                });
            });
        });

    }

    _toolbarResponse() {
        return true;
    }

    _icon() {
        return `
            <svg viewbox="0 0 18 18" style="left: 0;">
                <rect class="ql-stroke" height="14.76924" width="14.769239" x="0.61538005" y="0.61538005"/>
                <rect class="ql-fill" height="2.46154" width="3.6923099" x="3.0769198" y="3.0769203" />
                <rect class="ql-fill" height="2.46154" width="4.92308" x="8.000001" y="3.0769203" />
                <g style="opacity:0.5;" class="ql-fill" transform="matrix(1.23077,0,0,1.23077,-3.0769299,-3.0769298)">
                    <rect height="2" width="3" x="5" y="8"/>
                    <rect height="2" width="4" x="9" y="8"/>
                    <rect height="2" width="3" x="5" y="11"/>
                    <rect height="2" width="4" x="9" y="11"/>
                </g>
            </svg>
        `;
    }

}
