from wagtail.admin import panels


class FieldPanel(panels.FieldPanel):
    def __init__(
        self,
        field_name,
        widget=None,
        widget_attrs={},
        disable_comments=None,
        permission=None,
        read_only=False,
        **kwargs,
    ):
        super().__init__(
            field_name,
            widget,
            disable_comments,
            permission,
            read_only,
            **kwargs,
        )
        self.widget_attrs = widget_attrs

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            widget_attrs=self.widget_attrs,
        )
        return kwargs

    class BoundPanel(panels.FieldPanel.BoundPanel):
        def get_editable_context_data(self):
            widget_described_by_ids = []
            help_text_id = "%s-helptext" % self.prefix
            error_message_id = "%s-errors" % self.prefix

            widget_described_by_ids = []
            if self.help_text:
                widget_described_by_ids.append(help_text_id)

            widget_attrs = self.panel.widget_attrs
            if self.bound_field.errors:
                widget = self.bound_field.field.widget
                if hasattr(widget, "render_with_errors"):
                    widget_attrs["id"] = (self.bound_field.auto_id,)
                    if widget_described_by_ids:
                        widget_attrs["aria-describedby"] = " ".join(
                            widget_described_by_ids
                        )

                    rendered_field = widget.render_with_errors(
                        self.bound_field.html_name,
                        self.bound_field.value(),
                        attrs=widget_attrs,
                        errors=self.bound_field.errors,
                    )
                else:
                    widget_described_by_ids.append(error_message_id)
                    rendered_field = self.bound_field.as_widget(
                        attrs={
                            "aria-invalid": "true",
                            "aria-describedby": " ".join(widget_described_by_ids),
                        }
                    )
            else:
                if widget_described_by_ids:
                    widget_attrs["aria-describedby"] = " ".join(widget_described_by_ids)

                rendered_field = self.bound_field.as_widget(attrs=widget_attrs)

            return {
                "field": self.bound_field,
                "rendered_field": rendered_field,
                "error_message_id": error_message_id,
                "help_text": self.help_text,
                "help_text_id": help_text_id,
                "show_add_comment_button": self.comments_enabled
                and getattr(
                    self.bound_field.field.widget,
                    "show_add_comment_button",
                    True,
                ),
            }
