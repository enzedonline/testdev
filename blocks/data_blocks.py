from django.utils.functional import cached_property
from wagtail.blocks import CharBlock, PageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

from .base_blocks import ExtendedURLBlock, CustomChooserMixin
from product.blocks import ProductChooserBlock


class DataFieldBlockMixin:    
    def __init__(self, *args, attrs={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs = self.field.widget.attrs.update(attrs)

class DataCharBlock(DataFieldBlockMixin, CharBlock):
    pass

class DataExtendedURLBlock(DataFieldBlockMixin, ExtendedURLBlock):
    pass

class DataChooserBlockMixin(CustomChooserMixin):
    def __init__(self, *args, attrs={}, chooser_attrs={}, **kwargs):
        super().__init__(chooser_attrs=chooser_attrs, *args, **kwargs)
        self.attrs = attrs

    @cached_property
    def field(self):
        field = super().field
        field.widget.attrs.update(self.attrs)
        return field

class DataPageChooserBlock(DataChooserBlockMixin, PageChooserBlock):
    pass

class DataDocumentChooserBlock(DataChooserBlockMixin, DocumentChooserBlock):
    pass

class DataProductChooserBlock(DataChooserBlockMixin, ProductChooserBlock):
    pass
