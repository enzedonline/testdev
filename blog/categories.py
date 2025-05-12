import django_filters
from django.db import models
from django.db.models import Count
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.panels import FieldPanel, TitleFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import IndexView, SnippetViewSet
from wagtail.admin.ui.tables import Column, UpdatedAtColumn

from core.panels.utility_panel import UtilityPanel


class BlogCategory(models.Model):
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
            value_dict={'useage': 'get_useage_count'},
            style="margin-bottom: -2rem;",
            class_list="help"
        ),
        TitleFieldPanel("title"),
        FieldPanel("slug"),
    ]

    def get_useage_count(self):
        """
        Returns the number of times this category is used in blog posts.
        """
        return self.blog_pages.count()

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
        fields = ["title", "slug"]

class BlogCategoryIndexView(IndexView):
    # don't use default "__str__", this will disable ordering on that column
    list_display = ["title", "slug"]

    @cached_property
    def columns(self):
        columns = super().columns + [
            Column(
                "count",
                label=_("Useage Count"),
                sort_key="count",
            ),
            UpdatedAtColumn()
        ]
        return columns
    
    def get_base_queryset(self):
        # Add the usage count here, using get_queryset will throw error when trying to create the column
        qs = super().get_base_queryset().annotate(count=Count('blog_pages')).order_by(*BlogCategory._meta.ordering)
        return qs

class BlogCategoryViewSet(SnippetViewSet):
    model = BlogCategory
    filterset_class = BlogCategoryFilterSet
    index_view_class = BlogCategoryIndexView

register_snippet(BlogCategoryViewSet)