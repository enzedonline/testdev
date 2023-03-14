from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import ChooserBlock


class SVGChooserBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        from ..models import SVGIcon
        return SVGIcon
        
    @cached_property
    def widget(self):
        from .widget import SVGChooser
        return SVGChooser()
    
    def get_form_state(self, value):
        return self.widget.get_value_data(value)

    class Meta:
        icon = "image"
