from django.contrib import messages
from django.http import HttpResponseRedirect
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.models import Page

from .draftail_extensions import (DRAFTAIL_ICONS, register_block_feature,
                                  register_inline_styling)
from .sitemap import SiteMap
from .thumbnails import ThumbnailOperation
from .utils import has_role, get_custom_icons

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler

@hooks.register('register_rich_text_features')
def register_help_text_feature(features):
    """
    Registering the `help-text` feature, which uses the `help-text` Draft.js block type,
    and is stored as HTML with a `<div class="help-text">` tag.
    """
    feature_name = 'help-text'
    type_ = 'help-text'

    control = {
        'type': type_,
        'icon': ["m 334.22246,308.44491 c 0,-76.23832 61.98413,-138.22245 138.22245,-138.22245 h 69.11123 c 76.23832,0 138.22246,61.98413 138.22246,138.22245 v 7.77502 c 0,47.08202 -23.97296,90.92446 -63.49594,116.19325 l -91.14044,58.52857 c -54.42509,34.98756 -87.25292,95.24391 -87.25292,159.81972 v 3.23958 c 0,38.22715 30.88408,69.11123 69.11123,69.11123 38.22715,0 69.11123,-30.88408 69.11123,-69.11123 v -3.02361 c 0,-17.70975 9.07084,-34.12367 23.75698,-43.62646 L 691.00917,548.8224 C 770.05514,497.85287 818.00105,410.38397 818.00105,316.21993 v -7.77502 C 818.00105,155.75229 694.24876,32 541.55614,32 H 472.44491 C 319.75229,32 196,155.75229 196,308.44491 c 0,38.22715 30.88408,69.11123 69.11123,69.11123 38.22715,0 69.11123,-30.88408 69.11123,-69.11123 z M 507.00053,999.5572 a 86.38904,86.38904 0 1 0 0,-172.77808 86.38904,86.38904 0 1 0 0,172.77808 z"],
        'description': 'Help text',
        # Optionally, we can tell Draftail what element to use when displaying those blocks in the editor.
        'element': 'div',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'div[class=help-text]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'div', 'props': {'class': 'help-text'}}}},
    })

@hooks.register('register_rich_text_features')
def register_align_left_feature(features):
    register_block_feature(
        features=features,
        feature_name='left-align',
        type_='left-align',
        description='Left align text',
        css_class='text-start',
        element='p',
        icon=DRAFTAIL_ICONS.left_align
    )
    
@hooks.register('register_rich_text_features')
def register_align_centre_feature(features):
    register_block_feature(
        features=features,
        feature_name='centre-align',
        type_='centre-align',
        description='Centre align text',
        css_class='text-center',
        element='p',
        icon=DRAFTAIL_ICONS.centre_align
    )
    
@hooks.register('register_rich_text_features')
def register_align_right_feature(features):
    register_block_feature(
        features=features,
        feature_name='right-align',
        type_='right-align',
        description='Right align text',
        css_class='text-end',
        element='p',
        icon=DRAFTAIL_ICONS.right_align
    )
    
@hooks.register('register_rich_text_features')
def register_code_block_feature(features):
    register_block_feature(
        features=features,
        feature_name='code-block',
        type_='CODE-BLOCK',
        description='Code Block',
        css_class='code-block',
        element='div',
        icon=DRAFTAIL_ICONS.code_block
    )
    
@hooks.register('register_rich_text_features')
def register_code_block_feature(features):
    register_block_feature(
        features=features,
        feature_name='code-block',
        type_='CODE-BLOCK',
        description='Code Block',
        css_class='code-block',
        element='div',
        icon=DRAFTAIL_ICONS.code_block
    )
    
@hooks.register("register_rich_text_features")
def register_fa_styling(features):
    """Add <fa> to the richtext editor and page."""
    register_inline_styling(
        features=features,
        feature_name='fa',
        description="Font Awesome Icon",
        type_="FA",
        tag="fa",
        format='style="display:none;"',
        editor_style={            
            'background-color': 'orange',            
            'color': '#666',
            'font-family': 'monospace',
            'font-size': '0.9rem',
            'font-weight': 'bolder',
            'padding': '0 0.4rem',
            'border-radius': '0.6rem'
        },
        icon=DRAFTAIL_ICONS.font_awesome
    )
    
@hooks.register("register_rich_text_features")
def register_small_styling(features):
    register_inline_styling(
        features=features,
        feature_name='small',
        type_='SMALL',
        tag='small',
        description='Small',
        icon=DRAFTAIL_ICONS.decrease_font
    )

@hooks.register("register_rich_text_features")
def register_underline_styling(features):
    register_inline_styling(
        features=features,
        feature_name='underline',
        type_='UNDERLINE',
        tag='u',
        description='Underline',
        icon=DRAFTAIL_ICONS.underline
    )

@hooks.register('register_rich_text_features')
def register_checklist_feature(features):
    register_block_feature(
        features=features,
        feature_name='checklist',
        type_='checklist',
        description='Check List',
        css_class='check-list',
        element='li',
        wrapper="ul class='check-list-wrapper' role='list'",
        icon="tasks"
    )
    
@hooks.register("register_rich_text_features")
def register_codeblock_feature(features):
    register_block_feature(
        features=features,
        feature_name='code-block',
        type_='code-block',
        description='Code Block',
        css_class='code-block',
        element='li',
        wrapper="ul class='code-block-wrapper' role='list'",
        icon=DRAFTAIL_ICONS.code_block
    )

@hooks.register("register_rich_text_features")
def register_quoteblock_feature(features):
    register_block_feature(
        features=features,
        feature_name='quoteblock',
        type_='quoteblock',
        description='Quote Block',
        css_class='quoteblock',
        element='li',
        wrapper="ul class='quoteblock-wrapper' role='list'",
        icon="openquote"
    )

@hooks.register("before_create_page")
@hooks.register("before_delete_page")
@hooks.register("before_edit_page")
def check_page_permissions(request, page, page_class=None):
    page_class = page_class or page.specific_class
    if not issubclass(page_class, Page):
        # kind of redundant - use django-admin groups for this, though this will override those settings
        # careful!, doesn't cover bulk actions, need seperate hook for that
        # this could be adapted to cover a page branch rather than type, not possible via django-admin
        if not has_role(request.user, ['Site Managers','IT Department']):
            page_type = getattr(page_class._meta, 'verbose_name', page_class.__name__)
            messages.error(
                request, 
                f'You do not have permission to add, edit or delete {page_type}s.\
                <br><span style="padding-left:2.3em;">Contact <a href="/lalala">support</a> \
                to report this issue</span>'
            )
            referer = request.META.get('HTTP_REFERER', '/admin/')
            if referer == request.build_absolute_uri():
                referer = '/admin/'
            return HttpResponseRedirect(referer)

@hooks.register('insert_global_admin_js')
def register_admin_js():
    admin_js = static('js/admin.js')
    m2m_chooser_js = static('js/m2m_chooser.js')
    return mark_safe(
        f'<script src="{admin_js}"></script>' +
        f'<script src="{m2m_chooser_js}"></script>'
    )

@hooks.register('insert_global_admin_css')
def register_admin_css():
    admin_css = static('css/admin.css')
    m2m_chooser_css = static('css/m2m_chooser.css')
    return mark_safe(
        f'<link rel="stylesheet" href="{admin_css}">' +
        f'<link rel="stylesheet" href="{m2m_chooser_css}">'
    )

@hooks.register('after_publish_page')
def add_page_sitemap_entry(request, page):
    if page.live and not page.view_restrictions.exists():
        SiteMap().add_page(page)
    else:
        SiteMap().remove_page(page)    

@hooks.register('after_unpublish_page')
@hooks.register('after_delete_page')
def remove_page_sitemap_entry(request, page):
    SiteMap().remove_page(page)    

@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('thumbnail', ThumbnailOperation)
    ]

@hooks.register("register_icons")
def register_icons(icons):
    return icons + get_custom_icons()
    