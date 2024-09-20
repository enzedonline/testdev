import random
import string

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.models import Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from core.panels.utility_panel import UtilityPanel


def generate_uuid():
    return ''.join((random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(12)))

@register_snippet
class Spacecraft(index.Indexed, models.Model):
    title = models.CharField(max_length=255, unique=True)
    uuid = models.CharField(max_length=12, default=generate_uuid, unique=True, null=False, blank=False, )

    panels = [
        UtilityPanel("UUID: {{uuid}}", {'uuid': 'uuid'}),
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
