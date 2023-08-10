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
            if not icon: icon = getattr(self, "icon", getattr(instance, "get_icon", "snippet"))
            return render_to_string('wagtailadmin/shared/icon.html', context=get_icon(icon))

        preview = getattr(instance, "preview", None)
        if preview:
            if isinstance(preview, Image):
                return preview.get_rendition("height-60").img_tag()
            else:
                if is_html(preview):# preview is html formatted string
                    return preview
                else:               # if preview is slug, assume preview is icon name else render viewset/model/default icon
                    return render_icon(preview) if slugify(preview) == preview else render_icon()
        else:
            return render_icon()    # no preview, render icon instead
    


class SnippetPreviewChooser(PreviewMixin, AdminSnippetChooser):
    template_name = "widgets/snippet_preview_chooser.html"
    js_constructor = "SnippetPreviewChooser"
    classname = "snippet-preview-chooser"

    def __init__(self, model, url_prefix=None, **kwargs):
        super().__init__(model, **kwargs)
        self.preview_key = "preview"
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
        return reverse(f"{self.url_prefix}:choose")

    @cached_property
    def media(self):
        widget_media = super().media
        return forms.Media(
            js=widget_media._js + ["js/widgets/snippet-preview-chooser.js"],
            css=widget_media._css,
        )


class SnippetPreviewChooserAdapter(SnippetChooserAdapter):
    js_constructor = "core.widgets.choosers.SnippetPreviewChooser"

    @cached_property
    def media(self):
        return forms.Media(
            js=[
                "js/widgets/snippet-preview-chooser-telepath.js",
            ]
        )


register(SnippetPreviewChooserAdapter(), SnippetPreviewChooser)


class SnippetPreviewChosenView(PreviewMixin, ChosenView):
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
    chosen_view_class = SnippetPreviewChosenView

    @cached_property
    def icon(self):
        return getattr(self.model, "icon", "snippet")

    @cached_property
    def widget_class(self):
        return SnippetPreviewChooser(self.model)
