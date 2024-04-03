import unidecode
import validators
from django import forms
from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import CharBlock, StructBlock
from wagtail.blocks.struct_block import (StructBlockAdapter,
                                         StructBlockValidationError)
from wagtail.telepath import register

from .choices import HeadingSizeChoiceBlock, TextAlignmentChoiceBlock


class HeadingBlock(StructBlock):
    title = CharBlock(required=True)
    heading_size = HeadingSizeChoiceBlock(default='h2')
    alignment = TextAlignmentChoiceBlock(default='start')
    anchor_id = CharBlock(
        required=False,
        label=_("Optional Anchor Identifier"),
    )

    class Meta:
        template = 'blocks/heading_block.html'
        label = _("Heading Block")
        form_classname = "struct-block heading-block"
        icon = 'title'

    def clean(self, value):
        errors = {}
        anchor_id = value.get('anchor_id')
        if anchor_id:
            if not validators.slug(anchor_id):
                slug = slugify(unidecode.unidecode(anchor_id)) or slugify(
                    unidecode.unidecode(value.get('title')))
                errors['anchor_id'] = ErrorList([_(f"\
                    '{anchor_id}' is not a valid slug for the anchor identifier. \
                    '{slug}' is the suggested value for this.")])
                raise StructBlockValidationError(block_errors=errors)

        return super().clean(value)


class HeadingBlockAdapter(StructBlockAdapter):
    @cached_property
    def media(self):
        return forms.Media(
            css={"all": ("css/heading-block.css",)},
        )


register(HeadingBlockAdapter(), HeadingBlock)
