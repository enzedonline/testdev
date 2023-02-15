from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel
from wagtail.rich_text import RichText
from wagtail.blocks import StreamValue
from core.utils import text_from_html
from django.utils.functional import cached_property

class RestrictedFieldPanel(FieldPanel):
    def __init__(self, field_name, authorised_groups, **kwargs):
        self.field_name = field_name
        self.authorised_groups = authorised_groups \
            if isinstance(authorised_groups, list) else [authorised_groups]
        super().__init__(self.field_name, **kwargs)

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            authorised_groups=self.authorised_groups,
        )
        return kwargs

    def get_form_options(self):
        return super().get_form_options()

    def format_value_for_display(self, value):
        """
        Hook to allow formatting of raw field values (and other attribute values) for human-readable
        display. For example, if rendering a ``RichTextField`` value, you might extract text from the HTML
        to generate a safer display value.
        """
        # Improve representation of many-to-many values
        if callable(getattr(value, "all", "")):
            return ", ".join(str(obj) for obj in value.all()) or "None"

        # Avoid rendering potentially unsafe HTML mid-form
        if isinstance(value, (RichText, StreamValue)):
            return text_from_html(value)

        return value

    class BoundPanel(FieldPanel.BoundPanel):
        
        def is_authorised(self):
            try:
                is_authorised = self.request.user.groups.get_queryset().filter(name__in=self.panel.authorised_groups).exists()
                return is_authorised
            except:
                print("error")
                return False

        def render_html(self, parent_context = None):
            return super().render_html(parent_context) \
                if self.is_authorised() else self.disable_input(parent_context)

        def disable_input(self, parent_context):
            msg = '<span style="color:red;">Read-only</span>'
            self.bound_field.help_text = mark_safe(
                f'{self.bound_field.help_text}/n{msg}' if self.bound_field.help_text else msg
            )
            # Don't do this, the field value is dropped on save
            self.form.fields[self.field_name].disabled = True
            html = super().render_html(parent_context)
            if self.form._meta.exclude:
                self.form._meta.exclude.append(self.field_name)
            else:
                # self.form._meta.exclude = [self.field_name]
                opts = self.panel.get_form_options()
                opts["exclude"] = opts['fields'].copy()
            # self.form.base_fields.pop(self.field_name)
            # self.form.fields.pop(self.field_name)
            # self.form.Meta.fields.remove(self.field_name)


            return html
            # soup = BeautifulSoup(super().render_html(parent_context), "html.parser")
            # soup.find('input')['disabled'] = ''
            # return mark_safe(soup.renderContents().decode("utf-8"))

        def get_read_only_context_data(self):
            return {
                "display_value": self.panel.format_value_for_display(
                    self.value_from_instance
                ),
                "id_for_label": self.id_for_label(),
                "help_text": self.help_text,
                "help_text_id": "%s-helptext" % self.prefix,
                "raw_value": self.value_from_instance,
                "show_add_comment_button": self.comments_enabled,
            }
        
        @cached_property
        def value_from_instance(self):
            return getattr(self.instance, self.field_name)         