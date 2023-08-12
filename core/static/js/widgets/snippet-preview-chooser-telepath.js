const declareSnippetPreviewChooserFactory = async () => {
    const SnippetChooserFactory = window.telepath.constructors['wagtail.snippets.widgets.SnippetChooser'];
    await waitForObject(SnippetChooserFactory);

    class SnippetPreviewChooserFactory extends SnippetChooserFactory {
        widgetClass = window.SnippetPreviewChooser;
    }

    window.telepath.register('core.widgets.choosers.SnippetPreviewChooser', SnippetPreviewChooserFactory);
};

declareSnippetPreviewChooserFactory();
