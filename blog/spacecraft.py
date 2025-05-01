import random
import string

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.images import get_image_model
from wagtail.models import Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from core.panels.utility_panel import UtilityPanel


def generate_uuid():
    return ''.join((random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(12)))

def check_min_pixels(value):
    min_width = 350
    min_height = 250

    image = get_image_model().objects.filter(id=value).first()
    
    if image and not image.is_svg() and (image.width < min_width or image.height < min_height):
        print(image.width, image.height)
        raise ValidationError(
            _(f"Image too small ({image.width} x {image.height}px). Required: {min_width} x {min_height}px.")
        )

# @register_snippet
# class Spacecraft(index.Indexed, models.Model):
#     title = models.CharField(max_length=255, unique=True)
#     uuid = models.CharField(max_length=12, default=generate_uuid, unique=True, null=False, blank=False)
#     image = models.ForeignKey(
#         "wagtailimages.Image",
#         null=True,
#         blank=True,
#         related_name="+",
#         on_delete=models.SET_NULL,
#         validators = [check_min_pixels]
#     )

#     panels = [
#         UtilityPanel("UUID: {{uuid}}", {'uuid': 'uuid'}),
#         FieldPanel("title"),
#         FieldPanel("image"),
#     ]

#     def __str__(self):
#         return self.title
    



# class ImageDetailPageSpacecraftOrderable(Orderable):
#     page = ParentalKey("blog.BlogPage", related_name="spacecrafts")
#     spacecraft = models.ForeignKey(
#         "blog.Spacecraft", on_delete=models.CASCADE, related_name="spacecraft"
#     )

#     @property
#     def spacecraft_title(self):
#         return self.spacecraft.title

#     api_fields = [
#         APIField("spacecraft_title"),
#     ]

#     panels = [
#         FieldPanel("spacecraft"),
#     ]
