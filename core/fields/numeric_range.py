import json

from django.core.exceptions import ValidationError
from django.db import models

from core.widgets import NumericRangeScaleOptions, NumericRangeSlider


class NumericRangeField(models.JSONField):
    widget = NumericRangeSlider

    def __init__(self, options: NumericRangeScaleOptions = NumericRangeScaleOptions(), *args, **kwargs):
        self.options = options
        super().__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {'widget': self.widget(self.options)}
        defaults.update(kwargs)
        return super().formfield(**defaults)
    
    def get_default(self):
        default = super().get_default()
        if default == None:
            return list 
        return default

    def validate_range_value(self, value):
        if not isinstance(value, list) or len(value) != 2:
            raise ValidationError("Value must be a list of two numeric elements.")
        first_value, second_value = value
        if first_value is not None and not isinstance(first_value, (int, float)):
            raise ValidationError("First value must be numeric.")
        if second_value is not None and not isinstance(second_value, (int, float)):
            raise ValidationError("Second value must be numeric.")
        if first_value is not None and second_value is not None:
            if first_value > second_value:
                raise ValidationError("First value must be less than or equal to the second value.")

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        self.validate_range_value(value)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        raise ValidationError("Invalid value for NumericRangeField.")

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)
    

    
# Version fo dbs not supporting JSONField

# import ast

# class NumericRangeField(models.Field):
#     widget = NumericRangeSlider

#     def __init__(self, options: NumericRangeScaleOptions = NumericRangeScaleOptions(), *args, **kwargs):
#         self.options = options
#         super().__init__(*args, **kwargs)

#     def db_type(self, connection):
#         return 'VARCHAR(100)'
    
#     def formfield(self, **kwargs):
#         defaults = {'widget': self.widget(self.options)}
#         defaults.update(kwargs)
#         return super().formfield(**defaults)
    
#     def from_db_value(self, value, expression, connection):
#         # use ';' as separator - ',' used as decimal point in some locales
#         if value is None:
#             return None
#         parts = value.split(";")
#         return [float(parts[0]) if parts[0] else None, float(parts[1]) if parts[1] else None]

#     def to_db_value(self, value, expression, connection):
#         if value is None:
#             return None
#         return f"{float(value[0])};{float(value[1])}"

#     def validate_range_value(self, value):
#         if not isinstance(value, list) or len(value) != 2:
#             raise ValidationError("Value must be a list of two numeric elements.")
#         first_value, second_value = value
#         if first_value is not None and not isinstance(first_value, (int, float)):
#             raise ValidationError("First value must be numeric.")
#         if second_value is not None and not isinstance(second_value, (int, float)):
#             raise ValidationError("Second value must be numeric.")
#         if first_value is not None and second_value is not None:
#             if first_value > second_value:
#                 raise ValidationError("First value must be less than or equal to the second value.")

#     def validate(self, value, model_instance):
#         super().validate(value, model_instance)
#         try:
#             range_value = ast.literal_eval(value)
#         except (SyntaxError, ValueError):
#             raise ValidationError("Invalid range list string - expected [float, float]")
#         self.validate_range_value(range_value)

