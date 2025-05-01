import logging
from django.conf import settings


class OrderedChoicesMixin:
    """
    Mixin class to order choice queryset based on a specified field.
    Attributes:
        order_by (str): An optional kwarg that specifies the field 
            by which the choices should be ordered.
    """

    def _get_super_prop(self, name):
        """
        Look up the next property in the MRO after Mixin.
        This method searches the MRO of self and returns the property object
        for the given name from the first class *after* Mixin that defines it.
        """
        found_self = False
        for cls in type(self).__mro__:
            if cls is OrderedChoicesMixin:
                found_self = True
                continue
            if found_self and name in cls.__dict__:
                return cls.__dict__[name]
        raise AttributeError(f"No super property found for {name}")

    def __init__(self, *args, **kwargs):
        self.order_by = kwargs.pop('order_by', None)
        super().__init__(*args, **kwargs)

    def _set_choices(self, value):
        try:
            if self.order_by and bool(value) & hasattr(value, 'queryset'):
                value.queryset = value.queryset.order_by(self.order_by)
        except Exception as e:
            logging.error(
                f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
            )
            if getattr(settings, 'DEBUG', False):
                raise
        
        prop = self._get_super_prop("choices")
        prop.fset(self, value)

    @property
    def choices(self):
        return super().choices

    @choices.setter
    def choices(self, value):
        self._set_choices(value)

# Define choices widgets here

from django.forms.widgets import CheckboxSelectMultiple

class OrderedCheckboxSelectMultiple(OrderedChoicesMixin, CheckboxSelectMultiple):
    pass
