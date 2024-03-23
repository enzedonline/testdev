from dataclasses import dataclass

from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (BooleanBlock, CharBlock, ChoiceBlock, IntegerBlock,
                            ListBlock, StaticBlock, StreamBlock, StructBlock)
from wagtail.blocks.stream_block import StreamBlockAdapter
from wagtail.telepath import register

from blocks.base_blocks import CustomImageChooserBlock, CustomPageChooserBlock
from blocks.models import LinkBlock


class DisplayWhenChoiceBlock(ChoiceBlock):
    def __init__(self, **kwargs):
        kwargs['default'] = 'ALWAYS'
        kwargs['required'] = True
        kwargs['help_text'] = _(
            "Shown if user logged in, logged out or always")
        super().__init__(**kwargs)

    choices = [
        ('ALWAYS', _("Always")),
        ('True', _("Logged in")),
        ('False', _("Not logged in"))
    ]


@dataclass
class MenuItemOptions:
    icon: bool = True
    display_when: bool = True
    sticky: bool = False


class MenuStructBlock(StructBlock):
    def __init__(self, local_blocks=(), show_options: MenuItemOptions = MenuItemOptions(), _depth=1, **kwargs):
        if type(show_options) != MenuItemOptions:
            raise ImproperlyConfigured(
                "show_options must be declared as MenuItemOptions instance")

        option_blocks = ()
        if show_options.icon:
            option_blocks += (
                ("icon", CustomImageChooserBlock(
                    required=False,
                    chooser_attrs={"show_edit_link": False},
                    form_classname="compact-image-chooser",
                    label=_("Optional menu icon")
                )),
            )
        if show_options.display_when:
            option_blocks += (
                ("display_when", DisplayWhenChoiceBlock(required=True)),
            )
        if show_options.sticky and _depth==1:
            option_blocks += (("sticky", BooleanBlock(
                required=False,
                help_text=_("Item remains on menu bar in mobile view")
            )),
            )
        if option_blocks:
            local_blocks += (
                ("options", StructBlock(
                    option_blocks,
                    form_classname="structblock menu-item-options",
                    label=_(f"{self._meta_class.label} Options")
                )),
            )
        super().__init__(local_blocks, **kwargs)


class MenulLinkBlock(MenuStructBlock):
    link = LinkBlock(
        link_types=['page', 'url_link'],
    )

    class Meta:
        icon = "link"
        label = _("Menu Link")
        template = "menu/menu-link.html"
        label_format = label
        form_classname = "struct-block menu-link-block hide-label"


class AutoPageLinksBlock(MenuStructBlock):
    # @TODO - look at autofilling from routable pages
    title = CharBlock(
        label=_("Submenu Label"),
        max_length=50,
    )
    parent_page = CustomPageChooserBlock(
        label=_("Parent Page"),
        form_classname="autofill-parent-page"
    )
    order_by = ChoiceBlock(
        label=_("Order By"),
        choices=[
            ("-first_published_at", _("Newest to Oldest (by date originally published)")),
            ("first_published_at", _("Oldest to Newest (by date originally published)")),
            ("-last_published_at", _("Newest to Oldest (by date of last update)")),
            ("last_published_at", _("Oldest to Newest (by date of last update)")),
            ("title", _("Title (A-Z)")),
        ],
        default="-first_published_at",
        help_text=_("Choose the order in which to show results")
    )
    include_parent_page = BooleanBlock(
        label=_("Include Parent Page in Submenu"),
        default=False,
        required=False,
        help_text=_(
            "If selected, linked page will included before auto-filled items followed by dividing line")
    )
    only_show_in_menus = BooleanBlock(
        label=_("Only 'Show In Menu' Pages"),
        default=False,
        required=False,
        help_text=_(
            "If selected, only child pages with 'Show In Menu' selected will be shown.")
    )
    max_items = IntegerBlock(
        label=_("Maximum Items"),
        default=4,
        min_value=1,
        blank=False,
        help_text=_("Maximum number of results to display in the menu")
    )

    class Meta:
        icon = 'list-ul'
        template = "menu/auto-page-links-submenu.html"
        label = _("Auto Page Links Submenu")
        label_format = label + ": {title} ({parent_page})"
        form_classname = "struct-block auto-page-links-block"

class SubMenuDividerBlock(StaticBlock):
    class Meta:
        label = _("Divider")
        admin_text = _("Inserts a horizontal line in the submenu.")
        icon = 'minus'
        template = "menu/submenu-divider.html"

class RecursiveSubMenuBlock(MenuStructBlock):
    def __init__(
            self, 
            local_blocks=(), 
            max_depth=3, 
            _depth=0, 
            *args, 
            **kwargs
        ):
        _depth += 1
        if _depth <= max_depth:
            streamblocks = (
                ("sub_menu", RecursiveSubMenuBlock(local_blocks, max_depth, _depth, *args, **kwargs)),
                ("autofill_submenu", AutoPageLinksBlock()),
             ) if _depth < max_depth else ()
            streamblocks += (
                ("link", MenulLinkBlock(link_types=['page', 'url_link'])),
                ("divider", SubMenuDividerBlock())
            )
            local_blocks += (
                ("title", CharBlock(max_length=50, label=_("Submenu Display Title"))),
                ("items", StreamBlock(streamblocks)),
                *local_blocks
            )
        super().__init__(local_blocks, _depth=_depth, *args, **kwargs)

    class Meta:
        icon = 'folder-open-1'
        template = "menu/submenu.html"
        label = _("Sub Menu")
        label_format = label + ": {title}"
        form_classname = "struct-block sub-menu-block"


class SearchMenuBlock(MenuStructBlock):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    title = CharBlock(
        label = _("Menu label"),
        max_length=20,
    )

    class Meta:
        icon = 'search'
        template = "menu/search.html"
        label = _("Search Form")
        label_format = label


class UserMenuBlock(MenuStructBlock):
    def __init__(self, show_options=MenuItemOptions(icon=False, display_when=False), **kwargs):
        show_options.icon = False
        show_options.display_when = False
        super().__init__(show_options=show_options, **kwargs)

    logged_in_title = CharBlock(
        max_length=50,
        help_text=_("Menu title when user is logged in.")
    )
    logged_in_icon = CustomImageChooserBlock(
        required=False,
        chooser_attrs={"show_edit_link": False},
        form_classname="compact-image-chooser",
        label=_("Optional icon when logged in")
    )
    logged_in_text = CharBlock(
        max_length=150,
        required=False,
        help_text=_(
            "Message to display to logged in users. \
             Use @username or @display_name to display those values inline.")
    )
    logged_out_title = CharBlock(
        max_length=50,
        help_text=_("Menu title when user is not logged in.")
    )
    logged_out_icon = CustomImageChooserBlock(
        required=False,
        chooser_attrs={"show_edit_link": False},
        form_classname="compact-image-chooser",
        label=_("Optional icon when logged out")
    )
    items = ListBlock(MenulLinkBlock(), label=_("User Menu Links"))

    class Meta:
        icon = 'user'
        template = "menu/user.html"
        label = _("User Menu")
        label_format = label
        form_classname = "struct-block user-menu-block"


class MenuStreamBlock(StreamBlock):
    submenu = RecursiveSubMenuBlock(show_options=MenuItemOptions(sticky=True))
    autofill_menu = AutoPageLinksBlock(show_options=MenuItemOptions(sticky=True))
    link = MenulLinkBlock(show_options=MenuItemOptions(sticky=True))
    search_form = SearchMenuBlock(show_options=MenuItemOptions(sticky=True))
    user_menu = UserMenuBlock(show_options=MenuItemOptions(sticky=True))

    class Meta:
        form_classname = "menustreamblock"
        block_counts = {
            'search_form': {'min_num': 0, 'max_num': 1},
            'user_menu': {'min_num': 0, 'max_num': 1},
        }


class MenuStreamBlockAdapter(StreamBlockAdapter):
    @cached_property
    def media(self):
        return forms.Media(
            css={"all": ("css/admin/menustream.css",)},
        )


register(MenuStreamBlockAdapter(), MenuStreamBlock)
