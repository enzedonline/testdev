from bs4 import BeautifulSoup
from dateutil.parser import parse
from django.forms.fields import CharField, DateTimeField
from django.utils import timezone
from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel
from wagtail.admin.widgets import AdminDateTimeInput


class PrepopulatePanel(FieldPanel):
    """
    Prepopulate form fields in the Wagtail admin interface based on URL parameters.
    Attributes:
        url_parameter (str): The URL parameter used to prepopulate the field. Defaults to the field name if not provided.
    Inner Classes:
        BoundPanel:
            Handles the logic for prepopulating the field value and rendering the HTML with the initial value.
            Methods:
                __init__(**kwargs):
                    Initializes the BoundPanel and sets the initial value of the field based on the URL parameter.
                render_html(parent_context):
                    Renders the HTML for the panel, ensuring that the initial value is correctly set in the widget.
    """
    def __init__(
        self, field_name, url_parameter=None, *args, **kwargs
    ):
        # Set the url_parameter to the field_name if not provided
        self.url_parameter = url_parameter or field_name 
        super().__init__(field_name, *args, **kwargs)

    def clone_kwargs(self):
        super_kwargs = super().clone_kwargs()
        super_kwargs['url_parameter'] = self.url_parameter
        return super_kwargs
    
    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            if not self.bound_field.value():
                value = self.request.GET.get(self.panel.url_parameter)
                if value:                
                    match self.bound_field.field:
                        case DateTimeField():
                            try:
                                init_value = parse(value)
                                # convert value to db timezone if tz component supplied
                                if timezone.is_aware(init_value):
                                    init_value = timezone.localtime(init_value)
                                self.bound_field.field.initial = init_value
                            except ValueError:
                                value = None
                        case CharField():
                            # If the field is a CharField, we can set the initial value directly
                            self.bound_field.field.initial = value
                        # add other cases as needed 

        @mark_safe
        def render_html(self, parent_context):
            # Wagtail widgets are not always rendered with the initial value - fix it here
            html = super().render_html(parent_context)
            if not self.bound_field.value() and self.bound_field.field.initial:
                match self.bound_field.field.widget:
                    case AdminDateTimeInput():
                        try:
                            parsed = self.bound_field.field.initial.strftime(self.bound_field.field.widget.format)
                            soup = BeautifulSoup(html, "html.parser")
                            input_element = soup.find("input")
                            if input_element:
                                input_element["value"] = parsed
                                return str(soup)
                        except (ValueError, TypeError):
                            pass
                    # add other cases as needed 

            return html                              

