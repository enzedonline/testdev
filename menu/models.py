from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import (DraftStateMixin, LockableMixin, PreviewableMixin,
                            RevisionMixin, TranslatableMixin, WorkflowMixin)
from wagtail.snippets.models import register_snippet

from .blocks import MenuStreamBlock

BREAKPOINT_CHOICES = (
    # ('none', _("No breakpoint (always collapsed)")),
    # ('sm', _("Mobile screens only (<576px)")),
    ('md', _("Small Screens (<768px)")),
    ('lg', _("Medium Screens (<992px)")),
    # ('xl', _("Extra Large (<1200px)")),
)

@register_snippet
class Menu(
    PreviewableMixin,
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    TranslatableMixin,
    models.Model,
):
    title = models.CharField(max_length=255, verbose_name=_("Menu Title"))
    slug = models.SlugField(unique=True)
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name=_("Optional Menu Title Logo"),
    )
    items = StreamField(
        MenuStreamBlock(), verbose_name="Menu Items", blank=True, use_json_field=True
    )
    breakpoint = models.CharField(
        max_length=4,
        choices=BREAKPOINT_CHOICES,
        default='lg', 
        blank=False, 
        null=True,  
        verbose_name=_("Mobile Layout Breakpoint")
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("logo"),
        FieldPanel("breakpoint"),
        FieldPanel("items"),
    ]

    def __str__(self) -> str:
        return self.title

    def get_preview_template(self, request, mode_name):
        return "menu/previews/menu.html"

    class Meta:
        verbose_name = _("Menu")
        unique_together = ("translation_key", "locale")
