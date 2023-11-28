from wagtail.blocks import StructBlock

class CSVTableBlock(StructBlock):
    from django.utils.translation import gettext_lazy as _
    from wagtail.blocks import BooleanBlock, RichTextBlock
    from wagtail.blocks.field_block import IntegerBlock

    from .choices import TextAlignmentChoiceBlock
    from .heading import HeadingBlock
    from .import_text import ImportTextBlock

    title = HeadingBlock(required=False, label=_("Table Title"))
    data = ImportTextBlock(
        label=_("Comma Separated Data"),
        help_text=_("Paste in CSV data or import from .csv file"),
        file_type_filter='.csv'
    )
    precision = IntegerBlock(
        label=_("Float Precision"),
        default=2, help_text=_("Number of decimal places to display for float type.")
    )
    column_headers = BooleanBlock(
        label=_("Column Headers"),
        required=False, default=True, help_text=_("First row contains column headers")
    )
    row_headers = BooleanBlock(
        label=_("Row Headers"),
        required=False, help_text=_("First column contains row headers")
    )
    compact = BooleanBlock(
        label=_("Compact Table Style"),
        required=False, 
        help_text=_("Cell padding reduced by half")
    )
    caption = RichTextBlock(
        label=_("Table Caption"),
        editor="minimal", 
        required=False,
        help_text=_("Caption displayed beneath the table. Use as explanation or annotation.")
    )
    caption_alignment = TextAlignmentChoiceBlock(
        label=_("Caption Alignment"),
        required=False, 
        default="end"
    )
    width = IntegerBlock(
        label=_("Table Width (%)"),
        default=100,
        help_text=_("Table width (as percentage of container)"),
    )
    max_width = IntegerBlock(
        label=_("Maximum Table Width (rem)"),
        required=False,
        help_text=_("Optional: Maximum width (in rem) the table can grow to"),
    )

    class Meta:
        template = "blocks/csv_table_block.html"
        icon = "table"
        label = "CSV Table"
