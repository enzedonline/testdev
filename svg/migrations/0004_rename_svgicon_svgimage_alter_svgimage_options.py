# Generated by Django 4.1.5 on 2023-03-14 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        # ("menu", "0002_alter_menu_title"),
        ("taggit", "0005_auto_20220424_2025"),
        ("svg", "0003_svgtag_svgicon_tags"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SVGIcon",
            new_name="SVGImage",
        ),
        migrations.AlterModelOptions(
            name="svgimage",
            options={"verbose_name": "SVG Image"},
        ),
    ]
