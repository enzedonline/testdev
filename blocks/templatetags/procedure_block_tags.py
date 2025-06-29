from django import template

register = template.Library()

@register.simple_tag()
def get_next_counter(content_item, counter):
    print(counter)
    pass