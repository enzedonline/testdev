from types import SimpleNamespace

from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

cellColor = SimpleNamespace(
    primary='#4582ec',
    secondary='#adb5bd',
    success='#02b875',
    warning='#f0ad4e',
    fail='#d9534f',
    default='white'
)

def generate_table_options(max_rows=7, max_cols=7):
    table_options = [f"newtable_{r+1}_{c+1}" for r in range(max_rows) for c in range(max_cols)]
    return table_options

DEFAULT_CONFIG = {
    'theme': 'snow',
    'modules': {
        # code highlighter
        'syntax': True,
        # quill-image-compress
        "imageCompressor": {
            "quality": 0.7,
            "maxWidth": 1500,
            "maxHeight": 1500,
            "imageType": "image/jpeg",
            "debug": False,
            "suppressErrorLogging": True,
        },
        # quill-better-table-plus
        'table': 'false',
        'better-table-plus': {
            "operationMenu": {
                "items": {
                    "unmergeCells": {
                        "text": 'Unmerge'
                    }
                },
                "color": {
                    "colors": [
                        cellColor.primary, 
                        cellColor.secondary, 
                        cellColor.success, 
                        cellColor.warning, 
                        cellColor.fail, 
                        cellColor.default
                    ],
                    "text": 'Background Colors:'
                }
            }
        },
        # quill-blot-formatter
        'blotFormatter': {},
        # quill-magic-url
        'magicUrl': True,

        'toolbar': [
            [{'header': [2, 3, 4, 5, 6, False]},'bold', 'italic', 'underline', 'strike', 
             {'script': 'sub'}, {'script': 'super'}, {'indent': '-1'}, {'indent': '+1'}, {'align': []}], 
            [{'better-table-plus': generate_table_options()},{'list': 'ordered'}, {'list': 'bullet'}, {'list': 'check'}],
            ['blockquote', 'code-block'],
            ['link', 'image', 'video', 'formula'],
            [{'color': []}, {'background': []}],
            ['clean'] 
        ],
        # 'keyboard': { https://github.com/seehar/quill-better-table-plus/issues/6
        #     'bindings': 'quillBetterTablePlus.keyboardBindings'
        # }
    },
}
MEDIA_JS = [
        # syntax-highlight - must be before quilljs
        "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js",
        # quill
        "https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.js",
        # quill-better-table
        "https://unpkg.com/quill-better-table-plus@0.1.6/dist/quill-better-table-plus.js",
        # quill-image-compress
        "https://cdn.jsdelivr.net/npm/quill-image-compress@1.2.21/dist/quill.imageCompressor.min.js",
        # quill-blot-formatter
        "https://cdn.jsdelivr.net/npm/quill-blot-formatter@1.0.5/dist/quill-blot-formatter.min.js",
        # quill-magic-url
        "https://unpkg.com/quill-magic-url@3.0.0/dist/index.js",
        # quill-paste-smart - not yet compatible with quill 2 https://github.com/Artem-Schander/quill-paste-smart/issues/33
        # "https://unpkg.com/quill-paste-smart@latest/dist/quill-paste-smart.js", 
        # custom
        static("js/quill.js"),
]
MEDIA_CSS = [
    # quill
    "https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.snow.css",
    # syntax-highlight
    "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css",
    # quill-better-table
    "https://unpkg.com/quill-better-table-plus@0.1.6/dist/quill-better-table-plus.css",
    # custom
    static("css/quill.css"),
]
TOOLBAR_LABELS = [
        ('span.ql-header', _("Heading Size")),
        ('button.ql-bold', _("Bold")),
        ('button.ql-italic', _("Italic")),
        ('button.ql-underline', _("Underline")),
        ('button.ql-strike', _("Strikethrough")),
        ('button.ql-script[value="sub"]', _("Subscript")),
        ('button.ql-script[value="super"]', _("Superscript")),
        ('button.ql-indent[value="-1"]', _("Decrease Indent")),
        ('button.ql-indent[value="+1"]', _("Increase Indent")),
        ('span.ql-align', _("Text Align")),
        ('span.ql-align>span.ql-picker-options>span:not([data-value])', _("Align Left")),
        ('span.ql-align>span.ql-picker-options>span[data-value="center"]', _("Align Centre")),
        ('span.ql-align>span.ql-picker-options>span[data-value="right"]', _("Align Right")),
        ('span.ql-align>span.ql-picker-options>span[data-value="justify"]', _("Justfied")),
        ('span.ql-better-table-plus', _("Insert Table")),
        ('button.ql-list[value="ordered"]', _("Ordered List")), 
        ('button.ql-list[value="bullet"]', _("Bullet list")),
        ('button.ql-list[value="check"]', _("Check List")),
        ('button.ql-blockquote', _("Block Quote")),
        ('button.ql-code-block', _("Code Block")),
        ('button.ql-link', _("Insert Hyperlink")),
        ('button.ql-image', _("Insert Image")),
        ('button.ql-video', _("Embed Video")),
        ('button.ql-formula', _("Insert Katex Formula")),
        ('span-ql-color', _("Font Colour")),
        ('span.ql-background', _("Background Colour")),
        ('button.ql-clean', _("Clear Formatting"))
]
