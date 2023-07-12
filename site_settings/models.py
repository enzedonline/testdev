from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet

@register_setting(icon='password')
class Tokens(BaseSiteSetting):
    mapbox = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Mapbox Access Token")
    )
    google_analytics = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Google Analytics Site ID")
    )
    facebook_app_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Facebook App ID")
    )
    fontawesome = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("FontAwesome Kit ID")
    )    
    openai = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("OpenAI Key")
    )    


@register_snippet
class Product(models.Model):
    sku = models.CharField(max_length=10, verbose_name=_("SKU"))
    title = models.CharField(max_length=100, verbose_name=_("Product Title"))
    description = models.TextField(verbose_name=_("Product Description"))
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    panels = [
        FieldPanel('sku'),
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('image')
    ]

    def __str__(self):
        return f'{self.sku} - {self.title}'
