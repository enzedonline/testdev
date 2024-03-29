# Generated by Django 4.2.2 on 2023-10-25 00:12

import blocks.import_text
import blocks.parsed_richtext
from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# home.migrations.0002_create_homepage
def create_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model("contenttypes.ContentType")
    Page = apps.get_model("wagtailcore.Page")
    Site = apps.get_model("wagtailcore.Site")
    HomePage = apps.get_model("home.HomePage")

    # Delete the default homepage
    # If migration is run multiple times, it may have already been deleted
    Page.objects.filter(id=2).delete()

    # Create content type for homepage model
    homepage_content_type, __ = ContentType.objects.get_or_create(
        model="homepage", app_label="home"
    )

    # Create a new homepage
    homepage = HomePage.objects.create(
        title="Home",
        draft_title="Home",
        slug="home",
        content_type=homepage_content_type,
        path="00010001",
        depth=2,
        numchild=0,
        url_path="/home/",
    )

    # Create a site with the new homepage set as the root
    Site.objects.create(hostname="localhost", root_page=homepage, is_default_site=True)


def remove_homepage(apps, schema_editor):
    # Get models
    ContentType = apps.get_model("contenttypes.ContentType")
    HomePage = apps.get_model("home.HomePage")

    # Delete the default homepage
    # Page and Site objects CASCADE
    HomePage.objects.filter(slug="home", depth=2).delete()

    # Delete content type for homepage model
    ContentType.objects.filter(model="homepage", app_label="home").delete()


class Migration(migrations.Migration):

    # replaces = [('home', '0001_initial'), ('home', '0002_create_homepage'), ('home', '0003_homepage_content'), ('home', '0004_homepage_banner_headline'), ('home', '0005_remove_homepage_banner_headline'), ('home', '0006_homepage_typedtable'), ('home', '0007_remove_homepage_typedtable'), ('home', '0008_alter_homepage_content'), ('home', '0009_alter_homepage_content'), ('home', '0010_alter_homepage_content'), ('home', '0011_alter_homepage_content'), ('home', '0012_alter_homepage_content'), ('home', '0013_homepage_intro'), ('home', '0014_alter_homepage_content'), ('home', '0015_alter_homepage_content'), ('home', '0016_alter_homepage_content'), ('home', '0017_alter_homepage_content'), ('home', '0018_alter_homepage_content'), ('home', '0019_alter_homepage_content'), ('home', '0020_alter_homepage_content'), ('home', '0021_alter_homepage_content'), ('home', '0022_alter_homepage_content'), ('home', '0023_alter_homepage_content'), ('home', '0024_alter_homepage_content'), ('home', '0025_alter_homepage_content'), ('home', '0026_alter_homepage_content'), ('home', '0027_alter_homepage_content')]

    initial = True

    dependencies = [
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.RunPython(
            code=create_homepage,
            reverse_code=remove_homepage,
        ),
        migrations.AddField(
            model_name='homepage',
            name='intro',
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='content',
            field=wagtail.fields.StreamField([('cleaned_rich_text', blocks.parsed_richtext.ParsedRichTextBlock()), ('csv_table', wagtail.blocks.StructBlock([('title', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(required=True)), ('heading_size', wagtail.blocks.ChoiceBlock(choices=[('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4'), ('h5', 'H5'), ('h6', 'H6')], label=None)), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('justify', 'Justified'), ('start', 'Left'), ('center', 'Centre'), ('end', 'Right')], label=None)), ('anchor_target', wagtail.blocks.CharBlock(help_text='Anchor Target must be a compatible slug format without spaces or special characters', label='Optional Anchor Target', required=False))], label='Table Title', required=False)), ('data', blocks.import_text.ImportTextBlock(file_type_filter='.csv', help_text='Paste in CSV data or import from .csv file', label='Comma Separated Data')), ('precision', wagtail.blocks.IntegerBlock(default=2, help_text='Number of decimal places to display for float type.', label='Float Precision')), ('column_headers', wagtail.blocks.BooleanBlock(default=True, help_text='First row contains column headers', label='Column Headers', required=False)), ('row_headers', wagtail.blocks.BooleanBlock(help_text='First column contains row headers', label='Row Headers', required=False)), ('compact', wagtail.blocks.BooleanBlock(help_text='Cell padding reduced by half', label='Compact Table Style', required=False)), ('caption', wagtail.blocks.RichTextBlock(editor='minimal', help_text='Caption displayed beneath the table. Use as explanation or annotation.', label='Table Caption', required=False)), ('caption_alignment', wagtail.blocks.ChoiceBlock(choices=[('justify', 'Justified'), ('start', 'Left'), ('center', 'Centre'), ('end', 'Right')], label='Caption Alignment', required=False)), ('width', wagtail.blocks.IntegerBlock(default=100, help_text='Table width (as percentage of container)', label='Table Width (%)')), ('max_width', wagtail.blocks.IntegerBlock(help_text='Optional: Maximum width (in rem) the table can grow to', label='Maximum Table Width (rem)', required=False))])), ('import_text_block', blocks.import_text.ImportTextBlock())], blank=True, use_json_field=True, verbose_name='Page body'),
        ),
    ]
