from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.snippets.blocks import SnippetChooserBlock


class SVGChooserBlock(SnippetChooserBlock):
    
    @cached_property
    def widget(self):
        from .svg_chooser import SVGSnippetChooser
        return SVGSnippetChooser(self.target_model)
    
    # def get_form_state(self, value):
    #     value_data = super().get_form_state(value)
    #     return value_data

    class Meta:
        icon = "image"
