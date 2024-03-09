from django.utils.functional import cached_property
from wagtail.blocks import CharBlock, PageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

from .base_blocks import ExtendedURLBlock
from product.blocks import ProductChooser


class DataFieldBlockMixin:    
    def __init__(self, *args, attrs={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs = self.field.widget.attrs.update(attrs)

class DataCharBlock(DataFieldBlockMixin, CharBlock):
    pass

class DataExtendedURLBlock(DataFieldBlockMixin, ExtendedURLBlock):
    pass

class DataChooserBlockMixin:
    def __init__(self, *args, attrs={}, chooser_attrs={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs = attrs
        self.chooser_attrs = chooser_attrs

    @cached_property
    def field(self):
        field = super().field
        field.widget.attrs.update(self.attrs)
        return field
        
    @cached_property
    def widget(self):
        chooser = super().widget
        for key, value in self.chooser_attrs.items():
            if hasattr(chooser, key):
                setattr(chooser, key, value)
        return chooser

class DataPageChooserBlock(DataChooserBlockMixin, PageChooserBlock):
    pass

class DataDocumentChooserBlock(DataChooserBlockMixin, DocumentChooserBlock):
    pass

class DataProductChooserBlock(DataChooserBlockMixin, ProductChooser):
    pass
