from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.snippets.models import register_snippet

from .blocks import MenuStreamBlock
from .chooser.svg_chooser import SVGSnippetChooser
from .icons import MenuIcon

@register_snippet
class Menu(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Optional Menu Titile"))
    slug = models.SlugField(unique=True)
    icon = models.ForeignKey(
        'MenuIcon',
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
        FieldPanel('icon', widget=SVGSnippetChooser(MenuIcon)),
        FieldPanel('items')
    ]

    def __str__(self) -> str:
        return self.title

    @property
    def logo(self):
        return mark_safe(self.icon.svg) if self.icon else ''