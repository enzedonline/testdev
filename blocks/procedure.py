from typing import Final

import unidecode
import validators
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (BooleanBlock, CharBlock, ChoiceBlock, ListBlock,
                            RichTextBlock, StreamBlock, StructBlock,
                            StructValue)
from wagtail.blocks.struct_block import (StructBlockAdapter,
                                         StructBlockValidationError)
from wagtail.images.blocks import ImageBlock
from wagtail.telepath import register

from blocks.video import InlineVideoBlock


class HeadingSizeChoiceBlock(ChoiceBlock):
    """
    A ChoiceBlock subclass for selecting HTML heading sizes within a specified range.
    Attributes:
        default_choices (list): List of available heading size choices as (value, label) tuples.
    Args:
        heading_range (tuple, optional): A tuple specifying the start and end heading tags (inclusive) to be included as choices. Defaults to ('h2', 'h4').
        default (str, optional): The default selected heading size. Defaults to None.
        required (bool, optional): Whether selection is required. Defaults to True.
        **kwargs: Additional keyword arguments passed to the parent ChoiceBlock.
    Example:
        block = HeadingSizeChoiceBlock(heading_range=('h3', 'h5'))
        # Choices will be: [('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5')]
    """
    default_choices = [
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5'),
        ('h6', 'H6'),
    ]

    def __init__(self, heading_range: tuple = ('h2', 'h4'), default=None, required=True, **kwargs):
        # Find the indices of the elements in heading_range within default_choices
        start_index = next((i for i, (value, _) in enumerate(
            self.default_choices) if value == heading_range[0]), None)
        end_index = next((i for i, (value, _) in enumerate(
            self.default_choices) if value == heading_range[1]), None)
        # Filter default_choices based on the indices
        choices = self.default_choices[start_index:end_index + 1]
        super().__init__(choices, default, required, **kwargs)


class ListItemStreamBlock(StreamBlock):
    """
    Blocks common to all levels of list items
    """
    rich_text = RichTextBlock(editor='procedure', features=None)
    image = ImageBlock()
    video = InlineVideoBlock()


class ProcedureListItemBlock(StructBlock):
    """
    A recursive Wagtail StructBlock for representing a list item in a procedure, supporting nested list items up to a specified maximum depth.
    Args:
        local_blocks (tuple): Additional blocks to include in the StructBlock. Defaults to an empty tuple.
        max_depth (int): The maximum allowed depth for nested list items. Defaults to 3.
        _depth (int): The current recursion depth. Used internally to track nesting level.
        *args: Additional positional arguments passed to the parent StructBlock.
        **kwargs: Additional keyword arguments passed to the parent StructBlock.
    Attributes:
        Meta (class): Wagtail block meta options, including icon, template, label, label_format, and form_classname.
    Behavior:
        - Recursively nests ProcedureListItemBlock as "nested_list_item" up to max_depth.
        - Each list item contains a "content" StreamBlock, which can include other blocks and nested list items.
    """
    def __init__(
        self,
        local_blocks=(),
        max_depth=3,
        _depth=0,
        *args,
        **kwargs
    ):
        _depth += 1
        if _depth <= max_depth:
            streamblocks = list(ListItemStreamBlock().child_blocks.items())
            if _depth < max_depth:
                streamblocks += (
                    ("nested_list_item", ProcedureListItemBlock(
                        local_blocks, max_depth, _depth, *args, **kwargs)),
                )
            local_blocks += (
                ("content", StreamBlock(streamblocks)),
                *local_blocks
            )
        super().__init__(local_blocks, _depth=_depth, *args, **kwargs)

    class Meta:
        icon = 'list-ul'
        template = "blocks/procedure-block/list-item.html"
        label = _("List Item")
        label_format = label + ": {title}"
        form_classname = "struct-block procedure-list-item-block"


class ProcedureValue(StructValue):
    """
    ProcedureValue is a subclass of StructValue that provides methods for rendering
    procedure-related data.
    Methods:
        list_type() -> str:
            Returns the type of HTML list ("ol" for ordered, "ul" for unordered)
            based on the "is_ordered" attribute.
        heading() -> str:
            Returns a formatted HTML heading string using the "title", "anchor_id",
            and "heading_size" attributes. If "anchor_id" is provided, it is added
            as an id attribute to the heading element.
    """
    def list_type(self) -> str:
        return "ol" if self.get("is_ordered") else "ul"

    def heading(self) -> str:
        title = self.get("title")
        id = self.get("anchor_id", '')
        if id:
            id = format_html(" id={}", id)
        size = self.get("heading_size")
        return format_html("<{}{} class='procedure-heading'>{}</{}>", size, id, title, size)


class ProcedureBlock(StructBlock):
    """
    A custom Wagtail StructBlock for representing a procedure with a title, heading size, optional anchor, introduction, and a list of steps.
    Args:
        heading_range (tuple): Allowed heading levels for the block's title (default: ('h2', 'h4')).
        default_size (str): Default heading size for the title (default: 'h3').
        max_depth (int): Maximum nesting depth for procedure list items (default: 3, valid: 1 - 5).
        **kwargs: Additional keyword arguments passed to the parent StructBlock.
    Fields:
        title (CharBlock): The title of the procedure.
        heading_size (HeadingSizeChoiceBlock): The heading size for the title.
        anchor_id (CharBlock): Optional anchor identifier for linking.
        is_ordered (BooleanBlock): Whether the procedure list is ordered (default: True).
        introduction (RichTextBlock): Optional introductory text for the procedure.
        items (ListBlock): List of procedure steps, each represented by a ProcedureListItemBlock.
    Methods:
        clean(value): Validates the block's data, ensuring the anchor_id is a valid slug. Suggests a valid slug if necessary.
    Raises:
        StructBlockValidationError: If the anchor_id is not a valid slug.
    """
    MAX_DEPTH: Final = 5

    def __init__(
            self,
            heading_range=('h2', 'h4'),
            default_size='h3',
            max_depth=3,
            **kwargs):
        if not (0 < max_depth <= self.MAX_DEPTH):
            raise ImproperlyConfigured(f'max_depth parameter must be greater than 0 and not exceed {self.MAX_DEPTH}, got {max_depth}')
        local_blocks = (
            ("title", CharBlock(
                label=_("Title"),
            )),
            ("heading_size", HeadingSizeChoiceBlock(
                label=_("Size"),
                heading_range=heading_range,
                default=default_size
            )),
            ("anchor_id", CharBlock(
                label=_("Optional Anchor Identifier"),
                required=False,
            )),
            ("is_ordered", BooleanBlock(
                label=_("Ordered List"),
                default=True,
                required=False
            )),
            ("introduction", RichTextBlock(
                editor='minimal',
                features=None,
                label=_("Optional Introduction Text"),
                required=False
            )),
            ("items", ListBlock(
                ProcedureListItemBlock(max_depth=max_depth),
                min=1
            ))
        )
        super().__init__(local_blocks, **kwargs)

    class Meta:
        template = 'blocks/procedure-block/block.html'
        label = _("Procedure Block")
        label_format = label + ": {title}"
        form_classname = "struct-block procedure-block"
        icon = 'list-ol'
        value_class = ProcedureValue

    def clean(self, value):
        errors = {}
        anchor_id = value.get('anchor_id')
        if anchor_id:
            if not validators.slug(anchor_id):
                slug = slugify(unidecode.unidecode(anchor_id)) or slugify(
                    unidecode.unidecode(value.get('title')))
                errors['anchor_id'] = ErrorList([_(f"\
                    '{anchor_id}' is not a valid slug for the anchor identifier. \
                    '{slug}' is the suggested value for this.")])
                raise StructBlockValidationError(block_errors=errors)

        return super().clean(value)

ProcedureBlock.MAX_DEPTH = 4
class ProcedureBlockAdapter(StructBlockAdapter):
    """
    Adapter to add the styling to the admin form
    """
    @cached_property
    def media(self):
        return forms.Media(
            css={"all": ("css/admin/procedure-block-admin.css",)},
        )


register(ProcedureBlockAdapter(), ProcedureBlock)
