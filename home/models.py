from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page


class HomePage(Page):
    content = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]
