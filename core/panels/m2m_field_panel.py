from bs4 import BeautifulSoup
from django.core.exceptions import ImproperlyConfigured
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from django.template import Context, Template
from django.forms.models import ModelMultipleChoiceField

class M2MFieldPanel(FieldPanel):
    """
    FieldPanel with pop-over chooser style form to select options in ParentalManyToManyField.
    """

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            widget=None,
        )
        return kwargs

    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.m2m_field_panel = {
                    "field_id": str(self.id_for_label()),
                    "heading": self.heading,
                    "select_button_text": _("Select"),
                    "submit_button_text": _("Submit"),
                    "search_text": _("Search"),
                    "cancel_text": _("Close without changes"),
                }

        def get_context_data(self, parent_context=None):
            context = super().get_context_data(parent_context)
            context.update(
                {
                    "m2m_field_panel": self.m2m_field_panel,
                }
            )
            return context
        
        def render_html(self, parent_context=None):
            html = super().render_html(parent_context)
            soup = BeautifulSoup(html, 'html.parser')
            select = soup.find('select')
            if not (select and self.bound_field.field.__class__ == ModelMultipleChoiceField):
                raise ImproperlyConfigured(_("M2MFieldPanel should only be used with ParentalManyToManyFields"))
            else:
                select['hidden'] = 'true'
            return mark_safe(
                str(soup) + 
                Template('{% include "panels/m2m_field_panel.html" %}').render(Context(self.get_context_data()))
            )
