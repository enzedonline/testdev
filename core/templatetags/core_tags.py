import secrets
import string

from bs4 import BeautifulSoup
from django import template
from wagtail.documents.models import Document
from wagtail.models import Page
from wagtail.templatetags.wagtailcore_tags import richtext

register = template.Library()

@register.filter()
def localised_slugurl(slug):
    try:
        return Page.objects.live().filter(slug=slug).first().localized.url
    except:
        return ''
    
@register.filter(name='is_in_group') 
def is_in_group(user, group_name):
    if user.id==None:
        return False
    else:
        return user.groups.get_queryset().filter(name=group_name).exists() 
    
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
    if not image.is_svg():
        try:
            imageOverSized = (width > image.width)
            if imageOverSized:
                return image.get_rendition("original|format-webp")
        except:
            pass
        return image.get_rendition(f"width-{width}|format-webp")
    else:
        return image.get_rendition(f"width-{width}")
    
@register.simple_tag()
def richtext_with_css(rich_text, classlist, target_elements=None):
    """
    Inserts css classes into rich text html
    classlist (str): css classes to insert, separate multiple values with space'
    target_elements(str: elements to apply classes to. None will apply to all. Separate multiple values with space.
    """
    target_elements = target_elements.split() if target_elements else True
    soup = BeautifulSoup(rich_text, 'html.parser')
    for p_tag in soup.find_all(target_elements):
        p_tag['class'] = p_tag.get('class', []) + [classlist]
    return richtext(str(soup))

@register.filter(name='is_integer')
def is_integer(value):
    return isinstance(value, int)