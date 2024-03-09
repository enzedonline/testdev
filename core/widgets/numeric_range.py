
from dataclasses import asdict, dataclass

from django import forms
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


@dataclass
class NumericRangeScaleOptions:
    min_value: float = 0
    max_value: float = 100
    step: bool = 10
    unit: str = ''
    pip_count: int = 6
    pip_prefix: str = ''
    pip_decimals: int = 0
    minor_tick_density: int = 4
    vertical_labels: bool = False

    @property
    def dict(self):
        return asdict(self)
    
    @property
    def items(self):
        return self.dict.items()

    @property
    def attrs(self):
        modified_values = {}
        for key, value in self.items:
            modified_key = 'data-' + key.replace('_', '-')
            if isinstance(value, bool):
                value = 'true' if value else 'false'
            modified_values[modified_key] = value
        return modified_values

class NumericRangeSlider(forms.Widget):
    def __init__(self, options: NumericRangeScaleOptions = NumericRangeScaleOptions()):
        super().__init__()
        self.options = options

    @mark_safe
    def render(self, name, value, attrs={}, renderer=None):
        # Create data attributes for min_value, max_value, and step
        attrs.update(self.options.attrs)
        # Render a hidden input field with data attributes
        hidden_input = forms.HiddenInput().render(name, value, attrs)
        # Add the script tag to initialize the NumericRangeSlider
        return f'<div>{hidden_input}</div>{self.js(attrs["id"])}'

    def js(self, id):
        return f"""
        <script>
            Promise.all([
                include_css("{static('css/widgets/nouislider.min.css')}", "nouislider-css"),
                include_css("{static('css/widgets/numeric-range-slider.css')}", "numeric-range-slider-css"),
                include_js("{static('js/widgets/nouislider.js')}", "nouislider-js"),
                include_js("{static('js/widgets/numeric-range-slider.js')}", "numeric-range-slider-js"),
                include_js("{static('js/wNumb.js')}", "wnumb-js"),
            ]).then(() => {{
                new NumericRangeSlider("{id}");
            }})
            .catch(error => {{
                console.error('Error loading scripts:', error);
            }});
        </script>
        """
