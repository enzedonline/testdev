from django import forms
from django.core.exceptions import ValidationError
from wagtail.blocks import CharBlock, ChoiceBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from .validators import is_valid_href


class DefaultChoiceBlock(ChoiceBlock):
    def __init__(self, *args, **kwargs):
        default = kwargs.pop("default", getattr(self, "default", None))
        label = kwargs.pop("label", getattr(self, "label", None))
        help_text = kwargs.pop("help_text", getattr(self, "help_text", None))

        super().__init__(
            *args,
            default=default,
            label=label,
            help_text=help_text,
            **kwargs,
        )


class ExtendedURLBlock(CharBlock):
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
        allow_relative=True,
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
        self.allow_relative = allow_relative

    def clean(self, value):
        if value:
            result = is_valid_href(
                value, protocols=self.protocols, relative=self.allow_relative
            )
            if result:
                value = result
            else:
                raise ValidationError(result)
        return super().clean(value)

    class Meta:
        icon = "link"

class CustomChooserMixin:
    def __init__(self, *args, chooser_attrs={"show_edit_link":False}, **kwargs):
        super().__init__(*args, **kwargs)
        self.chooser_attrs = chooser_attrs

    @property
    def widget(self):
        chooser = super().widget
        for key, value in self.chooser_attrs.items():
            if hasattr(chooser, key):
                setattr(chooser, key, value)
        return chooser
        
class CustomImageChooserBlock(CustomChooserMixin, ImageChooserBlock):
    pass

class CustomPageChooserBlock(CustomChooserMixin, PageChooserBlock):
    pass

class CustomSnippetChooserBlock(CustomChooserMixin, PageChooserBlock):
    pass

