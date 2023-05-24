from bs4 import BeautifulSoup
from django.core.exceptions import ImproperlyConfigured
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel


class ImportTextFieldPanel(FieldPanel):
    """
    TextArea form field with option to import from file or drag/drop.
    file_type_filter: any valid accept string
    https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/accept
    """
    def __init__(self, field_name, file_type_filter=None, *args, **kwargs):
        self.file_type_filter = file_type_filter
        super().__init__(field_name, *args, **kwargs)

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            file_type_filter=self.file_type_filter,
        )
        return kwargs

    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.accepts = (
                f'accept="{self.panel.file_type_filter}" ' if self.panel.file_type_filter else ""
            )

        msg = {
            'file_label': _("Read data from file"),
        }

        def render_html(self, parent_context=None):
            html = super().render_html(parent_context)
            if not BeautifulSoup(html, 'html.parser').find('textarea'):
                raise ImproperlyConfigured(_("ImportTextFieldPanel should only be used with TextFields"))
            return mark_safe(
                html + self.import_text_field_button() + self.initialise_panel()
            )

        def import_text_field_button(self):
            file_input_id = f'{self.field_name}File'
            return '''
                <label for="''' + file_input_id + '''"> 
                    <h4 class="w-panel__heading w-panel__heading--label svg-panel-label">
                        ''' + self.msg['file_label'] + '''
                    </h4> 
                </label> 
                <input 
                    type="file" 
                    id="''' + file_input_id + '''" 
                    ''' + self.accepts + ''' 
                    style="border-style: none; padding: 0; display: block; width: fit-content;" 
                />'''
        
        def initialise_panel(self):
            return '''
                <script>
                    window.addEventListener('DOMContentLoaded', (event) => {
                        initialiseImportTextFieldPanel(
                            "''' + f'{self.field_name}File' + '''", 
                            "''' + self.id_for_label() + '''"
                        )
                    });
                </script>
                '''    