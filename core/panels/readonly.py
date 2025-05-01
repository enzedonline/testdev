from wagtail.admin.panels import FieldPanel
from django import forms

class ReadOnlyFieldPanel(FieldPanel):
    """
    A FieldPanel that renders its field as read-only.
    Clones the default widget instance, adds the readonly attribute set to True and disabled for Select widgets.

    Args:
        field_name (str): The name of the field to render as read-only.
        read_only_class (str, optional): CSS class to apply to the read-only field. Defaults to 'readonly-field'.
    """
    
    def __init__(self, field_name, *args, **kwargs):
        self.read_only_class = kwargs.pop('read_only_class', 'readonly-field')
        self.label = kwargs.pop('label', None)
        self.kwargs = kwargs  # Store kwargs for clone method
        super().__init__(field_name, *args, **kwargs)

    def get_form_options(self):
        options = super().get_form_options()
        options.setdefault("widgets", {})
        if self.label:
            options.setdefault("labels", {})[self.field_name] = self.label
        field = self.model._meta.get_field(self.field_name)
        original_widget = field.formfield().widget
        widget_attrs = {
            **original_widget.attrs,
            'readonly': '',
            'class': f'{original_widget.attrs.get("class", "")} {self.read_only_class}'.strip(),
            'tabindex': '-1',  # Prevent tab focus
        }

        # Handle special widget types
        widget_kwargs = {'attrs': widget_attrs}
        if isinstance(original_widget, forms.Select):
            widget_attrs['disabled'] = ''
            widget_kwargs['choices'] = getattr(original_widget, 'choices', None)
        if hasattr(original_widget, 'format'):
            widget_kwargs['format'] = original_widget.format

        # Create new widget instance with appropriate kwargs
        widget_clone = type(original_widget)(**widget_kwargs)
        options["widgets"][self.field_name] = widget_clone
        return options

    def clone(self):
        return self.__class__(
            self.field_name,
            read_only_class=self.read_only_class,
            label=self.label,
            **self.kwargs
        )

# CSS    
# .readonly-field {
#     color: var(--w-color-text-meta) !important;
#     pointer-events: none;
# }
# .readonly-field:focus-visible {
#     outline: 0 !important;
# }
# .readonly-field:hover {
#     border-color: var(--w-color-border-field-default) !important;
# }