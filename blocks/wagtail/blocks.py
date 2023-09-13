from django import forms
from wagtail import blocks
from wagtail.images import blocks as image_blocks

from .validators import is_valid_href
from django.core.exceptions import ValidationError


class RequiredMixin:
    def __init__(self, *args, **kwargs):
        self._required = kwargs.get('required', True)
        super().__init__(*args, **kwargs)

    @property
    def required(self):
        return self._required
    
    @required.setter
    def required(self, value):
        self._required = value

    def clean(self, value):
        if getattr(self, 'field', False):
            self.field.required = self.required
        return super().clean(value)

class StructBlock(RequiredMixin, blocks.StructBlock):
    def __init__(self, **kwargs):
        super().__init__(local_blocks=None, **kwargs)

class URLBlock(RequiredMixin, blocks.URLBlock):
    def __init__(
        self,
        required=True,
        help_text=None,
        max_length=None,
        min_length=None,
        validators=(),
        protocols=[
            "http",
            "https",
            "ftp",
            "ftps",
            "callto",
            "skype",
            "chrome-extension",
            "facetime",
            "gtalk",
            "mailto",
            "tel",
        ],
        ** kwargs,
    ):
        self.field = forms.CharField(
            required=required,
            help_text=help_text,
            max_length=max_length,
            min_length=min_length,
            validators=validators,
        )
        super().__init__(required=required, **kwargs)
        self.protocols = protocols

    def clean(self, value):
        if value:
            result = is_valid_href(value, protocols=self.protocols)
            if result:
                value = result
            else:
                raise ValidationError(result)        
        return super().clean(value)
    
    class Meta:
        icon = "link-external"

class ChoiceBlock(RequiredMixin, blocks.ChoiceBlock):

    def __init__(self, *args, **kwargs):

        default = kwargs.pop("default", getattr(self, "default", None))
        label = kwargs.pop("label", getattr(self, "label", None))
        help_text = kwargs.pop("help_text", getattr(self, "help_text", None))
        required = kwargs.pop("required", getattr(self, "required", True))

        super().__init__(
            *args,
            default=default,
            label=label,
            help_text=help_text,
            required=required,
            **kwargs
        )

class CharBlock(RequiredMixin, blocks.CharBlock):
    pass

class ImageChooserBlock(RequiredMixin, image_blocks.ImageChooserBlock):
    pass

class TextBlock(RequiredMixin, blocks.TextBlock):
    pass
