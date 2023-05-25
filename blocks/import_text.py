from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import StructBlock, TextBlock
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.telepath import register


class ImportTextBlock(StructBlock):
    def __init__(self, local_blocks=None, file_type_filter="", **kwargs):
        super().__init__(local_blocks, **kwargs)
        self.accept = file_type_filter

    text = TextBlock()

    class Meta:
        icon = "collapse-down"
        label = "Import Text"
        form_template = "blocks/forms/import_text_block_form.html"

    def get_form_context(self, value, prefix="", errors=None):
        context = super().get_form_context(value, prefix, errors)
        context['instructions'] = _("Use 'Choose File' or drag/drop to import data from file.")
        context["filter"] = self.accept
        return context


class ImportTextBlockAdapter(StructBlockAdapter):
    js_constructor = "blocks.models.ImportTextBlock"

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/import-text-block.js"],
            css={"all": ("css/import-text-block.css",)},
        )


register(ImportTextBlockAdapter(), ImportTextBlock)
