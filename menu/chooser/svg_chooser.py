from django.utils.translation import gettext_lazy as _
from wagtail.snippets.widgets import AdminSnippetChooser


class SVGSnippetChooser(AdminSnippetChooser):
    icon = "image"
    # template_name = "widgets/svg_chooser.html"
    # svg_key = "svg"

    # def get_value_data_from_instance(self, instance):
    #     data = super().get_value_data_from_instance(instance)
    #     data['svg'] = instance.svg
    #     return data
    
    # def render_html(self, name, value_data, attrs):
    #     html = super().render_html(name, value_data, attrs)
    #     return html

