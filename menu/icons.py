from bs4 import BeautifulSoup
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from .panels import SVGFieldPanel

class MenuIconForm(WagtailAdminPageForm):
    def clean(self) -> None:
        # check valid svg has been entered
        cleaned_data = super().clean()
        soup = BeautifulSoup(cleaned_data.get('svg'), 'xml')
        svg = soup.find('svg')
        if svg:
            del svg['height']
            del svg['width']
            # remove this next loop if you wany to allow <script> tags in <svg> icons
            for script in svg.find_all('script'):
                script.extract()
            cleaned_data['svg'] = str(svg.prettify())
        else:
            self.add_error('svg', _("Please enter a valid SVG including the SVG element."))
        return cleaned_data
    
@register_snippet
class MenuIcon(models.Model):
    base_form_class = MenuIconForm

    label = models.CharField(max_length=255)
    svg = models.TextField(
        verbose_name="SVG", 
        help_text=_("Height and width attributes will be stripped on save.")
    )

    panels = [
        FieldPanel('label'),
        SVGFieldPanel('svg'),
    ]

    def __str__(self) -> str:
        return self.label
