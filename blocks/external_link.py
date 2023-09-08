from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import RichTextBlock, CharBlock, StructBlock, TextBlock
from wagtail.blocks.field_block import IntegerBlock, URLBlock
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.telepath import register

from .choices import *


class ExternalLinkEmbedBlock(StructBlock):
    external_link = URLBlock(
        label=_("URL to External Article"),
        help_text=_("Use the 'Get Metadata' button to retrieve information from the external website."),
    )
    description = RichTextBlock()
    image = CharBlock(
        max_length=200, 
        required=False
    )

    class Meta:
        # template='blocks/external_link_embed.html',
        icon = 'link-external'
        label = _("Embed External Article")
    
class ExternalLinkEmbedBlockAdapter(StructBlockAdapter):
    js_constructor = "blocks.models.ExternalLinkEmbedBlock"

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/embed-external-link-block.js"],
            css={"all": ("css/embed-external-link-block.css",)},
        )


register(ExternalLinkEmbedBlockAdapter(), ExternalLinkEmbedBlock)