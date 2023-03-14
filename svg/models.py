import re

from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel

from .panels import SVGFieldPanel


class SVGImage(models.Model):
    label = models.CharField(max_length=255, verbose_name=_("label"), unique=True)
    svg = models.TextField(
        verbose_name="SVG",
        help_text=_("Height and width attributes will be stripped on save."),
    )

    panels = [
        FieldPanel("label"),
        SVGFieldPanel("svg"),  # provides read svg file feature with preview and parsing
    ]

    def __str__(self):
        return self.label

    def image(self):
        # used by SVGViewSet to display the image in the snippet list view
        return mark_safe(
            f'<div class="svg-viewset-cell">\
                <div class="svg-viewset-item">\
                    {self.svg}\
                </div>\
            </div>'
        )

    image.short_description = "Image"

    class Meta:
        verbose_name = _("SVG Image")

    def clean(self) -> None:
        # strip height/width attribute - should come from container or class
        # strip any xmlns:svg definition as it corrupts BSoup output.
        # strip preserveAspectRatio - default is True
        # strip any embedded JavaScript (purely for security)
        # check for valid svg element with viewBox attribute
        if self.svg:
            self.svg = re.sub(r"xmlns:svg=\"\S+\"", "", self.svg)
            soup = BeautifulSoup(self.svg, "xml")
            svg = soup.find("svg")
            if svg:
                del svg["height"]
                del svg["width"]
                del svg["preserveAspectRatio"]
                # remove this next loop if you wany to allow <script> tags in <svg> images
                for script in svg.find_all("script"):
                    script.extract()
                if not (svg.has_attr("viewBox") or svg.has_attr("viewbox")):
                    raise ValidationError(
                        _("SVG element must include a valid viewBox attribute.")
                    )
                self.svg = str(svg.prettify())
            else:
                raise ValidationError(
                    _("Please enter a valid SVG including the SVG element.")
                )
