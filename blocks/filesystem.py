from typing import Final

from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import CharBlock, IntegerBlock, StreamBlock, StructBlock, StructValue


class FileBlockValue(StructValue):
    @cached_property
    def label(self) -> str:
        return f"┗━ 📄 {self.get('name')} ({self.get('size')} bytes)"


class LinkBlockValue(StructValue):
    @cached_property
    def label(self) -> str:
        return f"┗━ 🔗 {self.get('name')} ({self.get('target')})"


class FolderBlockValue(StructValue):
    @cached_property
    def label(self) -> str:
        return f"┗━ 📁 {self.get('name')} ({len(self['content'].raw_data)} items)"


class FileBlock(StructBlock):
    """
    A simple representation of a file with a name and size.
    """
    name = CharBlock(label=_("File Name"), max_length=255)
    size = IntegerBlock(label=_("File Size (bytes)"), max_length=50)

    def __str__(self) -> str:
        return f"{self.name} ({self.size} bytes)"

    class Meta:
        icon = 'doc-full'
        value_class = FileBlockValue


class LinkBlock(StructBlock):
    """
    A simple representation of a link with a name and target.
    """
    name = CharBlock(label=_("Link Text"), max_length=255)
    target = CharBlock(label=_("Target"), max_length=2048)

    def __str__(self) -> str:
        return f"{self.name} ({self.target})"

    class Meta:
        icon = 'link'
        value_class = LinkBlockValue


class FolderContents(StreamBlock):
    """
    A block representing the contents of a folder, which can include files and links.
    This definition is exclusive of Folder so that the final folder layer can contain only files and links.
    """
    file = FileBlock()
    link = LinkBlock()


class FolderItemBlock(StructBlock):
    """
    A recursive block representing a folder that can contain folders (self), files and links.
    """
    MAX_DEPTH: Final = 5

    def __init__(self, local_blocks=(), max_depth=3, _depth=0, *args, **kwargs):
        if not (0 < max_depth <= self.MAX_DEPTH):
            raise ImproperlyConfigured(
                f'max_depth parameter must be greater than 0 and not exceed {self.MAX_DEPTH}, got {max_depth}'
            )

        _depth += 1  # keep track of recursion depth
        if _depth <= max_depth:  # safety check - should never be false
            streamblocks = []
            if _depth < max_depth:  # recursion: add self only if not at max_depth
                streamblocks += [
                    ("folder", FolderItemBlock(local_blocks, max_depth, _depth, *args, **kwargs)),
                ]
            # always add base blocks
            streamblocks += list(FolderContents().child_blocks.items())
            local_blocks += (
                # define folder name here rather than as class attribute
                ("name", CharBlock(label=_("Name"), max_length=255)),
                # add the content StreamBlock here so it can include self
                ("content", StreamBlock(streamblocks)),
                *local_blocks
            )
        super().__init__(local_blocks, _depth=_depth, *args, **kwargs)

    class Meta:
        icon = 'folder'
        template = 'blocks/filesystem-block/outer.html'
        value_class = FolderBlockValue

# class FileSystemBlock(StructBlock):
#     """
#     A block representing a file system structure with folders and files.
#     """
#     MAX_DEPTH: Final = 5

#     def __init__(
#         self,
#         max_depth=3,
#         **kwargs):
#         if not (0 < max_depth <= self.MAX_DEPTH):
#             raise ImproperlyConfigured(f'max_depth parameter must be greater than 0 and not exceed {self.MAX_DEPTH}, got {max_depth}')
#         local_blocks = (
#             ("title", CharBlock(
#                 label=_("Title"),
#             )),
#             ("items", ListBlock(
#                 FolderItemBlock(max_depth=max_depth),
#                 min=1
#             ))
#         )
#         super().__init__(local_blocks, **kwargs)

#     class Meta:
#         template = 'blocks/procedure-block/block.html'
#         form_classname = "struct-block filesystem-block"
#         icon = 'folder'
