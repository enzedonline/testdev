from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

DEFAULT_CONFIG = {
    'quillOptions': {
        'theme': 'snow',
        'modules': {
            # code highlighter
            'syntax': True,
            # quill-paste-smart
            "clipboard": {
                "customButtons": [
                    {
                        "module": 'insertBetterTablePlus',
                        "allowedTags": ['table', 'tr', 'td'],
                    },
                    {
                        "module": 'code',
                        "allowedTags": ['code']
                    },
                    {
                        "module": 'divider',
                        "allowedTags": ['hr']
                    },
                ],
                "removeEmptyLines": True
            },
            # quill-image-compress
            "imageCompressor": {
                "quality": 0.7,
                "maxWidth": 1200,
                "maxHeight": 600,
                "imageType": "image/jpeg",
                "debug": False,
                "suppressErrorLogging": True,
                "handleOnPaste": True
            },
            # quill-image-reducer - resize embedded images with width/height attributes
            # 'image-reducer': {
            #     'jpeg_compression': 0.7,
            #     'toast_label': _('Reduced')
            # },
            # quill-better-table-plus
            'table': False,
            'better-table-plus': {
                "operationMenu": {
                    "items": {
                        "insertColumnRight": {
                            "text": _('Insert Column Right')
                        },
                        "insertColumnLeft": {
                            "text": _('Insert Column Left')
                        },
                        "insertRowUp": {
                            "text": _('Insert Row Above')
                        },
                        "insertRowDown": {
                            "text": _('Insert Row Below')
                        },
                        "mergeCells": {
                            "text": _('Merge Cells')
                        },
                        "unmergeCells": {
                            "text": _('Unmerge Cell')
                        },
                        "deleteColumn": {
                            "text": _('Delete Column')
                        },
                        "deleteRow": {
                            "text": _('Delete Row')
                        },
                        "deleteTable": {
                            "text": _('Delete Table')
                        },
                    },
                    "color": {
                        "colors": [
                            '#4582ec',  # primary
                            '#adb5bd',  # secondary
                            '#02b875',  # success
                            '#f0ad4e',  # warning
                            '#d9534f',  # fail
                            'white',   # default
                        ],
                        "text": _('Background Colours')
                    }
                }
            },
            # quill-insert-better-table-plus
            'insertBetterTablePlus': {
                'tableClassList': 'table table-borderless'
            },
            # quill-blot-formatter
            'blotFormatter2': {
                'video': {
                    'registerCustomVideoBlot': True,
                    'proxyStyle': {'border': '5px red solid'},
                },
                'resize': {
                    'useRelativeSize': True,
                    'allowResizeModeChange': True,
                    'allowResizing': True,
                    # 'imageOversizeProtection': True
                },
                'image': {
                    'allowAltTitleEdit': True,
                    'registerImageTitleBlot': True,
                    'allowCompressor': True,
                    'compressorOptions': {
                        'maxWidth': 800,
                    }
                }
            },
            # quill-magic-url
            'magicUrl': True,
            # 'list: check' and 'formula' not currently compatible with getSemanticHTML
            'toolbar': {
                'container': [
                    [{'header': [2, 3, 4, 5, 6, False]}, 'bold', 'italic', 'underline', 'strike',
                     {'script': 'sub'}, {'script': 'super'}, 'code', {'indent': '-1'}, {'indent': '+1'}, {'align': []}],
                    [{'insertBetterTablePlus': []}, {'list': 'ordered'}, {'list': 'bullet'}],
                    ['link', 'image', 'video'],
                    ['divider', 'linebreak', 'blockquote', 'code-block'],
                    [{'color': []}, {'background': []}],
                    ['clean']
                ],
                'handlers': {
                    # 'image-reducer': True,
                    'insertBetterTablePlus': True
                }
            },
            # 'keyboard': {
            #     register keyboard bindings in js
            #     see static/js/django-quill2/quill-register.js
            # }
        },
    },
    'quillRegister': [
        ("modules/imageCompressor", "imageCompressor"),
        ('modules/blotFormatter2', 'QuillBlotFormatter2.default'),
        ('modules/better-table-plus', "quillBetterTablePlus"),
        ("modules/insertBetterTablePlus", "InsertBetterTablePlus")
    ],
    'media_js': [
        # syntax-highlight - must be before quilljs
        "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js",
        # quill
        "https://cdn.jsdelivr.net/npm/quill@2.0/dist/quill.js",
        # quill-better-table-plus + toolbar button handler
        "https://cdn.jsdelivr.net/npm/quill-better-table-plus@0.1",
        static("js/django-quill2/quill-insert-better-table-plus.js"),
        # quill-image-compress
        # "https://cdn.jsdelivr.net/npm/quill-image-compress@1.2/dist/quill.imageCompressor.min.js",
        static("js/django-quill2/quill.imageCompressor.min.js"),
        # quill-blot-formatter
        static("js/django-quill2/quill-blot-formatter2.min.js"),
        # quill-magic-url
        "https://unpkg.com/quill-magic-url@4.2.0/dist/index.js",
        # quill-paste-smart
        static("js/django-quill2/quill-paste-smart.js"),
        # quill register + widget - register MUST run before widget
        static("js/django-quill2/quill-register.js"),
        static("js/django-quill2/quill-widget.js"),
    ],
    'media_css': [
        # quill
        "https://cdn.jsdelivr.net/npm/quill@2.0/dist/quill.snow.css",
        # syntax-highlight
        "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css",
        # quill-better-table
        static("css/django-quill2/quill-better-table-plus.css"),
        # quill-insert-better-table-plus
        static("css/django-quill2/quill-insert-better-table-plus.css"),
        # quill-blot-formatter
        static("css/django-quill2/quill-blot-formatter2.css"),
        # quill widget
        static("css/django-quill2/quill-widget.css"),
    ],
    'buttonTooltips': [
        # set toolbar button tooltip (title attribute) from query selector string
        # support for multi-lingual tooltips
        # [(query selector, tooltip text), ...]
        ('span.ql-header', _("Heading Size")),
        ('button.ql-bold', _("Bold")),
        ('button.ql-italic', _("Italic")),
        ('button.ql-underline', _("Underline")),
        ('button.ql-strike', _("Strikethrough")),
        ('button.ql-script[value="sub"]', _("Subscript")),
        ('button.ql-script[value="super"]', _("Superscript")),
        ('button.ql-code', _("Inline Code")),
        ('button.ql-indent[value="-1"]', _("Decrease Indent")),
        ('button.ql-indent[value="+1"]', _("Increase Indent")),
        ('span.ql-align', _("Text Align")),
        ('span.ql-align>span.ql-picker-options>span:not([data-value])', _(
            "Align Left")),
        ('span.ql-align>span.ql-picker-options>span[data-value="center"]', _(
            "Align Centre")),
        ('span.ql-align>span.ql-picker-options>span[data-value="right"]', _(
            "Align Right")),
        ('span.ql-align>span.ql-picker-options>span[data-value="justify"]', _(
            "Justfied")),
        ('span.ql-insertBetterTablePlus', _("Insert Table")),
        ('button.ql-list[value="ordered"]', _("Ordered List")),
        ('button.ql-list[value="bullet"]', _("Bullet List")),
        ('button.ql-list[value="check"]', _("Check List")),
        ('button.ql-divider', _("Insert Divider")),
        ('button.ql-linebreak', _("Line Break")),
        ('button.ql-blockquote', _("Block Quote")),
        ('button.ql-code-block', _("Code Block")),
        ('button.ql-link', _("Insert Hyperlink")),
        ('button.ql-image', _("Insert Image")),
        # ('button.ql-image-reducer', _("Reduce Resized Images")),
        ('button.ql-video', _("Embed Video")),
        ('button.ql-formula', _("Insert Katex Formula")),
        ('span.ql-color', _("Font Colour")),
        ('span.ql-background', _("Background Colour")),
        ('.ql-color-picker .ql-picker-item:not([data-value])',
         _("Default Colour")),
        ('button.ql-clean', _("Plain Text"))
    ],
    'buttonIcons': [
        # set toolbar button icon from query selector string
        # [(query selector: svg as string), ...]
        (
            'button.ql-clean',
            """
            <svg viewBox="0 0 16 16" class="ql-stroke ql-fill">
            <text xml:space="preserve" style="font-family:'Segoe UI';letter-spacing:-1.33px;display:inline;stroke:none;stroke-width:80;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:3.6;stroke-opacity:1">
                <tspan x="-0.15" y="10.5""><tspan style="font-size:14px;letter-spacing:-1.33px;">A</tspan><tspan style="font-size:12px;letter-spacing:-1.33px;">b</tspan></tspan>
            </text>
            <path fill-rule="evenodd" clip-rule="evenodd" d="m 11.55528,14.622154 c -0.227641,0.227692 -0.432256,0.432308 -0.620666,0.608615 h 4.680767 c 0.212411,0 0.384616,0.172205 0.384616,0.384616 C 15.999997,15.827795 15.827792,16 15.615381,16 H 9.4615373 C 9.4521285,16 9.4428029,15.999641 9.433569,15.999 9.0725938,15.985179 8.7663529,15.829179 8.4659633,15.6 8.1647378,15.370154 7.8284045,15.033846 7.4167636,14.622154 l -0.038948,-0.03893 C 6.9661638,14.17159 6.6298203,13.835282 6.3999999,13.534052 6.1597897,13.219179 6,12.897948 6,12.513948 6,12.13 6.1597897,11.808718 6.3999999,11.493898 6.6298255,11.192667 6.9661638,10.856359 7.3778149,10.444718 L 10.444717,7.3778154 C 10.856357,6.9661692 11.192665,6.6298205 11.493896,6.4 11.808717,6.1597897 12.129998,6 12.513946,6 c 0.384,0 0.705231,0.1597897 1.020104,0.4 0.301229,0.2298257 0.637537,0.5661641 1.049178,0.9778154 l 0.03893,0.038948 c 0.411692,0.411641 0.748,0.7479744 0.977846,1.0492 0.240205,0.3148359 0.4,0.6360974 0.4,1.020067 0,0.3839642 -0.159795,0.7052516 -0.4,1.0200726 -0.229795,0.30123 -0.566154,0.637538 -0.977795,1.049128 z M 10.969177,7.9412257 c 0.435898,-0.4359026 0.736052,-0.7348924 0.991333,-0.9296719 0.246412,-0.1880051 0.405283,-0.2423231 0.553436,-0.2423231 0.148154,0 0.307078,0.054318 0.553487,0.2423231 0.255283,0.1947795 0.555436,0.4937693 0.991333,0.9296719 0.435898,0.4359076 0.734924,0.7360512 0.929693,0.9913384 0.188,0.2464102 0.242307,0.4053126 0.242307,0.5534667 0,0.1481484 -0.0543,0.3070509 -0.242307,0.5534572 -0.194769,0.255281 -0.493795,0.555435 -0.929693,0.991333 l -2.150409,2.15041 -3.0895785,-3.08959 z M 9.4860294,15.230769 c 0.1481482,0 0.3070507,-0.05431 0.5534566,-0.242307 0.255282,-0.19477 0.555436,-0.493795 0.991333,-0.929693 L 11.36446,13.725128 8.2748505,10.635538 7.941225,10.969179 c -0.4359024,0.435898 -0.7348921,0.736052 -0.9296715,0.991334 -0.188005,0.24641 -0.242323,0.405282 -0.242323,0.553435 0,0.148155 0.054318,0.307078 0.242323,0.553488 0.1947794,0.255282 0.4937691,0.555436 0.9296715,0.991333 0.4359076,0.435898 0.736051,0.734924 0.9913381,0.929693 0.2464101,0.188 0.4053123,0.242307 0.5534663,0.242307 z" fill="#1c274c" style="stroke-width:0.512821;stroke:none;stroke-opacity:1;fill:#800080;fill-opacity:1" />
            <path style="fill:#800080;fill-opacity:1;stroke:none;stroke-width:2.33151;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:3.6;stroke-opacity:1" d="M 12.490893,6.2895037 C 11.908309,6.311098 11.495224,6.7701604 11.108037,7.1485086 10.223446,8.0141312 9.3434654,8.8865775 8.4751728,9.7673361 8.2554765,10.002503 8.3518654,10.373754 8.5938102,10.553923 c 1.0085139,0.997504 1.9946268,2.019222 3.0219118,2.996851 0.253499,0.175199 0.587709,0.06359 0.763832,-0.167236 0.969605,-0.973445 1.964079,-1.924181 2.890198,-2.939606 0.332687,-0.344171 0.571111,-0.8604099 0.376309,-1.3328209 C 15.39051,8.5356629 14.888205,8.1236551 14.468457,7.6707587 14.013719,7.2374559 13.59871,6.73852 13.044911,6.4272541 12.873603,6.3410236 12.684182,6.2839769 12.490893,6.2895037 Z" />
            </svg>
            """
        ),
        (
            'button.ql-code-block',
            """
            <svg viewBox="0 0 448 448" class="ql-stroke ql-fill">
            <path d="m 384,48 c 8.8,0 16,7.2 16,16 v 320 c 0,8.8 -7.2,16 -16,16 H 64 c -8.8,0 -16,-7.2 -16,-16 V 64 C 48,55.2 55.2,48 64,48 Z M 64,0 C 28.7,0 0,28.7 0,64 v 320 c 0,35.3 28.7,64 64,64 h 320 c 35.3,0 64,-28.7 64,-64 V 64 C 448,28.7 419.3,0 384,0 Z"
                style="stroke-width:0.5;stroke-dasharray:none" />
            <path d="m 257.56154,105.57972 c -7.85831,-2.26503 -16.04019,2.31127 -18.30522,10.16957 l -59.16844,207.08936 c -2.26504,7.85831 2.31128,16.04018 10.16958,18.30522 7.85831,2.26504 16.04019,-2.31126 18.30523,-10.16957 l 59.16842,-207.08936 c 2.26505,-7.85829 -2.31126,-16.04018 -10.16957,-18.30522 z m 37.25762,55.51659 c -5.77817,5.77817 -5.77817,15.16191 0,20.94007 l 41.27922,41.32542 -41.32545,41.32542 c -5.77816,5.77816 -5.77816,15.16191 0,20.94006 5.77818,5.77816 15.16191,5.77816 20.94009,0 l 51.77236,-51.77234 c 5.77816,-5.77815 5.77816,-15.1619 0,-20.94006 l -51.77236,-51.77234 c -5.77818,-5.77816 -15.16191,-5.77816 -20.94009,0 z m -141.77309,0 c -5.77817,-5.77815 -15.16191,-5.77815 -20.94008,0 l -51.772365,51.77234 c -5.778167,5.77817 -5.778167,15.16191 0,20.94006 l 51.772365,51.77235 c 5.77817,5.77816 15.16191,5.77816 20.94008,0 5.77817,-5.77817 5.77817,-15.1619 0,-20.94007 l -41.32544,-41.27919 41.32544,-41.32542 c 5.77817,-5.77816 5.77817,-15.1619 0,-20.94007 z"
                style="stroke-width:1;stroke-dasharray:none" />
            </svg>
            """
        ),
        (
            '.ql-color-picker .ql-picker-item:not([data-value])',
            """
            <svg viewBox="0 0 17 17" style="width: 16px; height: 16px; margin-top: -8px;">
            <path d="M0 16h1v1h-1v-1zM14 17h1v-1h-1v1zM12 17h1v-1h-1v1zM10 17h1v-1h-1v1zM8 17h1v-1h-1v1zM6 17h1v-1h-1v1zM2 17h1v-1h-1v1zM4 17h1v-1h-1v1zM16 17h1v-1h-1v1zM16 11h1v-1h-1v1zM16 13h1v-1h-1v1zM16 5h1v-1h-1v1zM16 9h1v-1h-1v1zM16 7h1v-1h-1v1zM16 3h1v-1h-1v1zM16 15h1v-1h-1v1zM16 0v1h1v-1h-1zM4 1h1v-1h-1v1zM2 1h1v-1h-1v1zM12 1h1v-1h-1v1zM10 1h1v-1h-1v1zM6 1h1v-1h-1v1zM14 1h1v-1h-1v1zM8 1h1v-1h-1v1zM0 1h1v-1h-1v1zM0 13h1v-1h-1v1zM0 15h1v-1h-1v1zM0 11h1v-1h-1v1zM0 5h1v-1h-1v1zM0 9h1v-1h-1v1zM0 3h1v-1h-1v1zM0 7h1v-1h-1v1z"/>
            <path d="m 11.70025,6.26025 c 0.265625,-0.265625 0.265625,-0.697 0,-0.962625 -0.265625,-0.265625 -0.697,-0.265625 -0.962625,0 L 8.5,7.537375 6.26025,5.29975 c -0.265625,-0.265625 -0.697,-0.265625 -0.962625,0 -0.265625,0.265625 -0.265625,0.697 0,0.962625 L 7.537375,8.5 5.29975,10.73975 c -0.265625,0.265625 -0.265625,0.697 0,0.962625 0.265625,0.265625 0.697,0.265625 0.962625,0 L 8.5,9.462625 10.73975,11.70025 c 0.265625,0.265625 0.697,0.265625 0.962625,0 0.265625,-0.265625 0.265625,-0.697 0,-0.962625 L 9.462625,8.5 Z"
            style="stroke-width:0.02125" />
            </svg>
            """
        ),
        (
            'button.ql-divider',
            """
            <svg viewBox="0 0 448 512" class="ql-stroke ql-fill">
            <path d="M432 256c0 17.7-14.3 32-32 32L48 288c-17.7 0-32-14.3-32-32s14.3-32 32-32l352 0c17.7 0 32 14.3 32 32z"/>
            </svg>
            """
        ),
        (
            'button.ql-linebreak',
            """
            <svg viewBox="0 0 1024 1024" class="ql-stroke ql-fill">
            <path d="M864 170h-60c-4.4 0-8 3.6-8 8v518H310v-73c0-6.7-7.8-10.5-13-6.3l-141.9 112a8 8 0 0 0 0 12.6l141.9 112c5.3 4.2 13 .4 13-6.3v-75h498c35.3 0 64-28.7 64-64V178c0-4.4-3.6-8-8-8z"/>
            </svg>
            """
        ),
    ],
    'toolbarLabels': [
        # support for multi-lingual dropdown labels
        # [(query selector, label text, ...)]
        # font size labels
        ('.ql-picker.ql-header .ql-picker-label[data-value="1"]::before, .ql-picker.ql-header .ql-picker-item[data-value="1"]::before', _(
            "Heading 1")),
        ('.ql-picker.ql-header .ql-picker-label[data-value="2"]::before, .ql-picker.ql-header .ql-picker-item[data-value="2"]::before', _(
            "Heading 2")),
        ('.ql-picker.ql-header .ql-picker-label[data-value="3"]::before, .ql-picker.ql-header .ql-picker-item[data-value="3"]::before', _(
            "Heading 3")),
        ('.ql-picker.ql-header .ql-picker-label[data-value="4"]::before, .ql-picker.ql-header .ql-picker-item[data-value="4"]::before', _(
            "Heading 4")),
        ('.ql-picker.ql-header .ql-picker-label[data-value="5"]::before, .ql-picker.ql-header .ql-picker-item[data-value="5"]::before', _(
            "Heading 5")),
        ('.ql-picker.ql-header .ql-picker-label[data-value="6"]::before, .ql-picker.ql-header .ql-picker-item[data-value="6"]::before', _(
            "Heading 6")),
        ('.ql-picker.ql-header .ql-picker-label:not([data-value])::before, .ql-picker.ql-header .ql-picker-item:not([data-value])::before', _(
            "Normal")),
    ]
}

MEDIA_JS = [
    # syntax-highlight - must be before quilljs
    "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js",
    # quill
    "https://cdn.jsdelivr.net/npm/quill@2.0/dist/quill.js",
    # quill-better-table-plus + toolbar button handler
    "https://unpkg.com/quill-better-table-plus@0.1.6/dist/quill-better-table-plus.js",
    static("js/django-quill2/quill-insert-better-table-plus.js"),
    # quill-image-compress
    # "https://cdn.jsdelivr.net/npm/quill-image-compress@1.2/dist/quill.imageCompressor.min.js",
    static("js/django-quill2/quill.imageCompressor.min.js"),
    # quill-blot-formatter
    static("js/django-quill2/quill-blot-formatter2.min.js"),
    # quill-magic-url
    "https://unpkg.com/quill-magic-url@4.2.0/dist/index.js",
    # quill-paste-smart
    static("js/django-quill2/quill-paste-smart.js"),
    # quill-image-reducer
    # static("js/django-quill2/quill-image-reducer.js"),
    static("js/django-quill2/quill-syntax-code-block-container.js"),
    # quill register + widget - register MUST run before widget
    static("js/django-quill2/quill-register.js"),
    static("js/django-quill2/quill-widget.js"),
]

MEDIA_CSS = [
    # quill
    "https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.snow.css",
    # syntax-highlight
    "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css",
    # quill-better-table
    static("css/django-quill2/quill-better-table-plus.css"),
    # quill-insert-better-table-plus
    static("css/django-quill2/quill-insert-better-table-plus.css"),
    # quill-blot-formatter
    static("css/django-quill2/quill-blot-formatter2.css"),
    # quill widget
    static("css/django-quill2/quill-widget.css"),
]

BUTTON_TOOLTIPS = [
    # set toolbar button tooltip (title attribute) from query selector string
    # support for multi-lingual tooltips
    # [(query selector, tooltip text), ...]
    ('span.ql-header', _("Heading Size")),
    ('button.ql-bold', _("Bold")),
    ('button.ql-italic', _("Italic")),
    ('button.ql-underline', _("Underline")),
    ('button.ql-strike', _("Strikethrough")),
    ('button.ql-script[value="sub"]', _("Subscript")),
    ('button.ql-script[value="super"]', _("Superscript")),
    ('button.ql-code', _("Inline Code")),
    ('button.ql-indent[value="-1"]', _("Decrease Indent")),
    ('button.ql-indent[value="+1"]', _("Increase Indent")),
    ('span.ql-align', _("Text Align")),
    ('span.ql-align>span.ql-picker-options>span:not([data-value])', _(
        "Align Left")),
    ('span.ql-align>span.ql-picker-options>span[data-value="center"]', _(
        "Align Centre")),
    ('span.ql-align>span.ql-picker-options>span[data-value="right"]', _(
        "Align Right")),
    ('span.ql-align>span.ql-picker-options>span[data-value="justify"]', _(
        "Justfied")),
    ('span.ql-insertBetterTablePlus', _("Insert Table")),
    ('button.ql-list[value="ordered"]', _("Ordered List")),
    ('button.ql-list[value="bullet"]', _("Bullet List")),
    ('button.ql-list[value="check"]', _("Check List")),
    ('button.ql-divider', _("Insert Divider")),
    ('button.ql-linebreak', _("Line Break")),
    ('button.ql-blockquote', _("Block Quote")),
    ('button.ql-code-block', _("Code Block")),
    ('button.ql-link', _("Insert Hyperlink")),
    ('button.ql-image', _("Insert Image")),
    # ('button.ql-image-reducer', _("Reduce Resized Images")),
    ('button.ql-video', _("Embed Video")),
    ('button.ql-formula', _("Insert Katex Formula")),
    ('span.ql-color', _("Font Colour")),
    ('span.ql-background', _("Background Colour")),
    ('.ql-color-picker .ql-picker-item:not([data-value])',
     _("Default Colour")),
    ('button.ql-clean', _("Plain Text"))
]

BUTTON_ICONS = [
    # set toolbar button icon from query selector string
    # [(query selector: svg as string), ...]
    (
        'button.ql-clean',
        """
        <svg viewBox="0 0 16 16" class="ql-stroke ql-fill">
        <text xml:space="preserve" style="font-family:'Segoe UI';letter-spacing:-1.33px;display:inline;stroke:none;stroke-width:80;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:3.6;stroke-opacity:1">
            <tspan x="-0.15" y="10.5""><tspan style="font-size:14px;letter-spacing:-1.33px;">A</tspan><tspan style="font-size:12px;letter-spacing:-1.33px;">b</tspan></tspan>
        </text>
        <path fill-rule="evenodd" clip-rule="evenodd" d="m 11.55528,14.622154 c -0.227641,0.227692 -0.432256,0.432308 -0.620666,0.608615 h 4.680767 c 0.212411,0 0.384616,0.172205 0.384616,0.384616 C 15.999997,15.827795 15.827792,16 15.615381,16 H 9.4615373 C 9.4521285,16 9.4428029,15.999641 9.433569,15.999 9.0725938,15.985179 8.7663529,15.829179 8.4659633,15.6 8.1647378,15.370154 7.8284045,15.033846 7.4167636,14.622154 l -0.038948,-0.03893 C 6.9661638,14.17159 6.6298203,13.835282 6.3999999,13.534052 6.1597897,13.219179 6,12.897948 6,12.513948 6,12.13 6.1597897,11.808718 6.3999999,11.493898 6.6298255,11.192667 6.9661638,10.856359 7.3778149,10.444718 L 10.444717,7.3778154 C 10.856357,6.9661692 11.192665,6.6298205 11.493896,6.4 11.808717,6.1597897 12.129998,6 12.513946,6 c 0.384,0 0.705231,0.1597897 1.020104,0.4 0.301229,0.2298257 0.637537,0.5661641 1.049178,0.9778154 l 0.03893,0.038948 c 0.411692,0.411641 0.748,0.7479744 0.977846,1.0492 0.240205,0.3148359 0.4,0.6360974 0.4,1.020067 0,0.3839642 -0.159795,0.7052516 -0.4,1.0200726 -0.229795,0.30123 -0.566154,0.637538 -0.977795,1.049128 z M 10.969177,7.9412257 c 0.435898,-0.4359026 0.736052,-0.7348924 0.991333,-0.9296719 0.246412,-0.1880051 0.405283,-0.2423231 0.553436,-0.2423231 0.148154,0 0.307078,0.054318 0.553487,0.2423231 0.255283,0.1947795 0.555436,0.4937693 0.991333,0.9296719 0.435898,0.4359076 0.734924,0.7360512 0.929693,0.9913384 0.188,0.2464102 0.242307,0.4053126 0.242307,0.5534667 0,0.1481484 -0.0543,0.3070509 -0.242307,0.5534572 -0.194769,0.255281 -0.493795,0.555435 -0.929693,0.991333 l -2.150409,2.15041 -3.0895785,-3.08959 z M 9.4860294,15.230769 c 0.1481482,0 0.3070507,-0.05431 0.5534566,-0.242307 0.255282,-0.19477 0.555436,-0.493795 0.991333,-0.929693 L 11.36446,13.725128 8.2748505,10.635538 7.941225,10.969179 c -0.4359024,0.435898 -0.7348921,0.736052 -0.9296715,0.991334 -0.188005,0.24641 -0.242323,0.405282 -0.242323,0.553435 0,0.148155 0.054318,0.307078 0.242323,0.553488 0.1947794,0.255282 0.4937691,0.555436 0.9296715,0.991333 0.4359076,0.435898 0.736051,0.734924 0.9913381,0.929693 0.2464101,0.188 0.4053123,0.242307 0.5534663,0.242307 z" fill="#1c274c" style="stroke-width:0.512821;stroke:none;stroke-opacity:1;fill:#800080;fill-opacity:1" />
        <path style="fill:#800080;fill-opacity:1;stroke:none;stroke-width:2.33151;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:3.6;stroke-opacity:1" d="M 12.490893,6.2895037 C 11.908309,6.311098 11.495224,6.7701604 11.108037,7.1485086 10.223446,8.0141312 9.3434654,8.8865775 8.4751728,9.7673361 8.2554765,10.002503 8.3518654,10.373754 8.5938102,10.553923 c 1.0085139,0.997504 1.9946268,2.019222 3.0219118,2.996851 0.253499,0.175199 0.587709,0.06359 0.763832,-0.167236 0.969605,-0.973445 1.964079,-1.924181 2.890198,-2.939606 0.332687,-0.344171 0.571111,-0.8604099 0.376309,-1.3328209 C 15.39051,8.5356629 14.888205,8.1236551 14.468457,7.6707587 14.013719,7.2374559 13.59871,6.73852 13.044911,6.4272541 12.873603,6.3410236 12.684182,6.2839769 12.490893,6.2895037 Z" />
        </svg>
        """
    ),
    (
        'button.ql-code-block',
        """
        <svg viewBox="0 0 448 448" class="ql-stroke ql-fill">
        <path d="m 384,48 c 8.8,0 16,7.2 16,16 v 320 c 0,8.8 -7.2,16 -16,16 H 64 c -8.8,0 -16,-7.2 -16,-16 V 64 C 48,55.2 55.2,48 64,48 Z M 64,0 C 28.7,0 0,28.7 0,64 v 320 c 0,35.3 28.7,64 64,64 h 320 c 35.3,0 64,-28.7 64,-64 V 64 C 448,28.7 419.3,0 384,0 Z"
            style="stroke-width:0.5;stroke-dasharray:none" />
        <path d="m 257.56154,105.57972 c -7.85831,-2.26503 -16.04019,2.31127 -18.30522,10.16957 l -59.16844,207.08936 c -2.26504,7.85831 2.31128,16.04018 10.16958,18.30522 7.85831,2.26504 16.04019,-2.31126 18.30523,-10.16957 l 59.16842,-207.08936 c 2.26505,-7.85829 -2.31126,-16.04018 -10.16957,-18.30522 z m 37.25762,55.51659 c -5.77817,5.77817 -5.77817,15.16191 0,20.94007 l 41.27922,41.32542 -41.32545,41.32542 c -5.77816,5.77816 -5.77816,15.16191 0,20.94006 5.77818,5.77816 15.16191,5.77816 20.94009,0 l 51.77236,-51.77234 c 5.77816,-5.77815 5.77816,-15.1619 0,-20.94006 l -51.77236,-51.77234 c -5.77818,-5.77816 -15.16191,-5.77816 -20.94009,0 z m -141.77309,0 c -5.77817,-5.77815 -15.16191,-5.77815 -20.94008,0 l -51.772365,51.77234 c -5.778167,5.77817 -5.778167,15.16191 0,20.94006 l 51.772365,51.77235 c 5.77817,5.77816 15.16191,5.77816 20.94008,0 5.77817,-5.77817 5.77817,-15.1619 0,-20.94007 l -41.32544,-41.27919 41.32544,-41.32542 c 5.77817,-5.77816 5.77817,-15.1619 0,-20.94007 z"
            style="stroke-width:1;stroke-dasharray:none" />
        </svg>
        """
    ),
    (
        '.ql-color-picker .ql-picker-item:not([data-value])',
        """
        <svg viewBox="0 0 17 17" style="width: 16px; height: 16px; margin-top: -8px;">
        <path d="M0 16h1v1h-1v-1zM14 17h1v-1h-1v1zM12 17h1v-1h-1v1zM10 17h1v-1h-1v1zM8 17h1v-1h-1v1zM6 17h1v-1h-1v1zM2 17h1v-1h-1v1zM4 17h1v-1h-1v1zM16 17h1v-1h-1v1zM16 11h1v-1h-1v1zM16 13h1v-1h-1v1zM16 5h1v-1h-1v1zM16 9h1v-1h-1v1zM16 7h1v-1h-1v1zM16 3h1v-1h-1v1zM16 15h1v-1h-1v1zM16 0v1h1v-1h-1zM4 1h1v-1h-1v1zM2 1h1v-1h-1v1zM12 1h1v-1h-1v1zM10 1h1v-1h-1v1zM6 1h1v-1h-1v1zM14 1h1v-1h-1v1zM8 1h1v-1h-1v1zM0 1h1v-1h-1v1zM0 13h1v-1h-1v1zM0 15h1v-1h-1v1zM0 11h1v-1h-1v1zM0 5h1v-1h-1v1zM0 9h1v-1h-1v1zM0 3h1v-1h-1v1zM0 7h1v-1h-1v1z"/>
        <path d="m 11.70025,6.26025 c 0.265625,-0.265625 0.265625,-0.697 0,-0.962625 -0.265625,-0.265625 -0.697,-0.265625 -0.962625,0 L 8.5,7.537375 6.26025,5.29975 c -0.265625,-0.265625 -0.697,-0.265625 -0.962625,0 -0.265625,0.265625 -0.265625,0.697 0,0.962625 L 7.537375,8.5 5.29975,10.73975 c -0.265625,0.265625 -0.265625,0.697 0,0.962625 0.265625,0.265625 0.697,0.265625 0.962625,0 L 8.5,9.462625 10.73975,11.70025 c 0.265625,0.265625 0.697,0.265625 0.962625,0 0.265625,-0.265625 0.265625,-0.697 0,-0.962625 L 9.462625,8.5 Z"
        style="stroke-width:0.02125" />
        </svg>
        """
    ),
    (
        'button.ql-divider',
        """
        <svg viewBox="0 0 448 512" class="ql-stroke ql-fill">
        <path d="M432 256c0 17.7-14.3 32-32 32L48 288c-17.7 0-32-14.3-32-32s14.3-32 32-32l352 0c17.7 0 32 14.3 32 32z"/>
        </svg>
        """
    ),
    (
        'button.ql-linebreak',
        """
        <svg viewBox="0 0 1024 1024" class="ql-stroke ql-fill">
        <path d="M864 170h-60c-4.4 0-8 3.6-8 8v518H310v-73c0-6.7-7.8-10.5-13-6.3l-141.9 112a8 8 0 0 0 0 12.6l141.9 112c5.3 4.2 13 .4 13-6.3v-75h498c35.3 0 64-28.7 64-64V178c0-4.4-3.6-8-8-8z"/>
        </svg>
        """
    ),
]

TOOLBAR_LABELS = [
    # support for multi-lingual dropdown labels
    # [(query selector, label text, ...)]
    # font size labels
    ('.ql-picker.ql-header .ql-picker-label[data-value="1"]::before, .ql-picker.ql-header .ql-picker-item[data-value="1"]::before', _("Heading 1")),
    ('.ql-picker.ql-header .ql-picker-label[data-value="2"]::before, .ql-picker.ql-header .ql-picker-item[data-value="2"]::before', _("Heading 2")),
    ('.ql-picker.ql-header .ql-picker-label[data-value="3"]::before, .ql-picker.ql-header .ql-picker-item[data-value="3"]::before', _("Heading 3")),
    ('.ql-picker.ql-header .ql-picker-label[data-value="4"]::before, .ql-picker.ql-header .ql-picker-item[data-value="4"]::before', _("Heading 4")),
    ('.ql-picker.ql-header .ql-picker-label[data-value="5"]::before, .ql-picker.ql-header .ql-picker-item[data-value="5"]::before', _("Heading 5")),
    ('.ql-picker.ql-header .ql-picker-label[data-value="6"]::before, .ql-picker.ql-header .ql-picker-item[data-value="6"]::before', _("Heading 6")),
    ('.ql-picker.ql-header .ql-picker-label:not([data-value])::before, .ql-picker.ql-header .ql-picker-item:not([data-value])::before', _(
        "Normal")),
]
