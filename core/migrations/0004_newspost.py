# Generated by Django 5.1.6 on 2025-06-02 21:12

import django.db.models.deletion
import wagtail.fields
import wagtail.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_category_options_alter_category_parents_and_more"),
        ("wagtailcore", "0094_alter_page_locale"),
        ("wagtailimages", "0027_image_description"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsPost",
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
                (
                    "locked",
                    models.BooleanField(
                        default=False, editable=False, verbose_name="locked"
                    ),
                ),
                (
                    "locked_at",
                    models.DateTimeField(
                        editable=False, null=True, verbose_name="locked at"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                (
                    "featured",
                    models.BooleanField(
                        default=False,
                        help_text="Check this box to feature this news post on the homepage.",
                        verbose_name="Featured",
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [("text", 0), ("image", 1)],
                        block_lookup={
                            0: ("wagtail.blocks.RichTextBlock", (), {"label": "Text"}),
                            1: (
                                "wagtail.images.blocks.ImageBlock",
                                [],
                                {"label": "Image"},
                            ),
                        },
                        verbose_name="News Article Body",
                    ),
                ),
                (
                    "card_image",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                        verbose_name="Card Image",
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
                (
                    "locked_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="locked_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="locked by",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtail.models.PreviewableMixin,
                wagtail.models.WorkflowMixin,
                models.Model,
            ),
        ),
    ]
