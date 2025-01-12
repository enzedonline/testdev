import logging
import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.forms import RadioSelect
from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (CharBlock, ChoiceBlock, StaticBlock, StructBlock,
                            StructValue)
from wagtail.blocks.struct_block import (StructBlockAdapter,
                                         StructBlockValidationError)
from wagtail.telepath import register

from blocks.data_blocks import (DataCharBlock, DataDocumentChooserBlock,
                                DataExtendedURLBlock, DataPageChooserBlock, DataProductChooserBlock)


class LinkTypeChoiceBlock(ChoiceBlock):
    """
    Choice block of link types - 
    link_types - the link types to offer as a choice, defaults ['page', 'url_link', 'document'], must be a subset of the default
    unselected_label - the label to use on the no value choice in the case of required=False
    default - the link_type value to set as default. If required and no default set, default will be first item in link_types
    """
    valid_link_types = ['page', 'url_link', 'document', 'product']

    def __init__(self, link_types=valid_link_types, unselected_label=_("No Link"), required=True, default=None, *args, **kwargs):
        if getattr(settings, 'DEBUG', False):
            self.validate_link_types(link_types, default)
        # Build choice list from link_types parameter
        choices = [(key, value) for key, value in [
            ('page', _('Page Link')),
            ('url_link', _('URL Link')),
            ('document', _('Document Link')),
            ('product', _('Product Link')),
        ] if key in link_types]
        if required and not default:
            # set default if required and no default supplied (no default will cause 'not selected' to be rendered)
            default = choices[0][0]
        elif not required:
            # relabel 'not selected' button (default is '---------')
            choices.insert(0, (None, unselected_label))
        super().__init__(choices=choices, required=required,
                         default=default, widget=RadioSelect(), *args, **kwargs)

    def validate_link_types(self, link_types, default):
        if not isinstance(link_types, list):
            raise ImproperlyConfigured("link_types must be a list")
        if not any(link_type in link_types for link_type in self.valid_link_types):
            raise ImproperlyConfigured(
                f"link_types must contain at least one of {', '.join(self.valid_link_types)}")
        if any(link_type not in self.valid_link_types for link_type in link_types):
            raise ImproperlyConfigured(
                f"link_types must only contain the following elements: {', '.join(self.valid_link_types)}")
        if default and default not in link_types:
            raise ImproperlyConfigured(
                f"Default value '{default}' not found in requested link types ({', '.join(link_types)})")


class LinkValue(StructValue):
    """
    Return url and link text for all link types
    """
    i18n_enabled = getattr(settings, "WAGTAIL_I18N_ENABLED", False)

    def url(self) -> str:
        """Return a link's url regardless of link type"""
        try:
            match self.get("link_type"):
                case 'page':
                    internal_page = self.get("page")

                    url = internal_page.localized.url if self.i18n_enabled else internal_page.url
                    return url + self.get("anchor_target")
                case 'url_link':
                    # if needing to localise routable page relative urls, use template tag
                    # requires active site (get from request)
                    return self.get("url_link")
                case 'document':
                    return self.get("document").url
                case 'product':
                    from product.models import Product, ProductPage
                    base_page = ProductPage.objects.first()
                    sku = self.get('product').sku
                    product = Product.objects.filter(sku=sku).first()
                    if product and base_page:
                        if self.i18n_enabled:
                            product = product.localized
                            base_page = base_page.localized
                        product_url_part = base_page.reverse_subpage(
                            name='product_detail', kwargs={'sku': product.sku})
                        return f"{base_page.url}{product_url_part}"
                    return ''
        except Exception as e:
            logging.error(
                f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
            )
        return None

    def text(self) -> str:
        """Return link text - default to object title for page and document links"""
        link_text = self.get("link_text")
        if link_text:
            return link_text
        else:
            try:
                match self.get("link_type"):
                    case 'page':
                        internal_page = self.get("page")
                        return internal_page.localized.title if self.i18n_enabled else internal_page.title
                    case 'url_link':
                        return self.get("url_link")
                    case 'document':
                        return self.get("document").title
                    case 'product':
                        return self.get("product").title
            except Exception as e:
                logging.error(
                    f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
                )
            return ''


class LinkBlock(StructBlock):
    def __init__(
        self,
        required=True,
        link_types=LinkTypeChoiceBlock.valid_link_types,
        default_link_type=None,
        url_link_text_required=True,
        _unselected_label=_("No Link"),
        _unselected_description=_("No link selected."),
        **kwargs
    ):
        local_blocks = (
            ('link_type', LinkTypeChoiceBlock(
                required=required,
                label=_("Link Type"),
                link_types=link_types,
                default=default_link_type,
                unselected_label=_unselected_label
            )),
        )
        if not required:
            local_blocks += (
                ('not_selected', StaticBlock(
                    label=_unselected_description,
                    admin_text="",
                )),
            )
        if 'page' in link_types:
            local_blocks += (
                ('page', DataPageChooserBlock(
                    required=False,
                    label=_("Link to internal page"),
                    attrs={'data-link-block-type': 'page'},
                    chooser_attrs={'show_edit_link': False}
                )),
                ('anchor_target', DataCharBlock(
                    required=False,
                    label=_("Optional anchor target (#)"),
                    attrs={'data-link-block-type': 'page'}
                )),
            )
        if 'url_link' in link_types:
            local_blocks += (
                ('url_link', DataExtendedURLBlock(
                    required=False,
                    label=_("Link to external site or internal URL"),
                    attrs={'data-link-block-type': 'url_link'}
                )),
            )
        if 'document' in link_types:
            local_blocks += (
                ('document', DataDocumentChooserBlock(
                    required=False,
                    label=_("Link to document"),
                    attrs={'data-link-block-type': 'document'},
                    chooser_attrs={'show_edit_link': False}
                )),
            )
        if 'product' in link_types:
            local_blocks += (
                ('product', DataProductChooserBlock(
                    required=False,
                    label=_("Link to product"),
                    attrs={'data-link-block-type': 'product'},
                    chooser_attrs={'show_edit_link': False}
                )),
            )
        local_blocks += (
            ('link_text', CharBlock(
                required=False,
                label=_("Link text"),
            )),
        )
        super().__init__(local_blocks, **kwargs)
        self._required = required
        self.link_types = link_types
        self.url_link_text_required = url_link_text_required
        self.no_link_label = _unselected_label
        self.no_link_description = _unselected_description

    class Meta:
        template = 'blocks/link_block.html'
        value_class = LinkValue
        icon = "link"
        form_classname = "struct-block link-block"
        label_format = _("Link")

    def clean(self, value):
        errors = {}
        selected_link_type = value.get("link_type")
        match selected_link_type:
            case 'page':
                internal_page = value.get('page')
                anchor_target = value.get('anchor_target')
                if not internal_page:
                    errors['page'] = ErrorList(
                        [_("Please select a page to link to")])
                if anchor_target:
                    # add '#' if missing, validate format
                    if not anchor_target.startswith("#"):
                        anchor_target = f"#{anchor_target}"
                        value['anchor_target'] = anchor_target
                    if not re.match(r'^#[\w\-.]+$', anchor_target):
                        errors['anchor_target'] = ErrorList(
                            [_("Anchor target must start with '#' followed by alphanumeric \
                                characters, hyphens and underscores.")])
            case 'url_link':
                url_link = value.get('url_link')
                if not url_link:
                    errors['url_link'] = ErrorList(
                        [_("Please enter a URL")])
                if self.url_link_text_required and not value.get('link_text'):
                    errors['link_text'] = ErrorList(
                        [_("Please enter a display text for the link")])
            case 'document':
                document = value.get('document')
                if not document:
                    errors['document'] = ErrorList(
                        [_("Please select a document to link to")])
            case 'product':
                document = value.get('product')
                if not document:
                    errors['product'] = ErrorList(
                        [_("Please select a product to link to")])
            case _:
                if self._required:
                    errors['link_type'] = ErrorList(
                        [_("Please select a link type and value")])
        if errors:
            raise StructBlockValidationError(block_errors=errors)

        # block validated - remove any link values for non-selected link types
        for link_type in self.link_types:
            if link_type != selected_link_type:
                value[link_type] = None
        if selected_link_type != 'page':
            value['anchor_target'] = None

        return super().clean(value)


class LinkBlockAdapter(StructBlockAdapter):
    js_constructor = "blocks.links.LinkBlock"

    def js_args(self, block):
        # keys added to args[2] found in this.meta in StructBlockDefinition
        args = super().js_args(block)
        # link types configured in LinkBlock class instance
        args[2]['link_types'] = block.link_types
        # add required '*' to link_text if url link selected and url_link_text_required==True
        args[2]['url_link_text_required'] = block.url_link_text_required
        return args

    @cached_property
    def media(self):
        from django import forms
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/link-block.js"],
            css={"all": ("css/admin/link-block.css",)},
        )


register(LinkBlockAdapter(), LinkBlock)
