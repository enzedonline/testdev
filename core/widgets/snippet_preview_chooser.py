from django import forms
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from wagtail.admin.templatetags.wagtailadmin_tags import icon as get_icon
from wagtail.images.models import Image
from wagtail.snippets.views.chooser import ChooserViewSet, ChosenView
from wagtail.snippets.widgets import AdminSnippetChooser, SnippetChooserAdapter
from wagtail.telepath import register

from core.utils import is_html


class PreviewMixin:
    @mark_safe
    def get_preview(self, instance):
        """
        Snippet model should have a 'preview' property that returns
        - a wagtail image (or custom subclass)
        - a rendered html string for the preview image for that instance
        - a registered icon name
        If preview is None or does not exist, defaults to viewset/model icon if exists, else the default snippet icon
        """

        def render_icon(icon=None):
            if not icon:
                icon = getattr(self, "icon", getattr(instance, "get_icon", "snippet"))
            context=get_icon(icon)
            return f'''<svg class="icon icon-{context['name']} {context['classname']}" viewBox="0 0 24 24" height="60px" aria-hidden="true">
                        <use href="#icon-{context['name']}"></use>
                       </svg>'''

        preview = getattr(instance, self.preview_name, None)
        if preview:
            if isinstance(preview, Image):
                return preview.get_rendition('height-60').img_tag({'class':"show-transparency"})
            else:
                if is_html(preview):  # preview is html formatted string
                    return preview
                else:  # if preview is slug, assume preview is icon name else render viewset/model/default icon
                    return (
                        render_icon(preview)
                        if slugify(preview) == preview
                        else render_icon()
                    )
        else:
            return render_icon()  # no preview, render icon instead


class SnippetPreviewChooser(PreviewMixin, AdminSnippetChooser):
    """
    Extends the default snippet chooser to include a dynamic preview icon.
    Add preview method to snippet class to return image, icon name or rendered image HTML
    """

    template_name = "widgets/snippet_preview_chooser.html"
    js_constructor = "SnippetPreviewChooser"
    classname = "snippet-preview-chooser"

    def __init__(self, model, url_prefix=None, preview_name="preview", **kwargs):
        super().__init__(model, **kwargs)
        self.preview_key = "preview"
        self.preview_name = preview_name
        self.url_prefix = url_prefix if url_prefix else model._meta.model_name
        if not self.icon:
            self.icon = getattr(model, "icon", "snippet")

    # wagtail.admin.viewsets.chooser.py: ChooserViewset.get_block_class() throws an error if widget class not callable
    # "widget": self.widget_class() in cls definition (L209 in Wagtail 5.0)
    def __call__(self, *args, **kwargs):
        return self

    def get_context(self, name, value_data, attrs):
        context = super().get_context(name, value_data, attrs)
        context[self.preview_key] = value_data.get(self.preview_key, "")
        return context

    def get_value_data_from_instance(self, instance):
        value_data = super().get_value_data_from_instance(instance)
        value_data[self.preview_key] = self.get_preview(instance)
        return value_data

    def get_chooser_modal_url(self):
        # override snippet chooser modal url -default url overrides custom view classes
        return reverse(f"{self.url_prefix}:choose")

    @cached_property
    def media(self):
        widget_media = super().media
        return forms.Media(
            js=widget_media._js + ["js/widgets/snippet-preview-chooser.js"],
            css=widget_media._css,
        )


class SnippetPreviewChooserAdapter(SnippetChooserAdapter):
    """Register SnippetPreviewChooser for use in blocks"""

    js_constructor = "core.widgets.choosers.SnippetPreviewChooser"

    @cached_property
    def media(self):
        widget_media = super().media
        return forms.Media(
            js=widget_media._js + [
                "js/widgets/snippet-preview-chooser-telepath.js",
            ]
        )


register(SnippetPreviewChooserAdapter(), SnippetPreviewChooser)


class SnippetPreviewChosenView(PreviewMixin, ChosenView):
    # model fieldname or property used to return preview image
    preview_name = "preview"

    # add preview to returned chosen data
    def get_chosen_response(self, item):
        return self._wrap_chosen_response_data(
            {
                "id": str(self.get_object_id(item)),
                "string": self.get_display_title(item),
                "preview": self.get_preview(item),
                "edit_url": self.get_edit_item_url(item),
            }
        )


class SnippetPreviewChooserViewSet(ChooserViewSet):
    """
    Abstract ViewSet class helper. Name and url prefix default to model name.
    Example usage:
        class ProductChooserViewSet(SnippetPreviewChooserViewSet):
            model = Product
        product_chooser_viewset = ProductChooserViewSet()
    """

    def __init__(self, name=None, *args, **kwargs):
        if not name:
            name = self.model._meta.model_name
        super().__init__(name=name, *args, **kwargs)

    chosen_view_class = SnippetPreviewChosenView

    @cached_property
    def icon(self):
        return getattr(self.model, "icon", "snippet")

    @cached_property
    def widget_class(self):
        return SnippetPreviewChooser(
            model=self.model,
            url_prefix=self.name,
            preview_name=SnippetPreviewChosenView.preview_name,
        )

    class Meta:
        abstract = True
