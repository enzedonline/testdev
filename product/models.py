from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Product(models.Model):
    sku = models.CharField(max_length=10, verbose_name=_("SKU"))
    title = models.CharField(max_length=100, verbose_name=_("Product Title"))
    description = models.TextField(verbose_name=_("Product Description"))
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    icon = "cogs"
    
    panels = [
        FieldPanel("sku"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("image"),
    ]
    
    def get_icon(self):
        return self.icon

    def __str__(self):
        return f"{self.sku} - {self.title}"
    
    @property
    def preview(self):
        if self.image:
            return self.image #.get_rendition("height-60").img_tag()
