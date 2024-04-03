from django.utils.functional import cached_property
from django.forms.widgets import HiddenInput, Textarea
from wagtail.blocks import CharBlock, TextBlock, BooleanBlock

class HiddenBlockMixin:
    def __init__(self, attrs={}, **kwargs):
        kwargs['label'] = ' '
        kwargs['help_text'] = ''
        kwargs['required'] = False
        super().__init__(**kwargs)
        attrs['hidden'] = ''        
        self.attrs = attrs
        self.attrs = self.field.widget.attrs.update(attrs)

class HiddenCharBlock(HiddenBlockMixin, CharBlock):
    pass

class HiddenTextBlock(HiddenBlockMixin, TextBlock):
    pass

class HiddenBooleanBlock(HiddenBlockMixin, BooleanBlock):
    pass