# Generated by Django 4.2.2 on 2024-02-23 02:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.contrib.routable_page.models
import wagtail.fields

from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        # ("wagtailcore", "0091_alter_querydailyhits_unique_together_and_more"),
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
    ]
  
    operations = [
        migrations.CreateModel(
            name="ProductPage",
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
                ("intro", wagtail.fields.RichTextField()),
            ],
            options={
                "abstract": False,
            },
            bases=(
                wagtail.contrib.routable_page.models.RoutablePageMixin,
                "wagtailcore.page",
            ),
        ),
        migrations.CreateModel(
            name="StoreDepartment",
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
                    "code",
                    models.CharField(
                        max_length=10, unique=True, verbose_name="Department Code"
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name")),
            ],
            options={
                "verbose_name": "Store Department",
                "verbose_name_plural": "Store Departments",
            },
        ),
        migrations.CreateModel(
            name="DepartmentSubcategory",
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
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=10, unique=True, verbose_name="Subcategory Code"
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name")),
                (
                    "department",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="department_subcategories",
                        to="product.storedepartment",
                    ),
                ),
            ],
            options={
                "verbose_name": "Department Subcategory",
                "verbose_name_plural": "Department Subcategories",
                "unique_together": set(),
            },
        ),
        migrations.CreateModel(
            name="Product",
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
                    "sku",
                    models.CharField(max_length=10, unique=True, verbose_name="SKU"),
                ),
                (
                    "title",
                    models.CharField(max_length=100, verbose_name="Product Title"),
                ),
                (
                    "description",
                    wagtail.fields.RichTextField(verbose_name="Product Description"),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
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
                    "first_published_at",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        null=True,
                        verbose_name="first published at",
                    ),
                ),
                (
                    "go_live_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="go live date/time"
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
                    "last_published_at",
                    models.DateTimeField(
                        editable=False, null=True, verbose_name="last published at"
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
                    "live",
                    models.BooleanField(
                        default=True, editable=False, verbose_name="live"
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
                (
                    "dept_subcategory",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="product.departmentsubcategory",
                        verbose_name="Department Subcategory",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="departmentsubcategory",
            constraint=models.UniqueConstraint(
                fields=("department", "name"),
                name="unique_department_departmentsubcategory_name",
            ),
        ),
    ]
