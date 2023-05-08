from django.contrib import messages
from django.http import HttpResponseRedirect
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.models import Page

from .draftail_extensions import (DRAFTAIL_ICONS, register_block_feature,
                                  register_inline_styling)
from .utils import has_role


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

@hooks.register('insert_editor_js')
def register_admin_js():
    admin_js = static('js/admin.js')
    import_text_field_panel_js = static('js/import_text_field_panel.js')
    return mark_safe(
        f'<script src="{admin_js}"></script>' +
        f'<script src="{import_text_field_panel_js}"></script>'
    )
