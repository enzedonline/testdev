# Generated by Django 5.0.3 on 2024-05-18 02:00

import django.db.models.deletion
import django_quill2.fields
import wagtail.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # ("wagtailcore", "0095_merge_0093_uploadedfile_0094_merge_20240323_1110"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "live",
                    models.BooleanField(
                        default=True, editable=False, verbose_name="live"
                    ),
                ),
                (
                    "has_unpublished_changes",
                    models.BooleanField(
                        default=False,
                        editable=False,
                        verbose_name="has unpublished changes",
                    ),
                ),
                (
                    "first_published_at",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="first published at",
                    ),
                ),
                (
                    "last_published_at",
                    models.DateTimeField(
                        editable=False, null=True, verbose_name="last published at"
                    ),
                ),
                (
                    "go_live_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="go live date/time"
                    ),
                ),
                (
                    "expire_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="expiry date/time"
                    ),
                ),
                (
                    "expired",
                    models.BooleanField(
                        default=False, editable=False, verbose_name="expired"
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("content", django_quill2.fields.QuillField()),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "latest_revision",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.revision",
                        verbose_name="latest revision",
                    ),
                ),
                (
                    "live_revision",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.revision",
                        verbose_name="live revision",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(wagtail.models.PreviewableMixin, models.Model),
        ),
    ]
