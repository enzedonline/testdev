# Generated by Django 5.0.3 on 2024-10-15 23:19

import blocks.collapsible_card
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0017_spacecraft_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Affiliate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="blogpage",
            name="content",
            field=wagtail.fields.StreamField(
                [
                    ("rich_text", 0),
                    ("code", 6),
                    ("import_text_block", 7),
                    ("csv_table", 23),
                    ("collapsible_card_block", 27),
                    ("product", 28),
                    ("external_link", 31),
                    ("link", 40),
                    ("flex_card", 53),
                    ("seo_image", 56),
                    ("heading", 59),
                    ("django_template_fragment", 61),
                    ("external_video", 64),
                ],
                blank=True,
                block_lookup={
                    0: ("wagtail.blocks.RichTextBlock", (), {}),
                    1: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Title", "required": False},
                    ),
                    2: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("disabled", "Not Collapsible"),
                                ("collapsible", "Collapsible"),
                                ("collapsed", "Collapsed"),
                            ],
                            "label": "Format",
                        },
                    ),
                    3: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("plaintext", "Plain Text"),
                                ("python", "Python"),
                                ("css", "CSS"),
                                ("scss", "SCSS"),
                                ("django", "Django Template"),
                                ("javascript", "Javascript"),
                                ("typescript", "Typescript"),
                                ("xml", "HTML / XML"),
                                ("shell", "Bash/Shell"),
                                ("json", "JSON"),
                                ("markdown", "Markdown"),
                                ("nginx", "Nginx"),
                                ("sql", "SQL"),
                                ("r", "R"),
                                ("powershell", "PowerShell"),
                            ],
                            "label": "Language",
                        },
                    ),
                    4: ("wagtail.blocks.RawHTMLBlock", (), {"label": "Code"}),
                    5: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "default": True,
                            "label": "Include extra space beneath code block?",
                            "required": False,
                        },
                    ),
                    6: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 1),
                                ("collapsible", 2),
                                ("language", 3),
                                ("code", 4),
                                ("bottom_padding", 5),
                            ]
                        ],
                        {},
                    ),
                    7: ("blocks.import_text.ImportTextBlock", (), {}),
                    8: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [("h3", "H3"), ("h4", "H4"), ("h5", "H5")],
                            "label": "Size",
                        },
                    ),
                    9: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("justify", "Justified"),
                                ("start", "Left"),
                                ("center", "Centre"),
                                ("end", "Right"),
                            ],
                            "label": "Alignment",
                        },
                    ),
                    10: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Optional Anchor Identifier", "required": False},
                    ),
                    11: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 1),
                                ("heading_size", 8),
                                ("alignment", 9),
                                ("anchor_id", 10),
                            ]
                        ],
                        {"label": "Optional Table Title"},
                    ),
                    12: (
                        "blocks.import_text.ImportTextBlock",
                        (),
                        {
                            "file_type_filter": ".csv",
                            "help_text": "Paste in CSV data or import from .csv file",
                            "label": "Comma Separated Data",
                        },
                    ),
                    13: (
                        "wagtail.blocks.IntegerBlock",
                        (),
                        {"default": 2, "label": "Float Precision"},
                    ),
                    14: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {"default": True, "label": "Column Headers", "required": False},
                    ),
                    15: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {"label": "Row Headers", "required": False},
                    ),
                    16: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {"default": True, "label": "Compact", "required": False},
                    ),
                    17: (
                        "wagtail.blocks.RichTextBlock",
                        (),
                        {
                            "editor": "minimal",
                            "help_text": "Caption displayed beneath the table. Use as explanation or annotation.",
                            "label": "Table Caption",
                            "required": False,
                        },
                    ),
                    18: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("justify", "Justified"),
                                ("start", "Left"),
                                ("center", "Centre"),
                                ("end", "Right"),
                            ],
                            "label": "Caption Alignment",
                        },
                    ),
                    19: (
                        "wagtail.blocks.IntegerBlock",
                        (),
                        {"default": 100, "label": "Table Width (%)"},
                    ),
                    20: (
                        "wagtail.blocks.IntegerBlock",
                        (),
                        {"label": "Maximum Table Width (rem)", "required": False},
                    ),
                    21: ("blocks.hidden.HiddenCharBlock", (), {}),
                    22: ("blocks.hidden.HiddenBooleanBlock", (), {"default": True}),
                    23: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 11),
                                ("data", 12),
                                ("precision", 13),
                                ("column_headers", 14),
                                ("row_headers", 15),
                                ("compact", 16),
                                ("caption", 17),
                                ("caption_alignment", 18),
                                ("width", 19),
                                ("max_width", 20),
                                ("html", 21),
                                ("rendered", 22),
                            ]
                        ],
                        {},
                    ),
                    24: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("bg-transparent", "Transparent"),
                                ("bg-primary", "Primary"),
                                ("bg-secondary", "Secondary"),
                                ("bg-success", "Success"),
                                ("bg-info", "Info"),
                                ("bg-warning", "Warning"),
                                ("bg-danger", "Danger"),
                                ("bg-light", "Light"),
                                ("bg-dark", "Dark"),
                                ("bg-black", "Black"),
                            ],
                            "label": "Card Header Background Colour",
                        },
                    ),
                    25: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("bg-transparent", "Transparent"),
                                ("bg-primary", "Primary"),
                                ("bg-secondary", "Secondary"),
                                ("bg-success", "Success"),
                                ("bg-info", "Info"),
                                ("bg-warning", "Warning"),
                                ("bg-danger", "Danger"),
                                ("bg-light", "Light"),
                                ("bg-dark", "Dark"),
                                ("bg-black", "Black"),
                            ],
                            "label": "Card Body Background Colour",
                        },
                    ),
                    26: (
                        "wagtail.blocks.ListBlock",
                        (blocks.collapsible_card.CollapsibleCard,),
                        {"min_num": 2},
                    ),
                    27: (
                        "wagtail.blocks.StructBlock",
                        [[("header_colour", 24), ("body_colour", 25), ("cards", 26)]],
                        {},
                    ),
                    28: ("product.blocks.ProductChooserBlock", (), {}),
                    29: (
                        "wagtail.blocks.URLBlock",
                        (),
                        {
                            "help_text": "Use the 'Get Metadata' button to retrieve information from the external website.",
                            "label": "URL to External Article",
                        },
                    ),
                    30: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"max_length": 200, "required": False},
                    ),
                    31: (
                        "wagtail.blocks.StructBlock",
                        [[("external_link", 29), ("description", 0), ("image", 30)]],
                        {},
                    ),
                    32: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                (None, "No Link"),
                                ("page", "Page Link"),
                                ("url_link", "URL Link"),
                                ("document", "Document Link"),
                                ("product", "Product Link"),
                            ],
                            "label": "Link Type",
                            "required": False,
                        },
                    ),
                    33: (
                        "wagtail.blocks.static_block.StaticBlock",
                        (),
                        {"admin_text": "", "label": "No link selected."},
                    ),
                    34: (
                        "blocks.data_blocks.DataPageChooserBlock",
                        (),
                        {
                            "attrs": {"data-link-block-type": "page"},
                            "chooser_attrs": {"show_edit_link": False},
                            "label": "Link to internal page",
                            "required": False,
                        },
                    ),
                    35: (
                        "blocks.data_blocks.DataCharBlock",
                        (),
                        {
                            "attrs": {"data-link-block-type": "page"},
                            "label": "Optional anchor target (#)",
                            "required": False,
                        },
                    ),
                    36: (
                        "blocks.data_blocks.DataExtendedURLBlock",
                        (),
                        {
                            "attrs": {"data-link-block-type": "url_link"},
                            "label": "Link to external site or internal URL",
                            "required": False,
                        },
                    ),
                    37: (
                        "blocks.data_blocks.DataDocumentChooserBlock",
                        (),
                        {
                            "attrs": {"data-link-block-type": "document"},
                            "chooser_attrs": {"show_edit_link": False},
                            "label": "Link to document",
                            "required": False,
                        },
                    ),
                    38: (
                        "blocks.data_blocks.DataProductChooserBlock",
                        (),
                        {
                            "attrs": {"data-link-block-type": "product"},
                            "chooser_attrs": {"show_edit_link": False},
                            "label": "Link to product",
                            "required": False,
                        },
                    ),
                    39: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Link text", "required": False},
                    ),
                    40: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("link_type", 32),
                                ("not_selected", 33),
                                ("page", 34),
                                ("anchor_target", 35),
                                ("url_link", 36),
                                ("document", 37),
                                ("product", 38),
                                ("link_text", 39),
                            ]
                        ],
                        {},
                    ),
                    41: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("justify", "Justified"),
                                ("start", "Left"),
                                ("center", "Centre"),
                                ("end", "Right"),
                            ],
                            "label": "Text Alignment",
                        },
                    ),
                    42: (
                        "wagtail.blocks.StructBlock",
                        [[("alignment", 41), ("content", 0)]],
                        {
                            "help_text": "Body text for this card.",
                            "label": "Card Body Text",
                        },
                    ),
                    43: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("bg-transparent", "Transparent"),
                                ("bg-primary", "Primary"),
                                ("bg-secondary", "Secondary"),
                                ("bg-success", "Success"),
                                ("bg-info", "Info"),
                                ("bg-warning", "Warning"),
                                ("bg-danger", "Danger"),
                                ("bg-light", "Light"),
                                ("bg-dark", "Dark"),
                                ("bg-black", "Black"),
                            ],
                            "label": "Card Background Colour",
                        },
                    ),
                    44: (
                        "wagtail.blocks.BooleanBlock",
                        (),
                        {
                            "default": True,
                            "help_text": "Draw a border around the card?",
                            "label": "Border",
                            "required": False,
                        },
                    ),
                    45: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("link_type", 32),
                                ("not_selected", 33),
                                ("page", 34),
                                ("anchor_target", 35),
                                ("url_link", 36),
                                ("document", 37),
                                ("product", 38),
                                ("link_text", 39),
                            ]
                        ],
                        {
                            "help_text": "If using a link, setting a link label will render a hyperlink button.<br>                    Leave link label blank to make the whole card a clickable link.",
                            "label": "Optional Card Link",
                        },
                    ),
                    46: (
                        "blocks.base_blocks.CustomImageChooserBlock",
                        (),
                        {
                            "form_classname": "compact-image-chooser",
                            "label": "Image",
                            "required": False,
                        },
                    ),
                    47: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "A contextual description of the image for screen readers and search engines",
                            "label": "Description",
                            "required": False,
                        },
                    ),
                    48: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 46), ("description", 47)]],
                        {
                            "help_text": "Card Image (approx 1:1.4 ratio - ideally upload 2100x1470px).",
                            "label": "Optional Card Image",
                        },
                    ),
                    49: (
                        "wagtail.blocks.IntegerBlock",
                        (),
                        {
                            "default": 200,
                            "label": "Minimum width the image can shrink to (pixels)",
                            "min_value": 100,
                        },
                    ),
                    50: (
                        "wagtail.blocks.IntegerBlock",
                        (),
                        {
                            "label": "Optional maximum width the image can grow to (pixels)",
                            "required": False,
                        },
                    ),
                    51: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                (
                                    "left-responsive",
                                    "Responsive Horizontal (Image left of text on widescreen only)",
                                ),
                                (
                                    "right-responsive",
                                    "Responsive Horizontal (Image right of text on widescreen only)",
                                ),
                                (
                                    "left-fixed",
                                    "Fixed Horizontal (Image left of text on all screen sizes)",
                                ),
                                (
                                    "right-fixed",
                                    "Fixed Horizontal (Image right of text on all screen sizes)",
                                ),
                                (
                                    "vertical",
                                    "Vertical (Image above text on on all screen sizes)",
                                ),
                            ],
                            "label": "Card Format",
                            "max_length": 15,
                        },
                    ),
                    52: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [
                                ("sm", "Small screen only"),
                                ("md", "Small and medium screens"),
                                ("lg", "Small, medium and large screens"),
                                ("none", "No breakpoint"),
                            ],
                            "label": "Breakpoint for responsive layouts",
                        },
                    ),
                    53: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("text", 42),
                                ("background", 43),
                                ("border", 44),
                                ("link", 45),
                                ("image", 48),
                                ("image_min", 49),
                                ("image_max", 50),
                                ("layout", 51),
                                ("breakpoint", 52),
                            ]
                        ],
                        {},
                    ),
                    54: (
                        "blocks.base_blocks.CustomImageChooserBlock",
                        (),
                        {
                            "form_classname": "compact-image-chooser",
                            "label": "Image",
                            "required": True,
                        },
                    ),
                    55: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {
                            "help_text": "A contextual description of the image for screen readers and search engines",
                            "label": "Description",
                            "required": True,
                        },
                    ),
                    56: (
                        "wagtail.blocks.StructBlock",
                        [[("image", 54), ("description", 55)]],
                        {},
                    ),
                    57: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Title", "required": True},
                    ),
                    58: (
                        "wagtail.blocks.ChoiceBlock",
                        [],
                        {
                            "choices": [("h2", "H2"), ("h3", "H3"), ("h4", "H4")],
                            "label": "Size",
                        },
                    ),
                    59: (
                        "wagtail.blocks.StructBlock",
                        [
                            [
                                ("title", 57),
                                ("heading_size", 58),
                                ("alignment", 9),
                                ("anchor_id", 10),
                            ]
                        ],
                        {},
                    ),
                    60: (
                        "wagtail.blocks.RawHTMLBlock",
                        (),
                        {"label": "Enter Django Template Fragment Code"},
                    ),
                    61: ("wagtail.blocks.StructBlock", [[("code", 60)]], {}),
                    62: (
                        "wagtail.embeds.blocks.EmbedBlock",
                        (),
                        {
                            "help_text": "eg 'https://www.youtube.com/watch?v=kqN1HUMr22I'",
                            "label": "Video URL",
                        },
                    ),
                    63: (
                        "wagtail.blocks.CharBlock",
                        (),
                        {"label": "Caption", "required": False},
                    ),
                    64: (
                        "wagtail.blocks.StructBlock",
                        [[("video", 62), ("caption", 63), ("background", 43)]],
                        {},
                    ),
                },
                verbose_name="Page Content",
            ),
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                ("name", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=255)),
                (
                    "affiliates",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="companies",
                        to="blog.affiliate",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
    ]