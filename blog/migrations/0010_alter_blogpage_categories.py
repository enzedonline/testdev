# Generated by Django 5.0.3 on 2024-06-05 04:52

import modelcluster.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0009_alter_blogpage_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="categories",
            field=modelcluster.fields.ParentalManyToManyField(
                related_name="categories",
                to="blog.blogcategory",
                verbose_name="Categories",
            ),
        ),
    ]