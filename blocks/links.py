from django import forms
from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (CharBlock, PageChooserBlock, 
                            StructValue)
from wagtail.blocks.struct_block import (StructBlockAdapter, StructBlock,
                                         StructBlockValidationError)
from wagtail.models import Locale
from wagtail.telepath import register
from django.conf import settings
from wagtail.documents.blocks import DocumentChooserBlock

from .choices import LinkTypeChoiceBlock
from blocks.wagtail.blocks import URLBlock, RequiredMixin


class Link_Value(StructValue):
    """Additional logic for the Link class"""

    def url(self) -> str:
        i18n_enabled = getattr(settings, "WAGTAIL_I18N_ENABLED", False)
        link_type = self.get("link_type")
        if link_type == 'page':
            internal_page = self.get("internal_page")
            if internal_page:
                url = internal_page.localized.url if i18n_enabled else internal_page.url
                anchor_target = self.get("anchor_target")
                if anchor_target:
                    url += anchor_target if anchor_target[:1] == "#" else f'#{anchor_target}'
                return url
        else:
            url_link = self.get("url_link")
            if url_link:
                if i18n_enabled and url_link.startswith("/"):
                    url_link = f"/{Locale.get_active().language_code}" + url_link
                return url_link
        return None
    
class LinkBlock(RequiredMixin, StructBlock):
    def __init__(self, link_types=['page', 'url', 'document'], **kwargs):
        super().__init__(**kwargs)
        self.link_types = link_types
        if kwargs:
            self.declared_blocks['link_type'].required = kwargs.get('required', True)
        
    link_type = LinkTypeChoiceBlock(label='')
    internal_page = PageChooserBlock(required=False, label=_("Link to internal page"))
    anchor_target = CharBlock(required=False, label=_("Optional anchor target"))
    url_link = URLBlock(
        required=False, label=_("Link to external site or internal URL")
    )
    document = DocumentChooserBlock(required=False, label=_("Link to document"))
    link_label = CharBlock(required=False, label=_("Optional link label"))

    class Meta:
        value_class = Link_Value
        icon = "link"
        form_classname = "link-block"
        # template = "blocks/link_button.html"


    def clean(self, value):
        errors = {}
        match value.get("link_type"):
            case 'page':
                internal_page = value.get('internal_page')
                if not internal_page:
                    errors['internal_page'] = ErrorList([_("Please select a page to link to")])
            case 'url':
                url_link = value.get('url_link')
                if not url_link:
                    errors['url_link'] = ErrorList([_("Please enter a URL to link to")])
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

class LinkBlockAdapter(StructBlockAdapter):
    js_constructor = "blocks.models.LinkBlock"

    def js_args(self, block):
        args = super().js_args(block)
        # link types to display as tabs
        # passed to LinkBlock as parameter: link_types=['page', 'url', 'document']
        args[2]['link_types'] = block.link_types
        # tab label and description for the empty value option
        args[2]['no_link_label'] = _("No Link")
        args[2]['no_link_description'] = _("No link selected.")
        return args

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/link-block.js"],
            css={"all": ("css/link-block.css",)},
        )


register(LinkBlockAdapter(), LinkBlock)
