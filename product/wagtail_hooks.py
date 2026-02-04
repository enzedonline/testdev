# wagtail_hooks.py

from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks

from .views import product_chooser_viewset


@hooks.register('register_admin_viewset')
def register_product_chooser_viewset():
    return product_chooser_viewset

@hooks.register('insert_global_admin_js')
def register_admin_js():
    subcategory_chooser_js = static('js/subcategory_chooser.js')
    return format_html('<script src="{}"></script>', subcategory_chooser_js)

@hooks.register('insert_global_admin_css')
def register_admin_css():
    subcategory_chooser_css = static('css/subcategory_chooser.css')
    return format_html('<link rel="stylesheet" href="{}">', subcategory_chooser_css)

