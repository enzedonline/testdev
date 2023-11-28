from wagtail.blocks import StructBlock

class ProductBlock(StructBlock):
    from product.blocks import ProductChooserBlock
    product = ProductChooserBlock()
    