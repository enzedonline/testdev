# Generated by Django 5.0.3 on 2024-05-24 01:26

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("front_editor", "0007_remove_post_posts_page_post_page"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="draftail",
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
    ]
