from django.forms.utils import ErrorList
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import CharBlock, StructBlock
from wagtail.blocks.struct_block import StructBlockValidationError

from .choices import HeadingSizeChoiceBlock, TextAlignmentChoiceBlock


class HeadingBlock(StructBlock):
    title = CharBlock(required=True)
    heading_size = HeadingSizeChoiceBlock(default='h2')
    alignment = TextAlignmentChoiceBlock(default='start')
    anchor_target = CharBlock(
        required=False,
        label=_("Optional Anchor Target"),
        help_text=_("Anchor Target must be a compatible slug format without spaces or special characters")
    )
    
    class Meta:
        template = 'blocks/heading_block.html'
        label = _("Heading Block")
        icon = 'title'

    def clean(self, value):
        errors = {}
        anchor_target = value.get('anchor_target')
        
        if anchor_target:
            slug = slugify(unidecode.unidecode(anchor_target))
            
            if anchor_target != slug:
                errors['anchor_target'] = ErrorList([_(f"\
                    '{anchor_target}' is not a valid slug for the anchor target. \
                    '{slug}' is the suggested value for this.")])
                raise StructBlockValidationError(block_errors=errors)

        return super().clean(value)