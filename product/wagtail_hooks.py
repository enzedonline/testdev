# wagtail_hooks.py

from django.templatetags.static import static
from django.utils.safestring import mark_safe
from wagtail import hooks

from .views import product_chooser_viewset


@hooks.register('register_admin_viewset')
def register_product_chooser_viewset():
    return product_chooser_viewset

@hooks.register('insert_global_admin_js')
def register_admin_js():
    product_category_chooser_js = static('js/product_category_chooser.js')
    return mark_safe(
        f'<script src="{product_category_chooser_js}"></script>'
    )

@hooks.register('insert_global_admin_css')
def register_admin_css():
    product_category_chooser_css = static('css/product_category_chooser.css')
    return mark_safe(
        f'<link rel="stylesheet" href="{product_category_chooser_css}">'
    )
