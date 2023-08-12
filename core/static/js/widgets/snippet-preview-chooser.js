const declareSnippetPreviewChooser = async () => {
    await waitForObject(window.SnippetChooser);

    class SnippetPreviewChooser extends window.SnippetChooser {
        previewStateKey = 'preview';

        initHTMLElements(id) {
            super.initHTMLElements(id);
            this.previewElement = this.chooserElement.querySelector(
                '.chooser__preview',
            );
        }

        getPreviewStateFromHTML() {
            if (this.previewElement && this.previewStateKey) {
                this.state[this.previewStateKey] = this.previewElement.innerHTML || '';
            }
        }

        getStateFromHTML() {
            const state = super.getStateFromHTML();
            if (this.previewElement && this.previewStateKey) {
                state[this.previewStateKey] = this.previewElement.innerHTML || '';
            }
            return state;
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
