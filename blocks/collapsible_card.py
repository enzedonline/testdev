from django.utils.translation import gettext_lazy as _
from wagtail.blocks import CharBlock, StructBlock, RichTextBlock, ListBlock

from .choices import ColourThemeChoiceBlock


class CollapsibleCard(StructBlock):
    header = CharBlock(
        label=_("Card Banner Title")
    )
    text = RichTextBlock(
        label=_("Card Body Text"),
        help_text=_("Body text for this card."),
    )

class CollapsibleCardBlock(StructBlock):
    header_colour  = ColourThemeChoiceBlock(
        default='bg-dark',
        label=_("Card Header Background Colour")
    )    
    body_colour  = ColourThemeChoiceBlock(
        default='bg-light',
        label=_("Card Body Background Colour")
    )
    cards = ListBlock(CollapsibleCard, min_num=2)

    class Meta:
        template='blocks/collapsible_card_block.html'
        icon="collapse-down"
        label = _("Collapsible Text Block")

