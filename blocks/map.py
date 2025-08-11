from django import forms
from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (BooleanBlock, CharBlock, ChoiceBlock, ListBlock,
                            StaticBlock, StructBlock, TextBlock)
from wagtail.blocks.field_block import IntegerBlock
from wagtail.blocks.struct_block import (StructBlockAdapter,
                                         StructBlockValidationError)
from wagtail.admin.telepath import register
from django.utils.safestring import mark_safe

from core.utils import isfloat


class RouteOptionChoiceBlock(ChoiceBlock):
     choices=[
        ('', "None"),
        ('walking', "Walking"),
        ('cycling', "Cycling"),
        ('driving', "Driving"),
        ('driving-traffic', "Driving (with traffic conditions)")
     ]

class MapStyleChoiceBlock(ChoiceBlock):
    choices = [
        ('standard', _("Standard Map")),
        ('streets', _("Street Map")),
        ('terrain', _("Outdoors / Terrain")),
        ('satellite', _("Satellite")),
        ('satellite_streets', _("Satellite Steet Map")),
    ]

class MapWaypointBlock(StructBlock):
    gps_coord = CharBlock(
        label=_('GPS Coordinates (Latitude, Longtitude)'),
        help_text=_('Ensure latitude followed by longitude separated by a comma (e.g. 42.597486, 1.429252).')
    )
    pin_label = TextBlock(
        label=_('Map Pin Label (optional)'),
        required=False
    )
    show_pin = BooleanBlock(
        label=_('Show Pin on Map'),
        default=True,
        required=False
    )
    class Meta:
        icon = 'thumbtack'
        label = _("Map Waypoint")
        label_format = label + ": {pin_label}"
        form_classname = "struct-block flex-block map-waypoint-block"
        
    def clean(self, value):
        errors = {}
        gps = value.get('gps_coord')

        if gps.count(',') != 1:
            errors['gps_coord'] = ErrorList(
                [_("Please enter latitude followed by longitude, separated by a comma.")]
            )
            raise StructBlockValidationError(block_errors=errors)

        lat, lng = gps.split(',')
        
        if not(isfloat(lat) and isfloat(lng)):
            errors['gps_coord'] = ErrorList(
                [_("Please enter latitude and longitude in numeric format (e.g. 42.603552, 1.442655 not 42°36'12.8\"N 1°26'33.6\"E).")]
            )
            raise StructBlockValidationError(block_errors=errors)

        if (float(lat) < -90 or float(lat) > 90 or float(lng) < -180 or float(lng) > 360):
            errors['gps_coord'] = ErrorList(
                [_("Please enter latitude between -90 and 90 and longitude between -180 and 360.")]
            )
            raise StructBlockValidationError(block_errors=errors)

        return super().clean(value)
        
class MapBlock(StructBlock):
    waypoints = ListBlock(
        MapWaypointBlock, 
        min_num=2, 
        max_num=25, 
        label=_("Add Waypoints (minimum 2, maximum 25)")
    )
    style = MapStyleChoiceBlock(
        default='outdoors-v12',
        required=True,
        label=_("Map Type")
    )
    height = IntegerBlock(
        default=70, 
        min_value=20,
        label=_("Height (% of viewport)")
    )
    route_type = RouteOptionChoiceBlock(
        default='walking', 
        required=False
    )
    show_route_info = BooleanBlock(
        label=_("Show Route Info"),
        default=True,
        required=False
    )
    pitch = IntegerBlock(
        default=0, 
        min_value=0, 
        max_value=90, 
        label=_("Initial Tilt (degrees from vertical)")
    )
    bearing = IntegerBlock(
        default=0, 
        min_value=-180, 
        max_value=360, 
        label=_("Initial Bearing (degrees from North)")
    )
    padding_top = IntegerBlock(
        default=5, 
        min_value=0, 
        label=_("Top Padding")
    )
    padding_bottom = IntegerBlock(
        default=5, 
        min_value=0, 
        label=_("Bottom Padding")
    )
    padding_left = IntegerBlock(
        default=5, 
        min_value=0, 
        label=_("Left Padding")
    )
    padding_right = IntegerBlock(
        default=5, 
        min_value=0, 
        label=_("Right Padding")
    )
    padding_help_text = _("Padding left/right should be given as a percentage of the map dimension.")
    padding_help = StaticBlock(
        admin_text=mark_safe(f"<span class='help'>{padding_help_text}</span>")
    )

    class Meta:
        template='blocks/map_block.html'
        icon="map-marker"
        label = _("Interactive Map")
        label_format = label
        form_classname = "struct-block map-block"

class MapBlockAdapter(StructBlockAdapter):
    @cached_property
    def media(self):
        super().media
        return forms.Media(
            css={"all": ("css/admin/map-block.css",)},
        )
    
register(MapBlockAdapter(), MapBlock)    