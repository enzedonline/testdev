from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from generic_chooser.widgets import AdminChooser
from django.template.loader import render_to_string

from ..models import SVGImage


class SVGChooser(AdminChooser):
    image = "image"
    model = SVGImage

    choose_one_text = _('Choose an image')
    choose_another_text = _('Choose another image')
    choose_modal_url_name = 'svg_image_chooser:choose'

    def get_value_data(self, value):
        if value is None:
            instance = None
        elif self.model and isinstance(value, self.model):
            instance = value
            value = value.pk
        else:
            try:
                instance = self.get_instance(value)
            except (ObjectDoesNotExist if self.model is None else self.model.DoesNotExist):
                instance = None

        if instance is None:
            return {
                'value': None,
                'title': '',
                'image': '',
                'edit_item_url': None,
            }
        else:
            return {
                'value': value,
                'title': self.get_title(instance),
                'image': getattr(instance, 'svg', ''),
                'edit_item_url': self.get_edit_item_url(instance),
            }

    def render_html(self, name, value, attrs):
        value_data = value

        original_field_html = self.render_input_html(name, value_data['value'], attrs)

        return render_to_string(self.template, {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'is_empty': value_data['value'] is None,
            'title': value_data['title'],
            'image': value_data['image'],
            'edit_item_url': value_data['edit_item_url'],
            'create_item_url': self.get_create_item_url(),
            'choose_modal_url': self.get_choose_modal_url(),
        })

    class Media:
        js = [
            'generic_chooser/js/tabs.js',
            'generic_chooser/js/chooser-modal.js',
            'js/svg-chooser-widget.js',
            ]


