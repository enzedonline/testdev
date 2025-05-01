import django_filters
from django.db import models
from django.db.models import Count, Manager
from django.utils.translation import gettext_lazy as _
from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.panels import FieldPanel, TitleFieldPanel
from wagtail.snippets.models import register_snippet

from core.panels.utility_panel import UtilityPanel


class BlogCategoryManager(Manager):
    def with_use_count(self):
        return self.get_queryset().annotate(count=Count("categories"))
    
@register_snippet    
class BlogCategory(models.Model):
    objects = BlogCategoryManager()
    add_to_reference_index = True

    title = models.CharField(max_length=100, verbose_name=_("Category Name"))
    slug = models.SlugField(
        max_length=100,
        help_text=_("How the category will appear in URL"),
        unique=True,  # <= can't use unique on translatable field
        allow_unicode=True,
    )

    panels = [
        UtilityPanel(
            text=_("Usage Count") + ': {{useage}}<hr style="margin: 0.5em 0;">', 
            value_dict={'useage': 'use_count'},
            style="margin-bottom: -2rem;",
            class_list="help"
        ),
        TitleFieldPanel("title"),
        FieldPanel("slug"),
    ]

    @classmethod
    def references(cls):
        """
        Returns a queryset of BlogCategory annotated with the number of related BlogPages.
        """
        return cls.objects.annotate(count=Count('categories'))
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ["title"]


class BlogCategoryFilterSet(WagtailFilterSet):
    # copy /templates/django_filters/widgets/multiwidget.html into a local template directory
    # or add django_filters into installed_apps
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')
    count = django_filters.RangeFilter(field_name='count', label="Usage Count")

    class Meta:
        model = BlogCategory
        fields = ["title", "slug", "count"]
