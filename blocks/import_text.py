from django import forms


from blocks.wagtail.blocks import TextBlock


class ImportTextBlock(TextBlock):
    """
    TextArea block with option to import from file or drag/drop.
    file_type_filter: any valid accept string
    https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/accept
    """

    from django.utils.functional import cached_property

    def __init__(
        self,
        required=True,
        help_text=None,
        rows=5,
        max_length=None,
        min_length=None,
        file_type_filter=None,
        validators=(),
        **kwargs
    ):
        super().__init__(
            required, help_text, rows, max_length, min_length, validators, **kwargs
        )
        self.file_type_filter = file_type_filter

    @cached_property
    def field(self):
        from core.widgets.models import ImportTextAreaWidget
        field_kwargs = {
            "widget": ImportTextAreaWidget(
                self.file_type_filter, attrs={"rows": self.rows}
            )
        }
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    class Meta:
        icon = "copy"