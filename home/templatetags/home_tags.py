from bs4 import BeautifulSoup
from django import template
from wagtail.templatetags.wagtailcore_tags import richtext
from html import unescape
from django.template.defaultfilters import linebreaksbr

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

NON_BREAKING_ELEMENTS = ['a', 'abbr', 'acronym', 'audio', 'b', 'bdi', 'bdo', 'big', 'button', 
    'canvas', 'cite', 'code', 'data', 'datalist', 'del', 'dfn', 'em', 'embed', 'i', 'iframe', 
    'img', 'input', 'ins', 'kbd', 'label', 'map', 'mark', 'meter', 'noscript', 'object', 'output', 
    'picture', 'progress', 'q', 'ruby', 's', 'samp', 'script', 'select', 'slot', 'small', 'span', 
    'strong', 'sub', 'sup', 'svg', 'template', 'textarea', 'time', 'u', 'tt', 'var', 'video', 'wbr']

@register.filter()
def plaintext(richtext):
    return BeautifulSoup(unescape(richtext), "html.parser").get_text(separator=" ")

@register.simple_tag()
def html_to_text(markup, preserve_new_lines=True, strip_tags=['style', 'script', 'code']):
    soup = BeautifulSoup(unescape(markup), "html.parser")
    for element in soup(strip_tags): element.extract()
    if preserve_new_lines:
        for element in soup.find_all():
            if element.name not in NON_BREAKING_ELEMENTS:
                element.append('\n') if element.name == 'br' else element.append('\n\n')
    return linebreaksbr(soup.get_text(" "))
