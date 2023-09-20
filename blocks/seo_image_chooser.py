from django import forms
from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import StructBlock, StructBlockValidationError
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.telepath import register

from blocks.wagtail.blocks import CharBlock, ImageChooserBlock, RequiredMixin


class SEOImageChooserBlock(RequiredMixin, StructBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs:
            self.declared_blocks["image"].required = kwargs.get("required", True)
            self.declared_blocks["seo_title"].required = kwargs.get("required", True)

    image = ImageChooserBlock(label=_("Image"))
    seo_title = CharBlock(
        label=_("SEO Title"),
        help_text=_(
            "A text description of the image for screen readers and search engines"
        ),
    )

    class Meta:
        form_classname = "seo-image-chooser-block"

    @cached_property
    def image_error(self):
        return ErrorList([_("Please select an image")])

    @cached_property
    def title_error(self):
        return ErrorList([_("Please enter a descriptive SEO title for the image")])

    def clean(self, value):
        errors = {}
        image = value.get("image")
        seo_title = value.get("seo_title")
        if self.required:
            if not image:
                errors["image"] = self.image_error
            if not seo_title:
                errors["seo_title"] = self.title_error
        elif image and not seo_title:
            errors["seo_title"] = self.title_error

        if errors:
            raise StructBlockValidationError(block_errors=errors)

        return super().clean(value)


class SEOImageChooserBlockAdapter(StructBlockAdapter):
    js_constructor = "blocks.models.SEOImageChooserBlock"

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/seo-image-chooser-block.js"],
            css={"all": ("css/seo-image-chooser-block.css",)},
        )


register(SEOImageChooserBlockAdapter(), SEOImageChooserBlock)
