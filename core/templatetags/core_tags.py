from django import template
import secrets
import string

register = template.Library()

@register.simple_tag()
def random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
