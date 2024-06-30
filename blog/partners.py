from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

@register_snippet
class Partner(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Partnership(models.Model):
    name = models.CharField(max_length=255)
    partners = models.ManyToManyField(Partner, related_name='partnerships')

    @property
    def partner_names(self):
        return ', '.join([partner.name for partner in self.partners.all()])

    def __str__(self):
        return self.name

class PartnershipViewSet(SnippetViewSet):
    model = Partnership
    list_display = ["name", "partner_names"]
    list_filter = {"name": ["icontains"], "partners": ["exact"]}

register_snippet(PartnershipViewSet)
