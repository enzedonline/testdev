from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class Spacecraft(index.Indexed, models.Model):
    spacecraft = models.CharField(max_length=255, unique=True)

    panels = [
        FieldPanel("spacecraft"),
    ]

    search_fields = [
        index.AutocompleteField("spacecraft")
    ]

    def __str__(self):
        return self.spacecraft


class ImageDetailPageSpacecraftOrderable(Orderable):
    page = ParentalKey("blog.BlogPage", related_name="spacecraft_page")
    spacecraft_name = models.ForeignKey(
        "blog.Spacecraft", on_delete=models.CASCADE, related_name="spacecraft_name"
    )

    panels = [
        FieldPanel("spacecraft_name"),
    ]
