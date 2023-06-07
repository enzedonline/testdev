from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.admin.widgets.slug import SlugInput
from wagtail.admin.forms import WagtailAdminModelForm


# <input id="id_title" type="text" name="title" maxlength="100" required="">
# <input id="id_title" type="text" name="title"
#     data-controller="w-sync"
#     data-action="focus->w-sync#check blur->w-sync#apply change->w-sync#apply"
#     data-w-sync-target-value="body:not(.page-is-live) #some_other_slug"
# />

class CategoryForm(WagtailAdminModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['data-controller'] = 'w-sync'
        self.fields['title'].widget.attrs['data-action'] = 'focus->w-sync#check blur->w-sync#apply change->w-sync#apply'
        self.fields['title'].widget.attrs['data-w-sync-target-value'] = '#id_slug'
        
@register_snippet
class BlogCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Category Name"))
    slug = models.SlugField(
        max_length=100,
        help_text=_("How the category will appear in URL"),
        unique=True, # <= can't use unique on translatable field
        allow_unicode=True,
    )

    base_form_class = CategoryForm

    panels = [
        FieldPanel("title", classname="title"),
        FieldPanel("slug", widget=SlugInput),
    ]

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ["title"]
