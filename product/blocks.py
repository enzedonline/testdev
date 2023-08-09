from .views import product_chooser_viewset

ProductChooserBlock = product_chooser_viewset.get_block_class(
    name="ProductChooserBlock", module_path="product.blocks",
)
