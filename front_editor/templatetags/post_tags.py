from django import template

from ..utils import is_in_group

register = template.Library()

@register.filter(name='is_integer')
def is_integer(value):
    return isinstance(value, int)

@register.filter()
def can_edit(user, post):
    try:
        return (user == post.author or is_in_group(user, "Post Moderators"))
    except:
        return False