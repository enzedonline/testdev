# Generated by Django 5.0.3 on 2024-06-25 03:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0011_partner_partnership"),
        ("wagtailimages", "0026_delete_uploadedimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carouselimages",
            name="carousel_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="images",
                to="wagtailimages.image",
                verbose_name="Image",
            ),
        ),
    ]