# Generated by Django 5.0.3 on 2024-05-24 02:58

# import django_tiptap.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("front_editor", "0008_post_draftail"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="draftail",
        ),
        # migrations.AddField(
        #     model_name="post",
        #     name="tiptap",
        #     field=django_tiptap.fields.TipTapTextField(blank=True, null=True),
        # ),
    ]
