class ImportTextBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );

        const dataField = document.getElementById(prefix + '-text');
        const fileInput = document.getElementById(prefix + '-filter');

        const readFile = (source, target) => {
            const reader = new FileReader();
            reader.addEventListener('load', (event) => {
                target.value = event.target.result;
                target.style.height = target.scrollHeight 
                    + parseFloat(getComputedStyle(target).paddingTop) 
                    + parseFloat(getComputedStyle(target).paddingBottom) + 'px';
            });
            reader.readAsText(source);
        }

        fileInput.addEventListener('change', (event) => {
            event.preventDefault();
            const input = fileInput.files[0];
            readFile(input, dataField)
            fileInput.value = '';
        });
        dataField.parentElement.addEventListener('dragover', (event) => {
            event.stopPropagation();
            event.preventDefault();
            event.dataTransfer.dropEffect = 'copy';
        });
        dataField.parentElement.addEventListener('drop', (event) => {
            event.stopPropagation();
            event.preventDefault();
            const input = event.dataTransfer.files[0];
            readFile(input, dataField)
        });
        return block;
    }
}
window.telepath.register('blocks.models.ImportTextBlock', ImportTextBlockDefinition);