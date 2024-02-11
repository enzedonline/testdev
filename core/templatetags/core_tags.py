import secrets
import string

from django import template
from wagtail.documents.models import Document
from wagtail.templatetags.wagtailcore_tags import richtext

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

@register.filter()
def clean_rich_text(rich_text):
    render = richtext(rich_text)
    return render

@register.simple_tag()
def get_rendition(image, image_options):
    return image.get_rendition(image_options)

@register.simple_tag()
def get_picture_rendition(image, width):
    file = getattr(image, 'file', False)
    if file:
        if width < image.file.width:
            return image.get_rendition(f"width-{width}|format-webp")
        else:
            return image.get_rendition("original|format-webp")
