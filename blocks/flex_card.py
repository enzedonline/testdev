from django import forms
from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import BooleanBlock, IntegerBlock, StructBlock
from wagtail.blocks.struct_block import (StructBlockAdapter,
                                         StructBlockValidationError)
from wagtail.telepath import register

from .choices import (BreakpointChoiceBlock, ColourThemeChoiceBlock,
                      FlexCardLayoutChoiceBlock)
from .seo_image_chooser import SEOImageChooserBlock
from .links import LinkBlock
from .rich_text import SimpleRichTextBlock


class FlexCardBlock(StructBlock):
    
    text = SimpleRichTextBlock(
        label=_("Card Body Text"),
        help_text=_("Body text for this card."),
    )
    background = ColourThemeChoiceBlock(
        default='bg-transparent',
        label=_("Card Background Colour")
    )
    border = BooleanBlock(
        default=True,
        required=False,
        label=_("Border"),
        help_text=_("Draw a border around the card?")
    )
    link = LinkBlock(
        label=_("Optional Card Link"),
        required=False,
        help_text=_("If using a link, setting a link label will render a hyperlink button.<br>\
                    Leave link label blank to make the whole card a clickable link."),
    )
    image = SEOImageChooserBlock(
        label=_("Select Image & Enter Details"),
        help_text=_("Card Image (approx 1:1.4 ratio - ideally upload 2100x1470px)."),
        required=False
    )
    image_min = IntegerBlock(
        label=_("Minimum width the image can shrink to (pixels)"),
        default=200,
        min_value=100
    )
    image_max = IntegerBlock(
        label=_("Optional maximum width the image can grow to (pixels)"),
        required=False
    )
    layout = FlexCardLayoutChoiceBlock(
        max_length=15,
        default='vertical',
        label=_("Card Format")
    )    
    breakpoint = BreakpointChoiceBlock(
        default = 'md',
        label=_("Breakpoint for responsive layouts")
    )

    class Meta:
        template = 'blocks/flex_card_block.html'
        label = _("Image & Text Card")
        icon = 'image'

    def clean(self, value):
        errors = {}
        image_min = value.get('image_min')
        image_max = value.get('image_max')

        if value.get('layout') == 'vertical':
            value['breakpoint'] = 'none'

        if image_min and image_max and image_min > image_max:
            errors['image_min'] = ErrorList([_("Please make sure minimum is less than maximum.")])
            errors['image_max'] = ErrorList([_("Please make sure minimum is less than maximum.")])
        if errors:
            raise StructBlockValidationError(block_errors=errors)

        return super().clean(value)     


class FlexCardBlockAdapter(StructBlockAdapter):
    js_constructor = "blocks.models.FlexCardBlock"

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/flex-card-block.js"],
        )


register(FlexCardBlockAdapter(), FlexCardBlock)