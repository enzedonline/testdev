import logging

from django import template
from django.conf import settings
from django.db.models import Q
from django.utils.safestring import mark_safe

from core.utils import strip_svg_markup
from menu.models import Menu

register = template.Library()

@register.inclusion_tag("menu/navbar.html", takes_context=True)
def load_menu(context, menu_slug):
    if getattr(settings, "WAGTAIL_I18N_ENABLED", False):
        menu = Menu.objects.filter(slug=menu_slug).first().localized
    else:
        menu = Menu.objects.filter(slug=menu_slug).first()
    return {
        **context.flatten(),
        'menu': menu,
    }
   
@register.simple_tag(takes_context=True)
def show_on_menu(context, item):
    """
    Check if the item should be displayed on the menu based on the display_when option & user authenticated status
    """
    try:
        display_when = item.get('options').get('display_when')
        request = context.get('request')
        return (display_when in ['ALWAYS', None] or str(request.user.is_authenticated) == display_when)
    except Exception as e:
        logging.error(
            f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
        )

@register.simple_tag(takes_context=True)
def link_active(context, link):
    """
    If the link is the current page, return 'active' for the active class
    """
    try:
        request = context.get('request')
        return ' active' if link.url() == request.path else ''
    except:
        return ''

@register.simple_tag()
@mark_safe
def menu_icon(image, rendition_token='fill-25x25|format-png'):
    """
    Return the image rendition tag for the menu icon
    If image is svg, return as pure svg, stripped of script tags, height & width attributes
    """
    if image:
        if image.is_svg():
            svg_file = image.file.file
            if svg_file.closed: svg_file.open()
            svg = svg_file.read().decode('utf-8')
            svg_file.close()
            return strip_svg_markup(svg)
        else:
            r = image.get_rendition(rendition_token)
            return r.img_tag()
    return ''

@register.simple_tag(takes_context=True)
def get_autofill_pages(context):
    """
    Return a list of pages to autofill the menu with
    """
    autofill_block = context['self']
    links=[]

    try:
        authenticated = context['request'].user.is_authenticated
    except: # 500 error has no request
        authenticated = False

    parent_page = autofill_block['parent_page']
    if not parent_page:
        return []
    else:
        parent_page = parent_page.localized

    # include parent page if selected and if matches restriction (just assume exists=private here)
    if autofill_block['include_parent_page']:
        if parent_page.url == context['request'].path:
            parent_page.active = 'active'
        if parent_page.get_view_restrictions().exists():
            if authenticated:
                links.append(parent_page)
        else:
            links.append(parent_page)
    
    query = Q(live=True)
    # filter by 'Show in Menus' if selected
    if autofill_block['only_show_in_menus']:
        query &= Q(show_in_menus=True)
    # return only public pages if user not authenticated
    if authenticated:
        children = parent_page.get_children().filter(query).order_by(autofill_block['order_by'])
    else:
        children = parent_page.get_children().public().filter(query).order_by(autofill_block['order_by'])

    for child in children[:autofill_block['max_items']]:
        if child.url == context['request'].path:
            child.active = 'active'
        links.append(child)

    return links

@register.simple_tag(takes_context=True)
def render_user_info(context, msg):
    """
    Replace placeholders in the message with user info in the user menu
    """
    request = context.get('request')
    user = request.user
    if not user:
        return None
    else:
        if "@username" in msg:
            msg = msg.replace("@username", user.username)
        if "@display_name" in msg:
            msg = msg.replace("@display_name", getattr(user, 'display_name', user.get_full_name()))
        return msg