from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.models import Orderable

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