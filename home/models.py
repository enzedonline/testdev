from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page
from blocks.models import CSVTableBlock, ParsedRichTextBlock, ImportTextBlock

class HomePage(Page):
    intro = RichTextField(blank=True, null=True)
    content = StreamField(
        [
            ("cleaned_rich_text", ParsedRichTextBlock()), 
            ("csv_table", CSVTableBlock()), 
            ('import_text_block', ImportTextBlock()),
        ], 
        verbose_name="Page body", blank=True, use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('content'),
    ]
