from django.db import models

from wagtail.models import Page
from wagtail.blocks import (BooleanBlock, CharBlock, PageChooserBlock,
                            RawHTMLBlock, RichTextBlock, StaticBlock,
                            StreamBlock, StructBlock, StructValue, TextBlock)
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import (FieldPanel, MultiFieldPanel)

class HomePage(Page):
    content = RichTextField()
    content_panels = Page.content_panels + [
        FieldPanel('content')
    ]
