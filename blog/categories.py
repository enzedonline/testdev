from django.db import models
from django.forms.widgets import TextInput
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.admin.widgets.slug import SlugInput
from wagtail.snippets.models import register_snippet

# Autosync from title to slug does not work by default from Wagtail 5.0
# 
# Title field misses necessary data attributes
# <input id="id_title" type="text" name="title" maxlength="100" required="">
# 
# Need to render the following:
# <input id="id_title" type="text" name="title" maxlength="100" required="" 
#   data-controller="w-sync" 
#   data-action="focus->w-sync#check blur->w-sync#apply change->w-sync#apply keyup->w-sync#apply" 
#   data-w-sync-target-value="[name='slug']">
# 
#  See custom TextInput widget definition below
#  Additionally, sync'd text will only be slugified by using SlugInput widget

@register_snippet
class BlogCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Category Name"))
    slug = models.SlugField(
        max_length=100,
        help_text=_("How the category will appear in URL"),
        unique=True,  # <= can't use unique on translatable field
        allow_unicode=True,
    )

    panels = [
        FieldPanel(
            "title",
            widget=TextInput(
                attrs={
                    "data-controller": "w-sync",
                    "data-action": "focus->w-sync#check blur->w-sync#apply change->w-sync#apply keyup->w-sync#apply",
                    "data-w-sync-target-value": "[name='slug']",
                }
            ),
        ),
        FieldPanel("slug", widget=SlugInput),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ["title"]
