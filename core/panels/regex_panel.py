from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe
from django.forms.fields import SlugField
from django.core.exceptions import ImproperlyConfigured

class RegexPanel(FieldPanel):
    def __init__(self, field_name, pattern=None, *args, **kwargs):
        self.pattern = pattern
        super().__init__(field_name, *args, **kwargs)

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            pattern=self.pattern,
        )
        return kwargs

    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            if self.panel.pattern:
                self.form.fields[self.field_name].__setattr__(
                    "pattern", self.panel.pattern
                )
            elif issubclass(self.form.fields[self.field_name].__class__, SlugField):
                self.form.fields[self.field_name].__setattr__(
                    "pattern", '^[-\w]+$'
                )
            else:
                raise ImproperlyConfigured(_("Field must be a SlugField or have a pattern set on either the model field or panel definition."))

        def render_html(self, parent_context) -> str:
            html = super().render_html(parent_context)
            soup = BeautifulSoup(html, 'html.parser')
            input_element = soup.find('input')
            if input_element:
                input_element['onkeydown']="return regex_keydownhandler(event)"
                script = soup.new_tag('script')
                script.string = f'\
                    function regex_keydownhandler(event) {{ \
                        if (!(/{self.form.fields[self.field_name].pattern}/.test(event.key))){{\
                            return false;}} \
                    }}'
                soup.append(script)
            return mark_safe(str(soup.prettify()))

