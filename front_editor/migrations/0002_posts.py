# Generated by Django 5.0.3 on 2024-05-18 05:13

import django.db.models.deletion
import wagtail.contrib.routable_page.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("front_editor", "0001_initial"),
        ("wagtailcore", "0095_merge_0093_uploadedfile_0094_merge_20240323_1110"),
    ]

    operations = [
        migrations.CreateModel(
            name="Posts",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtail.contrib.routable_page.models.RoutablePageMixin,
                "wagtailcore.page",
            ),
        ),
    ]
