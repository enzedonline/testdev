from wagtail.blocks import (CharBlock, ChoiceBlock, PageChooserBlock,
                            StructBlock, TextBlock)
from wagtail.images.blocks import ImageChooserBlock


class RequiredMixin:
    def __init__(self, *args, **kwargs):
        self._required = kwargs.get("required", True)
        super().__init__(*args, **kwargs)

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, value):
        self._required = value

    def clean(self, value):
        if getattr(self, "field", False):
            self.field.required = self.required
        return super().clean(value)


class StructBlock(RequiredMixin, StructBlock):
    def __init__(self, **kwargs):
        super().__init__(local_blocks=None, **kwargs)


class ChoiceBlock(RequiredMixin, ChoiceBlock):
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


class CharBlock(RequiredMixin, CharBlock):
    pass


class ImageChooserBlock(RequiredMixin, ImageChooserBlock):
    from django.utils.functional import cached_property

    def __init__(self, *args, widget_attrs={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_attrs = widget_attrs

    @cached_property
    def widget(self):
        from wagtail.images.widgets import AdminImageChooser

        return AdminImageChooser(**self.widget_attrs)


class PageChooserBlock(RequiredMixin, PageChooserBlock):
    from django.utils.functional import cached_property

    def __init__(self, *args, widget_attrs={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_attrs = widget_attrs

    @cached_property
    def widget(self):
        from wagtail.admin.widgets import AdminPageChooser

        return AdminPageChooser(
            target_models=self.target_models,
            can_choose_root=self.can_choose_root,
            **self.widget_attrs,
        )

class TextBlock(RequiredMixin, TextBlock):
    pass

class URLBlock(CharBlock):
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
        from django import forms
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
            from .validators import is_valid_href
            result = is_valid_href(value, protocols=self.protocols)
            if result:
                value = result
            else:
                from django.core.exceptions import ValidationError
                raise ValidationError(result)
        return super().clean(value)

    class Meta:
        icon = "link"
		
