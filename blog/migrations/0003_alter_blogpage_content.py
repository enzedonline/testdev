# Generated by Django 4.2.2 on 2024-03-15 03:54

import blocks.base_blocks
import blocks.collapsible_card
import blocks.data_blocks
import blocks.import_text
from django.db import migrations
import product.blocks
import wagtail.blocks
import wagtail.blocks.static_block
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_alter_blogpage_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="content",
            field=wagtail.fields.StreamField(
                [
                    ("rich_text", wagtail.blocks.RichTextBlock()),
                    ("html", wagtail.blocks.RawHTMLBlock()),
                    (
                        "code",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "language",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("python", "Python"),
                                            ("css", "CSS"),
                                            ("django", "Django Template"),
                                            ("javascript", "Javascript"),
                                            ("xml", "HTML / XML"),
                                            ("shell", "Bash/Shell"),
                                            ("json", "JSON"),
                                            ("markdown", "Markdown"),
                                            ("nginx", "Nginx"),
                                            ("sql", "SQL"),
                                            ("r", "R"),
                                            ("powershell", "PowerShell"),
                                        ]
                                    ),
                                ),
                                ("code", wagtail.blocks.TextBlock()),
                            ]
                        ),
                    ),
                    ("import_text_block", blocks.import_text.ImportTextBlock()),
                    (
                        "csv_table",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "title",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "title",
                                                wagtail.blocks.CharBlock(required=True),
                                            ),
                                            (
                                                "heading_size",
                                                wagtail.blocks.ChoiceBlock(
                                                    choices=[
                                                        ("h2", "H2"),
                                                        ("h3", "H3"),
                                                        ("h4", "H4"),
                                                    ]
                                                ),
                                            ),
                                            (
                                                "alignment",
                                                wagtail.blocks.ChoiceBlock(
                                                    choices=[
                                                        ("justify", "Justified"),
                                                        ("start", "Left"),
                                                        ("center", "Centre"),
                                                        ("end", "Right"),
                                                    ]
                                                ),
                                            ),
                                            (
                                                "anchor_id",
                                                wagtail.blocks.CharBlock(
                                                    help_text="Anchor identifier must be a compatible slug format without spaces or special characters",
                                                    label="Optional Anchor Identifier",
                                                    required=False,
                                                ),
                                            ),
                                        ],
                                        label="Table Title",
                                        required=False,
                                    ),
                                ),
                                (
                                    "data",
                                    blocks.import_text.ImportTextBlock(
                                        file_type_filter=".csv",
                                        help_text="Paste in CSV data or import from .csv file",
                                        label="Comma Separated Data",
                                    ),
                                ),
                                (
                                    "precision",
                                    wagtail.blocks.IntegerBlock(
                                        default=2,
                                        help_text="Number of decimal places to display for float type.",
                                        label="Float Precision",
                                    ),
                                ),
                                (
                                    "column_headers",
                                    wagtail.blocks.BooleanBlock(
                                        default=True,
                                        help_text="First row contains column headers",
                                        label="Column Headers",
                                        required=False,
                                    ),
                                ),
                                (
                                    "row_headers",
                                    wagtail.blocks.BooleanBlock(
                                        help_text="First column contains row headers",
                                        label="Row Headers",
                                        required=False,
                                    ),
                                ),
                                (
                                    "compact",
                                    wagtail.blocks.BooleanBlock(
                                        help_text="Cell padding reduced by half",
                                        label="Compact Table Style",
                                        required=False,
                                    ),
                                ),
                                (
                                    "caption",
                                    wagtail.blocks.RichTextBlock(
                                        editor="minimal",
                                        help_text="Caption displayed beneath the table. Use as explanation or annotation.",
                                        label="Table Caption",
                                        required=False,
                                    ),
                                ),
                                (
                                    "caption_alignment",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("justify", "Justified"),
                                            ("start", "Left"),
                                            ("center", "Centre"),
                                            ("end", "Right"),
                                        ],
                                        label="Caption Alignment",
                                        required=False,
                                    ),
                                ),
                                (
                                    "width",
                                    wagtail.blocks.IntegerBlock(
                                        default=100,
                                        help_text="Table width (as percentage of container)",
                                        label="Table Width (%)",
                                    ),
                                ),
                                (
                                    "max_width",
                                    wagtail.blocks.IntegerBlock(
                                        help_text="Optional: Maximum width (in rem) the table can grow to",
                                        label="Maximum Table Width (rem)",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "collapsible_card_block",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "header_colour",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
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
                                        label="Card Header Background Colour",
                                    ),
                                ),
                                (
                                    "body_colour",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
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
                                        label="Card Body Background Colour",
                                    ),
                                ),
                                (
                                    "cards",
                                    wagtail.blocks.ListBlock(
                                        blocks.collapsible_card.CollapsibleCard,
                                        min_num=2,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    ("product", product.blocks.ProductChooserBlock()),
                    (
                        "external_link",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "external_link",
                                    wagtail.blocks.URLBlock(
                                        help_text="Use the 'Get Metadata' button to retrieve information from the external website.",
                                        label="URL to External Article",
                                    ),
                                ),
                                ("description", wagtail.blocks.RichTextBlock()),
                                (
                                    "image",
                                    wagtail.blocks.CharBlock(
                                        max_length=200, required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "link",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "link_type",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            (None, "No Link"),
                                            ("page", "Page Link"),
                                            ("url_link", "URL Link"),
                                            ("document", "Document Link"),
                                            ("product", "Product Link"),
                                        ],
                                        label="Link Type",
                                        required=False,
                                    ),
                                ),
                                (
                                    "not_selected",
                                    wagtail.blocks.static_block.StaticBlock(
                                        admin_text="", label="No link selected."
                                    ),
                                ),
                                (
                                    "page",
                                    blocks.data_blocks.DataPageChooserBlock(
                                        attrs={"data-link-block-type": "page"},
                                        chooser_attrs={"show_edit_link": False},
                                        label="Link to internal page",
                                        required=False,
                                    ),
                                ),
                                (
                                    "anchor_target",
                                    blocks.data_blocks.DataCharBlock(
                                        attrs={"data-link-block-type": "page"},
                                        label="Optional anchor target (#)",
                                        required=False,
                                    ),
                                ),
                                (
                                    "url_link",
                                    blocks.data_blocks.DataExtendedURLBlock(
                                        attrs={"data-link-block-type": "url_link"},
                                        label="Link to external site or internal URL",
                                        required=False,
                                    ),
                                ),
                                (
                                    "document",
                                    blocks.data_blocks.DataDocumentChooserBlock(
                                        attrs={"data-link-block-type": "document"},
                                        chooser_attrs={"show_edit_link": False},
                                        label="Link to document",
                                        required=False,
                                    ),
                                ),
                                (
                                    "product",
                                    blocks.data_blocks.DataProductChooserBlock(
                                        attrs={"data-link-block-type": "product"},
                                        chooser_attrs={"show_edit_link": False},
                                        label="Link to product",
                                        required=False,
                                    ),
                                ),
                                (
                                    "link_text",
                                    wagtail.blocks.CharBlock(
                                        label="Link text", required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "flex_card",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "text",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "alignment",
                                                wagtail.blocks.ChoiceBlock(
                                                    choices=[
                                                        ("justify", "Justified"),
                                                        ("start", "Left"),
                                                        ("center", "Centre"),
                                                        ("end", "Right"),
                                                    ],
                                                    label="Text Alignment",
                                                ),
                                            ),
                                            ("content", wagtail.blocks.RichTextBlock()),
                                        ],
                                        help_text="Body text for this card.",
                                        label="Card Body Text",
                                    ),
                                ),
                                (
                                    "background",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
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
                                        label="Card Background Colour",
                                    ),
                                ),
                                (
                                    "border",
                                    wagtail.blocks.BooleanBlock(
                                        default=True,
                                        help_text="Draw a border around the card?",
                                        label="Border",
                                        required=False,
                                    ),
                                ),
                                (
                                    "link",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "link_type",
                                                wagtail.blocks.ChoiceBlock(
                                                    choices=[
                                                        (None, "No Link"),
                                                        ("page", "Page Link"),
                                                        ("url_link", "URL Link"),
                                                        ("document", "Document Link"),
                                                        ("product", "Product Link"),
                                                    ],
                                                    label="Link Type",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "not_selected",
                                                wagtail.blocks.static_block.StaticBlock(
                                                    admin_text="",
                                                    label="No link selected.",
                                                ),
                                            ),
                                            (
                                                "page",
                                                blocks.data_blocks.DataPageChooserBlock(
                                                    attrs={
                                                        "data-link-block-type": "page"
                                                    },
                                                    chooser_attrs={
                                                        "show_edit_link": False
                                                    },
                                                    label="Link to internal page",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "anchor_target",
                                                blocks.data_blocks.DataCharBlock(
                                                    attrs={
                                                        "data-link-block-type": "page"
                                                    },
                                                    label="Optional anchor target (#)",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "url_link",
                                                blocks.data_blocks.DataExtendedURLBlock(
                                                    attrs={
                                                        "data-link-block-type": "url_link"
                                                    },
                                                    label="Link to external site or internal URL",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "document",
                                                blocks.data_blocks.DataDocumentChooserBlock(
                                                    attrs={
                                                        "data-link-block-type": "document"
                                                    },
                                                    chooser_attrs={
                                                        "show_edit_link": False
                                                    },
                                                    label="Link to document",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "product",
                                                blocks.data_blocks.DataProductChooserBlock(
                                                    attrs={
                                                        "data-link-block-type": "product"
                                                    },
                                                    chooser_attrs={
                                                        "show_edit_link": False
                                                    },
                                                    label="Link to product",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "link_text",
                                                wagtail.blocks.CharBlock(
                                                    label="Link text", required=False
                                                ),
                                            ),
                                        ],
                                        help_text="If using a link, setting a link label will render a hyperlink button.<br>                    Leave link label blank to make the whole card a clickable link.",
                                        label="Optional Card Link",
                                    ),
                                ),
                                (
                                    "image",
                                    wagtail.blocks.StructBlock(
                                        [
                                            (
                                                "image",
                                                blocks.base_blocks.CustomImageChooserBlock(
                                                    form_classname="compact-image-chooser",
                                                    label="Image",
                                                    required=False,
                                                ),
                                            ),
                                            (
                                                "description",
                                                wagtail.blocks.CharBlock(
                                                    help_text="A contextual description of the image for screen readers and search engines",
                                                    label="Description",
                                                    required=False,
                                                ),
                                            ),
                                        ],
                                        help_text="Card Image (approx 1:1.4 ratio - ideally upload 2100x1470px).",
                                        label="Optional Card Image",
                                    ),
                                ),
                                (
                                    "image_min",
                                    wagtail.blocks.IntegerBlock(
                                        default=200,
                                        label="Minimum width the image can shrink to (pixels)",
                                        min_value=100,
                                    ),
                                ),
                                (
                                    "image_max",
                                    wagtail.blocks.IntegerBlock(
                                        label="Optional maximum width the image can grow to (pixels)",
                                        required=False,
                                    ),
                                ),
                                (
                                    "layout",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
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
                                        label="Card Format",
                                        max_length=15,
                                    ),
                                ),
                                (
                                    "breakpoint",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("sm", "Small screen only"),
                                            ("md", "Small and medium screens"),
                                            ("lg", "Small, medium and large screens"),
                                            ("none", "No breakpoint"),
                                        ],
                                        label="Breakpoint for responsive layouts",
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "seo_image",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "image",
                                    blocks.base_blocks.CustomImageChooserBlock(
                                        form_classname="compact-image-chooser",
                                        label="Image",
                                        required=True,
                                    ),
                                ),
                                (
                                    "description",
                                    wagtail.blocks.CharBlock(
                                        help_text="A contextual description of the image for screen readers and search engines",
                                        label="Description",
                                        required=True,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "heading",
                        wagtail.blocks.StructBlock(
                            [
                                ("title", wagtail.blocks.CharBlock(required=True)),
                                (
                                    "heading_size",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("h2", "H2"),
                                            ("h3", "H3"),
                                            ("h4", "H4"),
                                        ]
                                    ),
                                ),
                                (
                                    "alignment",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=[
                                            ("justify", "Justified"),
                                            ("start", "Left"),
                                            ("center", "Centre"),
                                            ("end", "Right"),
                                        ]
                                    ),
                                ),
                                (
                                    "anchor_id",
                                    wagtail.blocks.CharBlock(
                                        help_text="Anchor identifier must be a compatible slug format without spaces or special characters",
                                        label="Optional Anchor Identifier",
                                        required=False,
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "django_template_fragment",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "code",
                                    wagtail.blocks.RawHTMLBlock(
                                        label="Enter Django Template Fragment Code"
                                    ),
                                )
                            ]
                        ),
                    ),
                ],
                blank=True,
                use_json_field=True,
                verbose_name="Page Content",
            ),
        ),
    ]
