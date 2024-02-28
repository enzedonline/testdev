from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import CharBlock, StructBlock
from wagtail.blocks.struct_block import (StructBlockAdapter,
                                         StructBlockValidationError)
from wagtail.telepath import register

from blocks.base_blocks import CompactImageChooserBlock


class SEOImageChooserBlock(StructBlock):
    def __init__(self, required=True, **kwargs):
        local_blocks = (
            ("image", CompactImageChooserBlock(
                label=_("Image"),
                required=required
            )),
            ("description", CharBlock(
                label=_("Description"),
                help_text=_(
                    "A contextual description of the image for screen readers and search engines"
                ),
                required=required
            )),
        )   
        super().__init__(local_blocks, **kwargs)

    

    class Meta:
        icon = "image"
        label_format = '{seo_title}'
        template = 'blocks/image_block.html'
        form_classname = "structblock seo-image-chooser-block"

    def clean(self, value):
        # standard form validation
        cleaned_data = super().clean(value)
        # custom validation to run if standard form validation passes
        if not self.required and (bool(value['image']) and not bool(value['description'])):
            raise StructBlockValidationError(
                block_errors={'description': ErrorList(
                    [_("Please enter a text description for the image.")])}
            )
        return cleaned_data

class SEOImageChooserBlockAdapter(StructBlockAdapter):
    js_constructor = "blocks.seo_image_chooser.SEOImageChooserBlock"

    @cached_property
    def media(self):
        from django import forms
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/seo-image-chooser-block.js"],
            css={"all": ("css/seo-image-chooser-block.css",)},
        )
    
register(SEOImageChooserBlockAdapter(), SEOImageChooserBlock)
