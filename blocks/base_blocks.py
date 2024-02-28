from django import forms
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from wagtail.admin.widgets import AdminPageChooser
from wagtail.blocks import CharBlock, ChoiceBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.widgets import AdminImageChooser

from .validators import is_valid_href


class CompactImageChooserBlock(ImageChooserBlock):
    def __init__(self, *args, widget_attrs={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_attrs = widget_attrs
        self.widget_attrs["show_edit_link"]=False

    class Meta:
        form_classname = "compact-image-chooser"

    @property
    def widget(self):
        chooser = AdminImageChooser(**self.widget_attrs)
        return chooser    

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

class CustomPageChooserBlock(PageChooserBlock):
    def __init__(self, *args, widget_attrs={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_attrs = widget_attrs

    @cached_property
    def widget(self):
        return AdminPageChooser(
            target_models=self.target_models,
            can_choose_root=self.can_choose_root,
            **self.widget_attrs,
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
        icon = "link"
		
