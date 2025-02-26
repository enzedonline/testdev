
import json
from dataclasses import asdict, dataclass

from django import forms
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


@dataclass
class NumericRangeScaleOptions:
    """
    Data class for numeric range slider options.
    minValue: float = 0
    maxValue: float = 100
    step: float = 0 # Step size, use this value to restrict the slider to multiples of the step value.
    unit: str = '' # Unit of the slider values.
    prefix: str = '' # Prefix to be displayed before the value.
    decimalPlaces: int = 0 # Number of decimal places to display.
    majorIntervals: int = 10 # Number of major intervals (ticks - 1).
    minorIntervals: int = 10 # Number of minor intervals to display per major interval (pips + 1).
    verticalLabels: bool = False # Display major tick labels vertically.
    """
    minValue: float = 0
    maxValue: float = 100
    step: bool = 0
    unit: str = ''
    prefix: str = ''
    decimalPlaces: int = 0
    majorIntervals: int = 10
    minorIntervals: int = 10
    verticalLabels: bool = False

    @property
    def dict(self):
        return asdict(self)
    
    @property
    def json(self):
        return json.dumps(self.dict)
    
    @property
    def items(self):
        return self.dict.items()


class NumericRangeSlider(forms.Widget):
    def __init__(self, options: NumericRangeScaleOptions = NumericRangeScaleOptions()):
        super().__init__()
        self.options = options

    @mark_safe
    def render(self, name, value, attrs={}, renderer=None):
        html = f'<div>{forms.HiddenInput().render(name, value, attrs)}</div>'
        html += f'<script>new NumericRangeSlider("{attrs["id"]}", {self.options.json});</script>'
        return html

    class Media:
        js = [
            'js/widgets/nouislider.js',
            'js/widgets/numeric-range-slider.js',
            'js/wNumb.js',
        ]
        css = {
            'all': [
                'css/widgets/nouislider.min.css',
                'css/widgets/numeric-range-slider.css',
            ]
        }
