from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import TextBlock
from core.widgets import ImportTextAreaWidget

class ImportTextBlock(TextBlock):
    def __init__(self, required=True, help_text=None, rows=1, max_length=None, min_length=None, file_type_filter="", validators=(), **kwargs):
        super().__init__(required, help_text, rows, max_length, min_length, validators, **kwargs)
        self.file_type_filter = file_type_filter

    @cached_property
    def field(self):
        field_kwargs = {"widget": ImportTextAreaWidget(self.file_type_filter, attrs={"rows": self.rows})}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)
