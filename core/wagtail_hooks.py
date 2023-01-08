
from django.utils.translation import gettext_lazy as _
from wagtail import hooks

from .draftail_extensions import (DRAFTAIL_ICONS,
                                  register_block_feature,
                                  register_inline_styling)

import wagtail.admin.rich_text.editors.draftail.features as draftail_features

from wagtail.admin.rich_text.converters.html_to_contentstate import (
    ListElementHandler, ListItemElementHandler, BlockElementHandler)

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
    

# @hooks.register("register_rich_text_features")
# def register_checklist_feature(features):
#     feature_name = "checklist"
#     type_ = "checklist"

#     control = {
#         "type": type_,
#         "icon": "tasks",
#         "description": "Check List",
#     }

#     features.register_editor_plugin(
#         "draftail",
#         feature_name,
#         draftail_features.BlockFeature(control),
#     )

#     db_conversion = {
#         "from_database_format":  {
#             "ul[class='check-list-wrapper']": ListElementHandler(type_),
#             "li[class='check-list']": ListItemElementHandler(),
#         },
#         "to_database_format": {
#             "block_map": {
#                 type_: {
#                     "element": "li",
#                     "wrapper": "ul class='check-list-wrapper' role='list'",
#                     "props": {
#                         "class": "check-list"
#                     }
#                 }
#             },
#         }
#     }

#     features.register_converter_rule("contentstate", feature_name, db_conversion)


@hooks.register("register_rich_text_features")
def register_codeblock_feature(features):
    feature_name = "codeblock"
    type_ = "codeblock"

    control = {
        "type": type_,
        "icon": "code",
        "description": "Code Block",
    }

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.BlockFeature(control),
    )

    db_conversion = {
        "from_database_format":  {
            "li[class='code-block']": BlockElementHandler(type_),
        },
        "to_database_format": {
            "block_map": {
                type_: {
                    "element": "li",
                    "wrapper": "ul class='code-block-wrapper'",
                    "props": {
                        "class": "code-block"
                    }
                }
            },
        }
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
