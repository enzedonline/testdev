from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, TitleFieldPanel
from wagtail.admin.ui.tables import LiveStatusTagColumn, UpdatedAtColumn
from wagtail.admin.widgets.slug import SlugInput
from wagtail.fields import StreamField
from wagtail.images.widgets import AdminImageChooser
from wagtail.models import (DraftStateMixin, LockableMixin, PreviewableMixin,
                            RevisionMixin, TranslatableMixin, WorkflowMixin)
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .blocks import MenuStreamBlock

class BaseMenu(
    PreviewableMixin,
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    models.Model,
):
    icon = "menu"

    title = models.CharField(
        max_length=255,
        verbose_name=_("Menu Title"),
        help_text=_("A descriptive name for this menu (not displayed)")
    )
    slug = models.SlugField(
        unique=True,
        verbose_name=_("Slug")
    )
    breakpoint = models.CharField(
        max_length=5,
        choices=(
            ("", _("Always expanded")),
            ("-sm", _("Mobile only (<576px)")),
            ("-md", _("Medium (<768px)")),
            ("-lg", _("Large (<992px)")),
            ("-xl", _("Extra Large (<1200px)")),
            ("-none", _("Always collapsed")),
        ),
        default="-lg",
        blank=True,
        null=False,
        verbose_name=_("Mobile Layout Breakpoint"),
        help_text=_("Select screen widths to display menu in collapsed format.")
    )
    brand_title = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Optional Brand Display Title")
    )
    brand_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name=_("Optional Brand Logo"),
    )
    items = StreamField(
        MenuStreamBlock(), 
        verbose_name=_("Menu Items"), 
        blank=True
    )

    panels = [
        MultiFieldPanel([
            TitleFieldPanel("title", icon="info-circle",classname="menu-title"),
            FieldPanel("slug", icon="cogs", classname="menu-slug"),
            FieldPanel("breakpoint", icon="mobile-alt", classname="menu-breakpoint"),
            FieldPanel("brand_title", icon="title", classname="menu-brand-title"),
            FieldPanel("brand_logo", widget=AdminImageChooser(show_edit_link=False), classname="menu-brand-logo compact-image-chooser"),
        ], _('Menu Settings'), classname="menu-settings"),
        FieldPanel("items"),
    ]

    def __str__(self) -> str:
        return self.title

    def get_preview_template(self, request, mode_name):
        return "menu/previews/menu.html"

    class Meta:
        verbose_name = _("Menu")
        abstract = True


if getattr(settings, "WAGTAIL_I18N_ENABLED", False):
    class Menu(TranslatableMixin, BaseMenu):
        # unique = True not compatible with TranslatableMixin, use unique_together instead
        slug = models.SlugField(
            unique=False,
            verbose_name=_("Slug")
        )
        class Meta:
            unique_together = ('translation_key', 'locale'), ('locale', 'slug')            
else:
    class Menu(BaseMenu):
        pass

class MenuViewSet(SnippetViewSet):
    model = Menu
    icon = "menu"
    list_display = ["title", "slug", UpdatedAtColumn(), LiveStatusTagColumn()]
    ordering = ["title"]


register_snippet(MenuViewSet)
