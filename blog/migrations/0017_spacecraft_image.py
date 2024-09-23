# Generated by Django 5.0.3 on 2024-09-22 22:38

import blog.spacecraft
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0016_spacecraft_uuid"),
        ("wagtailimages", "0026_delete_uploadedimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="spacecraft",
            name="image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="wagtailimages.image",
                validators=[blog.spacecraft.check_min_pixels],
            ),
        ),
    ]
