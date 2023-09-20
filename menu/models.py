from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import PreviewableMixin
from wagtail.snippets.models import register_snippet

from .blocks import MenuStreamBlock


@register_snippet
class Menu(PreviewableMixin, models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Menu Title"))
    slug = models.SlugField(unique=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name=_("Optional Menu Title Logo")
    )
    items = StreamField(
        MenuStreamBlock(), verbose_name="Menu Items", blank=True, use_json_field=True
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('logo'),
        FieldPanel('items')
    ]

    def __str__(self) -> str:
        return self.title

    def get_preview_template(self, request, mode_name):
        return "menu/previews/menu.html"
    
    class Meta:
        verbose_name = _('Menu')

