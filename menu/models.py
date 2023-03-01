from bs4 import BeautifulSoup
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import (BooleanBlock, CharBlock, ChoiceBlock, IntegerBlock,
                            PageChooserBlock, StreamBlock, StructBlock,
                            StructValue, URLBlock)
from wagtail.fields import StreamField
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet

from .panels import FileToTextFieldPanel


class MenuIconForm(WagtailAdminPageForm):
    def clean(self) -> None:
        # check valid svg has been entered
        cleaned_data = super().clean()
        soup = BeautifulSoup(cleaned_data.get('svg'), 'xml')
        svg = soup.find('svg')
        if svg:
            del svg['height']
            del svg['width']
            # remove this next loop if you wany to allow <script> tags in <svg> icons
            for script in svg.find_all('script'):
                script.extract()
            cleaned_data['svg'] = str(svg.prettify())
        else:
            self.add_error('svg', _("Please enter a valid SVG including the SVG element."))
        return cleaned_data
    
@register_snippet
class MenuIcon(models.Model):
    base_form_class = MenuIconForm

    label = models.CharField(max_length=255)
    svg = models.TextField(verbose_name="SVG", help_text=_("Height and width attributes will be stripped on save."))

    panels = [
        FieldPanel('label'),
        FileToTextFieldPanel('svg'),
    ]

    def __str__(self) -> str:
        return self.label


class DefaultChoiceBlock(ChoiceBlock):

    def __init__(self, *args, **kwargs):

        default = kwargs.pop("default", getattr(self, "default", None))
        label = kwargs.pop("label", getattr(self, "label", None))
        help_text = kwargs.pop("help_text", getattr(self, "help_text", None))
        required = kwargs.pop("required", getattr(self, "required", True))

        super().__init__(
            *args,
            default=default,
            label=label,
            help_text=help_text,
            required=required,
            **kwargs
        )
        
class DisplayWhenChoiceBlock(DefaultChoiceBlock):        
    choices=[
        ('ALWAYS', _("Always")),
        ('True', _("When logged in")),
        ('False', _("When not logged in"))
    ]
    default='ALWAYS'
    help_text=_("Determines if menu item is only shown if user logged in, logged out or always")

class MenuItemValue(StructValue):
    @property
    def svg(self):
        icon = self.get("icon")
        return mark_safe(icon.svg) if icon else ''
    
class MenuStructBlock(StructBlock):
    icon = SnippetChooserBlock(
        MenuIcon,
        required=False,
        label=_("Optional icon for display")
    )
    display_when = DisplayWhenChoiceBlock(required=False)

    class Meta:
        value_class = MenuItemValue

class InternalLinkValue(MenuItemValue):
    @property
    def url(self) -> str:
        internal_page = self.get("page")
        return internal_page.localized.url

    @property
    def title(self) -> str:
        display_title = self.get("display_title")
        page = self.get("page")
        return display_title or page.title
    
class InternalLinkBlock(MenuStructBlock):
    page = PageChooserBlock()
    display_title = CharBlock(
        max_length=255, 
        required=False,
        label="Optional Text to Display on Menu",
        help_text="Leave blank to use page title."
    )

    class Meta:
        icon = 'doc-empty'
        template = "link_block.html"
        label = _("Link to Internal Page")
        value_class = InternalLinkValue

class ExternalLinkValue(MenuItemValue):
    @property
    def url(self) -> str:
        return self.get("url")

    @property
    def title(self) -> str:
        return self.get("title")

class ExternalLinkBlock(MenuStructBlock):
    url = URLBlock()
    title = CharBlock(
        max_length=255, 
        label="Text to Display on Menu"
    )

    class Meta:
        icon = 'link'
        template = "link_block.html"
        label = _("Link to External URL")
        value_class = ExternalLinkValue

class AutoFillLinkBlock(StructBlock):
    # @TODO - look at autofilling from routable pages
    parent_page = PageChooserBlock()
    include_parent_page = BooleanBlock(
        verbose_name = _("Include Parent Page in Menu"),
        default=False,
        required=False,
        help_text=_("If selected, linked page will included before auto-filled items followed by dividing line")
    )
    only_show_in_menus = BooleanBlock(
        verbose_name = _("Include only 'Show In Menu' pages"),
        default=False,
        required=False,
        help_text=_("If selected, only child pages with 'Show In Menu' selected will be shown.")
    )
    order_by = ChoiceBlock(
        choices=[
            ("-last_published_at", _("Newest (by most recently updated)")),
            ("-first_published_at", _("Newest to Oldest (by date originally published)")),
            ("first_published_at", _("Oldest to Newest")),
            ("title", _("Title (A-Z)")),
        ],
        default="-first_published_at",
        help_text=_("Choose the order in which to take results")
    )
    max_items = IntegerBlock(
        default=4,
        min_value=1,
        blank=False,
        help_text=_("Maximum results to display in the menu")
    )
    display_when = DisplayWhenChoiceBlock(required=False)

    class Meta:
        icon = 'list-ul'
        template = "autolink_block.html"
        label = _("Auto-fill Internal Page Links")

class LinksBlock(StreamBlock):
    internal_link = InternalLinkBlock()
    external_link = ExternalLinkBlock()
    autofill_links = AutoFillLinkBlock()

class SubMenuStructBlock(MenuStructBlock):
    title = CharBlock(
        max_length=255, 
        label="Text to Display on Menu"
    )
    links = LinksBlock()

    class Meta:
        icon = 'folder-open-1'
        template = "submenu.html"
        label = _("Sub Menu")

class MenuStreamBlock(StreamBlock):
    internal_link = InternalLinkBlock()
    external_link = ExternalLinkBlock()
    autofill_links = AutoFillLinkBlock()
    sub_menu = SubMenuStructBlock()

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
        FieldPanel('icon'),
        FieldPanel('items')
    ]

    def __str__(self) -> str:
        return self.title

    @property
    def logo(self):
        return mark_safe(self.icon.svg) if self.icon else ''