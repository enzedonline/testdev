# Generated by Django 5.0.3 on 2024-05-22 04:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("front_editor", "0005_rename_posts_postspage"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="posts_page",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to="front_editor.postspage",
            ),
        ),
    ]
