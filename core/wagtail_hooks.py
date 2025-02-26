import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.templatetags.static import static
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail.admin.rich_text.converters.html_to_contentstate import \
    BlockElementHandler
from wagtail.models import Page

from wagtail import hooks

from .documents.views.chooser import viewset as document_chooser_viewset
from .draftail_extensions import (register_block_feature,
                                  register_inline_styling)
from .images.image_operations import ThumbnailOperation
from .reports.unpublished_changes import UnpublishedChangesReportView
from .sitemap import SiteMap
from .utils import get_custom_icons, has_role


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
        'icon': 'question-mark',
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
        icon='left-align'
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
        icon='centre-align'
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
        icon='right-align'
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
        icon='code'
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
        icon='font-awesome'
    )


@hooks.register("register_rich_text_features")
def register_small_styling(features):
    register_inline_styling(
        features=features,
        feature_name='small',
        type_='SMALL',
        tag='small',
        description='Small',
        icon='decrease-font'
    )


@hooks.register("register_rich_text_features")
def register_underline_styling(features):
    register_inline_styling(
        features=features,
        feature_name='underline',
        type_='UNDERLINE',
        tag='u',
        description='Underline',
        icon='underline'
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
        icon='code-block'
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
        if not has_role(request.user, ['Site Managers', 'IT Department']):
            page_type = getattr(
                page_class._meta, 'verbose_name', page_class.__name__)
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


@hooks.register("register_admin_viewset")
def register_document_chooser_viewset():
    return document_chooser_viewset


@hooks.register('register_reports_menu_item')
def register_unpublished_changes_report_menu_item():
    return AdminOnlyMenuItem("Pages with unpublished changes", reverse('unpublished_changes_report'), icon_name=UnpublishedChangesReportView.header_icon, order=700)


@hooks.register('register_admin_urls')
def register_unpublished_changes_report_url():
    return [
        path('reports/unpublished-changes/', UnpublishedChangesReportView.as_view(),
             name='unpublished_changes_report'),
        path('reports/unpublished-changes/results/', UnpublishedChangesReportView.as_view(
            results_only=True), name='unpublished_changes_report_results'),
    ]
