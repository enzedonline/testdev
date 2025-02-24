const declareSnippetPreviewChooser = async () => {
    await waitForObject(window.SnippetChooser);

    class SnippetPreviewChooser extends window.SnippetChooser {
        previewStateKey = 'preview';

        initHTMLElements(id) {
            super.initHTMLElements(id);
            // Find the preview element, must be defined in the chooser template
            this.previewElement = this.chooserElement.querySelector(
                'div.chooser__preview',
            );
        }

        renderState(newState) {
            super.renderState(newState);
            if (this.previewElement && this.previewStateKey) {
                this.previewElement.innerHTML = newState[this.previewStateKey];
            }
        }
    }
    window.SnippetPreviewChooser = SnippetPreviewChooser;
};

declareSnippetPreviewChooser();
