const waitForObject = (object) => {
    return Promise.resolve(object).then((resolvedObject) => {
        if (!resolvedObject) {
            return new Promise((resolve) => {
                window.addEventListener('load', () => {
                    resolve(resolvedObject);
                });
            });
        }
        return resolvedObject;
    });
};

const declareSnippetPreviewChooserFactory = async () => {
    const SnippetChooserFactory = window.telepath.constructors['wagtail.snippets.widgets.SnippetChooser'];
    await waitForObject(SnippetChooserFactory);

    class SnippetPreviewChooserFactory extends SnippetChooserFactory {
        widgetClass = window.SnippetPreviewChooser;
    }

    window.telepath.register('core.widgets.choosers.SnippetPreviewChooser', SnippetPreviewChooserFactory);
};

declareSnippetPreviewChooserFactory();
