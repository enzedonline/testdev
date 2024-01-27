import secrets
import string

from django import template
from wagtail.documents.models import Document

register = template.Library()

@register.simple_tag()
def random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

@register.filter()
def doc_title_to_url(title):
    try:
        document = Document.objects.get(title=title)
        return document.url
    except:
        pass
    