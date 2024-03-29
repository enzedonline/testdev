# Generated by Django 4.2.2 on 2024-03-03 20:47

import core.fields.numeric_range
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("site_settings", "0001_feb2024"),
    ]

    operations = [
        migrations.CreateModel(
            name="NumericRange",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("minmax", core.fields.numeric_range.NumericRangeField()),
            ],
        ),
    ]
