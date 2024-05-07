from django.utils.translation import gettext_lazy as _
from wagtail.blocks import RawHTMLBlock, StructBlock

class DjangoTemplateFragmentBlock(StructBlock):
    code = RawHTMLBlock(
        label=_("Enter Django Template Fragment Code")
    )
    class Meta:
        template='blocks/django_code_block.html'
        icon = 'laptop-code'
        label = _("Django Fragment")
        label_format = label