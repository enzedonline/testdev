# wagtail_hooks.py

from wagtail import hooks
from .views import product_chooser_viewset

@hooks.register('register_admin_viewset')
def register_product_chooser_viewset():
    return product_chooser_viewset