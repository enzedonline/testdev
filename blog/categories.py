from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

@register_snippet
class BlogCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Category Name"))
    slug = models.SlugField(
        max_length=100,
        help_text=_("How the category will appear in URL"),
        unique=True, # <= can't use unique on translatable field
        allow_unicode=True,
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
    ]

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ["title"]
