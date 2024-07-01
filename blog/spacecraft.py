from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.api import APIField

@register_snippet
class Spacecraft(index.Indexed, models.Model):
    title = models.CharField(max_length=255, unique=True)

    panels = [
        FieldPanel("title"),
    ]

    def __str__(self):
        return self.title


class ImageDetailPageSpacecraftOrderable(Orderable):
    page = ParentalKey("blog.BlogPage", related_name="spacecrafts")
    spacecraft = models.ForeignKey(
        "blog.Spacecraft", on_delete=models.CASCADE, related_name="spacecraft"
    )

    @property
    def spacecraft_title(self):
        return self.spacecraft.title

    api_fields = [
        APIField("spacecraft_title"),
    ]

    panels = [
        FieldPanel("spacecraft"),
    ]
