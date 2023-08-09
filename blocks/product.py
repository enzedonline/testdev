from product.blocks import ProductChooserBlock
from wagtail.blocks import StructBlock

class ProductBlock(StructBlock):
    product = ProductChooserBlock()
    