from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (BooleanBlock, CharBlock, ChoiceBlock, IntegerBlock,
                            PageChooserBlock, StreamBlock, StructBlock,
                            StructValue, URLBlock)

from svg.chooser.block import SVGChooserBlock

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
        image = self.get("image")
        return mark_safe(image.svg) if image else ''
    
class MenuStructBlock(StructBlock):
    image = SVGChooserBlock(
        required=False,
        label=_("Optional image for display")
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
        return display_title or page.localized.title
    
class InternalLinkBlock(MenuStructBlock):
    page = PageChooserBlock()
    display_title = CharBlock(
        max_length=255, 
        required=False,
        label="Optional Text to Display on Menu",
        help_text="Leave blank to use page title."
    )

    class Meta:
        image = 'doc-empty'
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
        image = 'link'
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
        image = 'list-ul'
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
        image = 'folder-open-1'
        template = "submenu.html"
        label = _("Sub Menu")

class MenuStreamBlock(StreamBlock):
    internal_link = InternalLinkBlock()
    external_link = ExternalLinkBlock()
    autofill_links = AutoFillLinkBlock()
    sub_menu = SubMenuStructBlock()

