from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.snippets.models import register_snippet

from svg.chooser.widget import SVGChooser

from .blocks import MenuStreamBlock


@register_snippet
class Menu(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Menu Title"))
    slug = models.SlugField(unique=True)
    image = models.ForeignKey(
        'svg.SVGImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+', 
        verbose_name=_("Optional Menu Title Logo")
    )
    items = StreamField(
        MenuStreamBlock(), verbose_name="Menu Items", blank=True, use_json_field=True
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('slug'),
        FieldPanel('image', widget=SVGChooser),
        FieldPanel('items')
    ]

    def __str__(self) -> str:
        return self.title

    @property
    def logo(self):
        return mark_safe(self.image.svg) if self.image else ''
    
    class Meta:
        verbose_name = _('Menu')

