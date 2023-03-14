from wagtail.admin.filters import WagtailFilterSet
import re
from django.utils.safestring import mark_safe

from bs4 import BeautifulSoup
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.models import ClusterableModel

from .panels import SVGFieldPanel
from modelcluster.fields import ParentalKey

from taggit.models import TaggedItemBase
from taggit.managers import TaggableManager

class SVGTag(TaggedItemBase):
    content_object = ParentalKey('svg.SVGIcon', on_delete=models.CASCADE, related_name='tagged_items')

class SVGIconForm(WagtailAdminModelForm):
    def clean(self) -> None:
        # check valid svg has been entered
        cleaned_data = super().clean()
        code = cleaned_data.get('svg')
        if code:
            # strip any xmlns:svg definition as it corrupts BSoup output.
            code = re.sub(r'xmlns:svg=\"\S+\"', '', code)
            soup = BeautifulSoup(code, 'xml')
            svg = soup.find('svg')
            if svg:
                del svg['height']
                del svg['width']
                del svg['preserveAspectRatio']
                # remove this next loop if you wany to allow <script> tags in <svg> icons
                for script in svg.find_all('script'):
                    script.extract()
                if not svg.has_attr('viewBox'):
                    self.add_error('svg', _("SVG element must include a valid viewBox attribute."))
                cleaned_data['svg'] = str(svg.prettify())
            else:
                self.add_error('svg', _("Please enter a valid SVG including the SVG element."))
        return cleaned_data
    
class SVGIcon(ClusterableModel):
    base_form_class = SVGIconForm

    label = models.CharField(max_length=255)
    svg = models.TextField(
        verbose_name="SVG", 
        help_text=_("Height and width attributes will be stripped on save.")
    )
    tags = TaggableManager(through=SVGTag, blank=True)

    panels = [
        FieldPanel('label'),
        FieldPanel('tags'),
        SVGFieldPanel('svg'),
    ]

    def __str__(self):
        return self.label
    
    @property
    def icon(self):
        return mark_safe(self.svg)

    class Meta:
        verbose_name = _("SVG Icon")

class SVGFilterSet(WagtailFilterSet):
    class Meta:
        model = SVGIcon
        fields = ["label"]