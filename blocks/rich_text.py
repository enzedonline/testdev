from django.utils.translation import gettext_lazy as _
from wagtail.blocks import StructBlock



class RichTextStructBlock(StructBlock):
    from .choices import TextAlignmentChoiceBlock
    from wagtail.blocks import RichTextBlock

    alignment = TextAlignmentChoiceBlock(default="justify", label=_("Text Alignment"))
    content = RichTextBlock()

    class Meta:
        template = "blocks/simple_richtext_block.html"
        label = _("Rich Text Block")
        label_format = '{content}'
        icon = "pilcrow"
        abstract = True


class SimpleRichTextBlock(RichTextStructBlock):
    pass


class MinimalRichTextBlock(RichTextStructBlock):
    from wagtail.blocks import RichTextBlock
    content = RichTextBlock(editor="minimal")


class BasicRichTextBlock(RichTextStructBlock):
    from wagtail.blocks import RichTextBlock
    content = RichTextBlock(editor="basic")
