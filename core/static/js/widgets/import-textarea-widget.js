class ImportTextAreaWidget {
    constructor(id) {
        this.textArea = document.getElementById(id);
        this.textArea.parentElement.addEventListener('dragover', this.handleDragOver.bind(this));
        this.textArea.parentElement.addEventListener('drop', this.handleDrop.bind(this));
        this.fileInput = this.textArea.parentElement.querySelector('input');
        this.fileInput.addEventListener('change', this.handleFileInputChange.bind(this));
    }

    readFile(source, target) {
        const reader = new FileReader();
        reader.addEventListener('load', (event) => {
            target.value = event.target.result;
            this.textArea.dispatchEvent(new Event('input', { bubbles: true }));
        });
        reader.readAsText(source);
    }

    handleFileInputChange(event) {
        event.preventDefault();
        const input = this.fileInput.files[0];
        this.readFile(input, this.textArea);
        this.fileInput.value = '';
        this.fileInput.blur();
    }

    handleDragOver(event) {
        event.stopPropagation();
        event.preventDefault();
        event.dataTransfer.dropEffect = 'copy';
    }

    handleDrop(event) {
        event.stopPropagation();
        event.preventDefault();
        const input = event.dataTransfer.files[0];
        this.readFile(input, this.textArea);
    }
}
