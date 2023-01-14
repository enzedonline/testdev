from bs4 import BeautifulSoup
from django import template
from wagtail.templatetags.wagtailcore_tags import richtext
register = template.Library()

@register.filter
def clean_richtext(richtextblock):
    soup = BeautifulSoup(richtextblock, "html.parser")
    for item in soup.find_all():
        rich_text_parser(item)
    return richtext(str(soup))
    
def rich_text_parser(element):
    if element.name != None:
        for child in element.children:
            rich_text_parser(child)
        match element.name:
            case 'br':
                element.decompose()
            case 'p':
                try:
                    element.string.replace_with(element.text.strip())
                    if element.string == '' and element.children.count() == 0:
                        element.decompose()
                except AttributeError:
                    element.decompose()
    