from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from core.widgets.models import ImportTextAreaWidget
from django.db.models.fields import TextField

class ImportTextAreaPanel(FieldPanel):
    """
    TextArea form field with option to import from file or drag/drop.
    file_type_filter: any valid accept string
    https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/accept
    """

    def __init__(
        self,
        field_name,
        disable_comments=None,
        permission=None,
        read_only=False,
        file_type_filter=None,
        **kwargs,
    ):
        kwargs.update({'widget': ImportTextAreaWidget(file_type_filter=file_type_filter)})
        self.file_type_filter = file_type_filter
        super().__init__(
            field_name = field_name, 
            disable_comments = disable_comments,
            permission = permission,
            read_only = read_only,
            **kwargs
            )

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            field_name=self.field_name,
            disable_comments=self.disable_comments,
            permission=self.permission,
            read_only=self.read_only,
            file_type_filter = self.file_type_filter,
        )
        return kwargs        

    def on_model_bound(self):
        if not isinstance(self.db_field, TextField):
            raise ImproperlyConfigured(
                _("ImportTextFieldPanel should only be used with TextFields")
            )
        return super().on_model_bound()
