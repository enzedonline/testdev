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
                f'accept="{self.panel.file_type_filter}" '
                if self.panel.file_type_filter
                else ""
            )

        msg = {
            "file_label": _("Use 'Choose File' or drag/drop to import data from file."),
        }

        @mark_safe
        def render_html(self, parent_context=None):
            html = super().render_html(parent_context)
            soup = BeautifulSoup(html, "html.parser")
            text_area = soup.find("textarea")
            if not text_area:
                raise ImproperlyConfigured(
                    _("ImportTextFieldPanel should only be used with TextFields")
                )
            text_area["class"] = text_area.get("class", []) + ["import_text_area"]
            wrapper = soup.find(attrs={"data-field-wrapper": True})
            wrapper["data-field-wrapper"] = self.id_for_label()
            wrapper.append(self.import_text_field_button())
            wrapper.append(self.initialise_panel())
            return str(soup)

        def import_text_field_button(self):
            return BeautifulSoup(
                """
                <div class="textarea-fileinput-container">
                    <input type="file" class="textarea-fileinput"
                     """ + self.accepts + """ 
                    />
                    <span class="help">
                    """ + self.msg["file_label"] + """
                    </span> 
                </div>
                """,
                "html.parser",
            )

        def initialise_panel(self):
            return BeautifulSoup(
                f'<script>new ImportTextFieldPanel("{self.id_for_label()}")</script>',
                "html.parser",
            )
