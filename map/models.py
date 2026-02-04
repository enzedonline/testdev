from django.db import models
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from .settings import MapboxAssistConfigs, MapboxSettings


class HikingPlannerPage(RoutablePageMixin, Page):
    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = 1
    template = 'map/hiking_planner_page.html'

    @path('')
    @path('<config>/')
    def planner_map(self, request, config=None):
        mapbox_assist_config = None
        if config:
            mapbox_assist_config = MapboxAssistConfigs.objects.filter(
                slug=config).first()
        if not mapbox_assist_config:
            mapbox_assist_config = MapboxAssistConfigs.objects.first()
        self.title = mapbox_assist_config.title

        feature_layers = []
        for layer in mapbox_assist_config.feature_layers.all():
            feature_layers.append({
                "id": layer.uid,
                "tileId": layer.tile_id,
                "handler": layer.handler_function_name,
                "source": static(layer.handler_function_path) if layer.handler_function_path.startswith('/') else layer.handler_function_path
            })

        map_styles = []
        for style in mapbox_assist_config.mapbox_styles.all():
            try:
                img = style.tile_image.get_rendition('fill-50x50').img_tag()
            except:
                img = ''
            map_styles.append({
                "title": style.title,
                "source": style.source,
                "tileImageHTML": img,
            })

        parameters = {
            "mapOptions": {
                "container": 'map',
                "style": map_styles[0]['source']
            },
            "showUserLocationOnLoad": True
        }

        settings = {
            "mapStyles": map_styles,
            "fitBounds": {"relativePadding": 5},
            "loadSpritesheet": {
                "path": static("icons/mapbox-assist.svg"),
                "id": 'mapbox-assist--icons'
            },
            "route": {"form": {"show": True}, "enableUrlSharing": True},
            "search": {"show": True},
            "helpControl": {"show": True},
            "locationServices": {"showUserLocationControl": True},
        }

        if mapbox_assist_config.country_code:
            settings["limitToCountry"] = mapbox_assist_config.country_code

        context = {
            "mapbox": MapboxSettings.load(request_or_site=request),
            "parameters": parameters,
            "mapboxAssistSettings": settings,
            "featureLayers": feature_layers,
            "help": {
                "title": mapbox_assist_config.help_panel_title,
                "body": mapbox_assist_config.help_panel_body
            }
        }

        if mapbox_assist_config.extra_head:
            context["extra_head"] = mapbox_assist_config.extra_head

        return self.render(
            request,
            context_overrides=context,
            template="map/hiking_planner_page.html",
        )


# class MapPage(Page):
#     template = 'map/map_page.html'

#     intro = RichTextField(blank=True, null=True)
#     map_settings = models.ForeignKey(
#         MapboxAssistConfigs,
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name="map_pages"
#     )
#     parameters = models.JSONField(
#         _("Map Parameters"),
#         blank=True,
#         null=True
#     )
#     settings = models.JSONField(
#         _("Map Settings"),
#         blank=True,
#         null=True
#     )
#     help_panel_title = models.CharField(max_length=100, blank=True, null=True)
#     help_panel_body = RichTextField(blank=True, null=True)

#     content_panels = Page.content_panels + [
#         'intro',
#         'map_settings',
#         'parameters',
#         'settings',
#         'help_panel_title',
#         'help_panel_body'
#     ]
