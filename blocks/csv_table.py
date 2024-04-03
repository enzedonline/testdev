from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import BooleanBlock, RichTextBlock, StructBlock
from wagtail.blocks.field_block import IntegerBlock
from wagtail.blocks.struct_block import (StructBlockAdapter,
                                         StructBlockValidationError)
from wagtail.telepath import register

from .choices import TextAlignmentChoiceBlock
from .heading import HeadingBlock
from .hidden import HiddenBooleanBlock, HiddenCharBlock
from .import_text import ImportTextBlock


class CSVTableBlock(StructBlock):
    title = HeadingBlock(
        label=_("Optional Table Title"),
        required=False, 
        heading_range=('h3', 'h5'),
        default_size='h4',
        default_alignment='center'
    )
    data = ImportTextBlock(
        label=_("Comma Separated Data"),
        help_text=_("Paste in CSV data or import from .csv file"),
        file_type_filter='.csv'
    )
    precision = IntegerBlock(
        label=_("Float Precision"),
        default=2,
    )
    column_headers = BooleanBlock(
        label=_("Column Headers"),
        required=False, 
        default=True,
    )
    row_headers = BooleanBlock(
        label=_("Row Headers"),
        required=False, 
    )
    compact = BooleanBlock(
        label=_("Compact"),
        required=False, 
        default=True,
    )
    caption = RichTextBlock(
        label=_("Table Caption"),
        editor="minimal", 
        required=False,
        help_text=_("Caption displayed beneath the table. Use as explanation or annotation.")
    )
    caption_alignment = TextAlignmentChoiceBlock(
        label=_("Caption Alignment"),
        default="end"
    )
    width = IntegerBlock(
        label=_("Table Width (%)"),
        default=100,
    )
    max_width = IntegerBlock(
        label=_("Maximum Table Width (rem)"),
        required=False,
    )
    html = HiddenCharBlock()
    rendered = HiddenBooleanBlock(default=True)

    class Meta:
        template = "blocks/csv_table_block.html"
        icon = "table"
        label = "CSV Table"
        form_classname = "struct-block flex-block csv-table-block"

    def clean(self, value):
        rendered = value.get('rendered')
        if not rendered:
            raise StructBlockValidationError(non_block_errors=['There was an error rendering the CSV table.'])
        return super().clean(value)
    
class CSVTableBlockAdapter(StructBlockAdapter):
    js_constructor = "blocks.csv_table.CSVTableBlock"

    @cached_property
    def media(self):
        from django import forms
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/csv-table-block.js"],
            css={"all": ("css/csv-table-block.css",)},
        )
    
register(CSVTableBlockAdapter(), CSVTableBlock)
