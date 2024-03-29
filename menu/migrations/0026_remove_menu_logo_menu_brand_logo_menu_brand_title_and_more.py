# Generated by Django 4.2.2 on 2023-11-04 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
        ("menu", "0025_alter_menu_items"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="menu",
            name="logo",
        ),
        migrations.AddField(
            model_name="menu",
            name="brand_logo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
                verbose_name="Optional Menu Logo",
            ),
        ),
        migrations.AddField(
            model_name="menu",
            name="brand_title",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="Optional Menu Display Title",
            ),
        ),
        migrations.AlterField(
            model_name="menu",
            name="title",
            field=models.CharField(
                help_text="A descriptive name for this menu (not displayed)",
                max_length=255,
                verbose_name="Menu Title",
            ),
        ),
    ]
