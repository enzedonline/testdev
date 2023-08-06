const waitForSnippetChooser = () => {
    return new Promise((resolve) => {
        if (window.SnippetChooser) {
            resolve();
        } else {
            // If SnippetChooser is not available, wait for it to be loaded
            window.addEventListener('load', () => {
                resolve();
            });
        }
    });
};

const declareSnippetPreviewChooser = async () => {
    await waitForSnippetChooser();

    class SnippetPreviewChooser extends window.SnippetChooser {
        constructor(id, opts = {}) {
            console.log('constructor: ' + id)
            super(id, opts);
            this.previewStateKey = 'preview';
            if (this.state) {
                this.getPreviewStateFromHTML();
            }
        }

        initHTMLElements(id) {
            console.log('initHTMLElements: ' + id)
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
            if (state) {
                this.getPreviewStateFromHTML()
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
    window.telepath.register('core.widgets.choosers.SnippetPreviewChooser', SnippetPreviewChooser);
};

declareSnippetPreviewChooser();

