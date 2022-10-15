from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import \
    InlineStyleElementHandler
from wagtail.admin.rich_text.editors.draftail.features import \
    InlineStyleFeature

from .draftail_extensions import (CENTRE_ALIGN_ICON, LEFT_ALIGN_ICON,
                                  MINIMISE_ICON, RIGHT_ALIGN_ICON, UNDERLINE_ICON,
                                  register_block_feature,
                                  register_inline_styling)
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler

@hooks.register('register_rich_text_features')
def register_align_left_feature(features):
    register_block_feature(
        features=features,
        feature_name='left-align',
        type_='left-align',
        description='Left align text',
        css_class='text-start',
        element='p',
        icon=LEFT_ALIGN_ICON
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
        icon=CENTRE_ALIGN_ICON
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
        icon=RIGHT_ALIGN_ICON
    )
    
@hooks.register("register_rich_text_features")
def register_fa_styling(features):
    """Add <fa> to the richtext editor and page."""

    feature_name = "fa"
    type_ = "FA"
    tag = "fa"

    control = {
        "type": type_,
        "label": "⚐",
        "description": "Font Awesome",
        'style': {            
            'background-color': 'orange',            
            'color': '#666',
            'font-family': 'monospace',
            'font-size': '0.9rem',
            'font-weight': 'bolder',
            'padding-left': '2px',
            'padding-right': '4px'
        }    
    }

    features.register_editor_plugin(
        "draftail", feature_name, InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: {"element": tag + ' style="display:none;"'}}}
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)

@hooks.register("register_rich_text_features")
def register_small_styling(features):
    register_inline_styling(
        features=features,
        feature_name='small',
        type_='SMALL',
        tag='small',
        description='Small',
        icon=MINIMISE_ICON
    )

@hooks.register("register_rich_text_features")
def register_underline_styling(features):
    register_inline_styling(
        features=features,
        feature_name='underline',
        type_='UNDERLINE',
        tag='u',
        description='Underline',
        icon=UNDERLINE_ICON
    )


