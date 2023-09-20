from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (BooleanBlock, CharBlock, IntegerBlock,
                            PageChooserBlock, StreamBlock, StructBlock,
                            StructValue, URLBlock)
from wagtail.images.blocks import ImageChooserBlock
from blocks.wagtail import ChoiceBlock

class DisplayWhenChoiceBlock(ChoiceBlock):        
    choices=[
        ('ALWAYS', _("Always")),
        ('True', _("When logged in")),
        ('False', _("When not logged in"))
    ]
    default='ALWAYS'
    help_text=_("Determines if menu item is only shown if user logged in, logged out or always")

class MenuStructBlock(StructBlock):
    icon = ImageChooserBlock(
        required=False,
        label=_("Optional image for display")
    )
    display_when = DisplayWhenChoiceBlock(required=False)

class InternalLinkValue(StructValue):
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
        icon = 'doc-empty'
        template = "menu/link_block.html"
        label = _("Link to Internal Page")
        value_class = InternalLinkValue

class ExternalLinkValue(StructValue):
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
        template = "menu/link_block.html"
        label = _("Link to External URL")
        value_class = ExternalLinkValue

class AutoFillMenuBlock(MenuStructBlock):
    # @TODO - look at autofilling from routable pages
    title = CharBlock(
        max_length=255, 
        label="Text to Display on Menu"
    )
    parent_page = PageChooserBlock()
    include_parent_page = BooleanBlock(
        verbose_name = _("Include Parent Page in Sub-Menu"),
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
        help_text=_("Choose the order in which to show results")
    )
    max_items = IntegerBlock(
        default=4,
        min_value=1,
        blank=False,
        help_text=_("Maximum results to display in the menu")
    )

    class Meta:
        icon = 'list-ul'
        template = "menu/autolink_menu.html"
        label = _("Auto-fill Page Links Sub-Menu")

class AutoFillSubmenuBlock(AutoFillMenuBlock):
    open_direction = ChoiceBlock(
        choices=[
            ("end", _("Open items to the right")),
            ("start", _("Open items to the left")),
        ],
        default="start",
        help_text=_("Choose submenu direction.")
    )

    class Meta:
        template = "menu/autolink_submenu.html"

class LinksBlock(StreamBlock):
    internal_link = InternalLinkBlock()
    external_link = ExternalLinkBlock()
    autofill_submenu = AutoFillSubmenuBlock()

class SubMenuBlock(MenuStructBlock):
    title = CharBlock(
        max_length=255, 
        label=_("Text to Display on Menu")
    )
    links = LinksBlock()

    class Meta:
        icon = 'folder-open-1'
        template = "menu/submenu.html"
        label = _("Sub Menu")

class MenuStreamBlock(StreamBlock):
    internal_link = InternalLinkBlock()
    external_link = ExternalLinkBlock()
    autofill_menu = AutoFillMenuBlock()
    sub_menu = SubMenuBlock()
