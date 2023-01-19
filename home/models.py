from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from blocks.models import ParsedRichTextBlock

class HomePage(Page):
    content = StreamField(
        [
            ("cleaned_rich_text", ParsedRichTextBlock()), 
        ], 
        verbose_name="Page body", blank=True, use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]
