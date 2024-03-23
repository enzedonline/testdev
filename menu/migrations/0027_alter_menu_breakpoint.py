# Generated by Django 4.2.2 on 2023-11-04 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0026_remove_menu_logo_menu_brand_logo_menu_brand_title_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="breakpoint",
            field=models.CharField(
                blank=True,
                choices=[
                    ("-md", "Small Screens (<768px)"),
                    ("-lg", "Medium Screens (<992px)"),
                    ("", "Always expanded (no small screen format)"),
                ],
                default="lg",
                max_length=4,
                verbose_name="Mobile Layout Breakpoint",
            ),
        ),
    ]