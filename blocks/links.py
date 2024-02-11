import logging
import re

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.forms import RadioSelect
from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (CharBlock, ChoiceBlock, PageChooserBlock,
                            StructBlock, StructValue)
from wagtail.blocks.struct_block import (StructBlockAdapter,
                                         StructBlockValidationError)
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.telepath import register

from blocks.wagtail.blocks import URLBlock, RequiredMixin


class LinkTypeChoiceBlock(ChoiceBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(widget=RadioSelect, *args, **kwargs)
    
    choices=[
        ('page', _('Page Link')),
        ('url', _('URL Link')),
        ('document', _('Document Link')),
    ]

class Link_Value(StructValue):
    def url(self) -> str:
        """Return a link's url regardless of link type"""
        try:
            match self.get("link_type"):
                case 'page':
                    internal_page = self.get("internal_page")
                    i18n_enabled = getattr(settings, "WAGTAIL_I18N_ENABLED", False)
                    url = internal_page.localized.url if i18n_enabled else internal_page.url
                    return url + self.get("anchor_target")
                case 'url':
                    # if needing to localise routable page relative urls, use template tag
                    # requires active site (get from request)
                    return self.get("url_link")
                case 'document':
                    return self.get("document").url
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
                        internal_page = self.get("internal_page")
                        i18n_enabled = getattr(settings, "WAGTAIL_I18N_ENABLED", False)
                        return internal_page.localized.title if i18n_enabled else internal_page.title
                    case 'document':
                        return self.get("document").title
            except Exception as e:
                logging.error(
                    f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
                )
            return ''        
    
class LinkBlock(RequiredMixin, StructBlock):

    def __init__(
            self, 
            link_types=['page', 'url', 'document'], 
            url_link_text_required=True,
            no_link_label = _("No Link"),
            no_link_description = _("No link selected."),
            **kwargs
        ):
        super().__init__(**kwargs)
        self.link_types = link_types
        self.no_link_label = no_link_label
        self.url_link_text_required = url_link_text_required
        self.no_link_description = no_link_description
        if getattr(settings, 'DEBUG', False): self.validate_link_types()
        
    link_type = LinkTypeChoiceBlock(required=False, label='')
    internal_page = PageChooserBlock(required=False, label=_("Link to internal page"))
    anchor_target = CharBlock(
        required=False, 
        label=_("Optional anchor target"), 
        help_text=_("Anchor target must start with '#' followed by alphanumeric characters, hyphens and underscores.")
    )
    url_link = URLBlock(
        required=False, label=_("Link to external site or internal URL")
    )
    document = DocumentChooserBlock(required=False, label=_("Link to document"))
    link_text = CharBlock(required=False, label=_("Link text"))

    class Meta:
        template = 'blocks/link_block.html'
        value_class = Link_Value
        icon = "link"
        form_classname = "link-block"

    def clean(self, value):
        errors = {}
        link_type = value.get("link_type")
        match link_type:
            case 'page':
                internal_page = value.get('internal_page')
                anchor_target = value.get('anchor_target')
                if not internal_page:
                    errors['internal_page'] = ErrorList([_("Please select a page to link to")])
                if anchor_target:
                    # add '#' if missing, validate format
                    if not anchor_target.startswith("#"):
                        anchor_target = f"#{anchor_target}"
                        value['anchor_target'] = anchor_target
                    if not re.match(r'^#[\w\-.]+$', anchor_target):
                        errors['anchor_target'] = ErrorList([_("Please select a valid anchor target")])
            case 'url':
                url_link = value.get('url_link')
                if not url_link:
                    errors['url_link'] = ErrorList([_("Please enter a URL to link to")])
                if self.url_link_text_required and not value.get('link_text'):
                    errors['link_text'] = ErrorList([_("Please enter a display text for the link")])
            case 'document':
                url_link = value.get('document')
                if not url_link:
                    errors['document'] = ErrorList([_("Please enter a URL to link to")])
            case _:
                if self.required:
                    errors['link_type'] = ErrorList([_("Please select a link type and value")])
        if errors:
            raise StructBlockValidationError(block_errors=errors)

        return super().clean(value)

    def validate_link_types(self):
        if not isinstance(self.link_types, list):
            raise ImproperlyConfigured("link_types must be a list")
        if not any(link_type in self.link_types for link_type in ['page', 'url', 'document']):
            raise ImproperlyConfigured("link_types must contain at least one of 'page', 'url', or 'document'")
        if any(link_type not in ['page', 'url', 'document'] for link_type in self.link_types):
            raise ImproperlyConfigured("link_types must only contain elements 'page', 'url', or 'document'")

class LinkBlockAdapter(StructBlockAdapter):
    js_constructor = "blocks.models.LinkBlock"

    def js_args(self, block):
        args = super().js_args(block)
        # link types to display as tabs
        # passed to LinkBlock as parameter: link_types=['page', 'url', 'document']
        args[2]['link_types'] = block.link_types
        # tab label and description for the empty value option
        args[2]['no_link_label'] = block.no_link_label
        args[2]['no_link_description'] = block.no_link_description
        args[2]['url_link_text_required'] = block.url_link_text_required
        return args

    @cached_property
    def media(self):
        from django import forms
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/link-block.js"],
            css={"all": ("css/link-block.css",)},
        )


register(LinkBlockAdapter(), LinkBlock)
