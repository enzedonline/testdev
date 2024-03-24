from django.utils.translation import gettext_lazy as _
from wagtail.blocks import StructBlock
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.telepath import register


class ExternalLinkEmbedBlock(StructBlock):
    from django.utils.translation import gettext_lazy as _
    from wagtail.blocks import CharBlock, RichTextBlock, TextBlock
    from wagtail.blocks.field_block import IntegerBlock, URLBlock

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
        template='blocks/external_link_embed.html',
        icon = 'link-external'
        label = _("Embed External Article")
    
class ExternalLinkEmbedBlockAdapter(StructBlockAdapter):
    from django.utils.functional import cached_property

    js_constructor = "blocks.models.ExternalLinkEmbedBlock"

    @cached_property
    def media(self):
        from django import forms
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/embed-external-link-block.js"],
            css={"all": ("css/embed-external-link-block.css",)},
        )


register(ExternalLinkEmbedBlockAdapter(), ExternalLinkEmbedBlock)