# Generated by Django 5.0.3 on 2024-05-22 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("front_editor", "0004_remove_post_created_at_remove_post_updated_at"),
        ("wagtailcore", "0095_merge_0093_uploadedfile_0094_merge_20240323_1110"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Posts",
            new_name="PostsPage",
        ),
    ]