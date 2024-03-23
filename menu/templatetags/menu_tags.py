from django import template
from django.utils.safestring import mark_safe

from core.utils import strip_svg_markup
from menu.models import Menu

register = template.Library()

@register.simple_tag()
def load_menu(menu_slug):
    try:
        return Menu.objects.filter(slug=menu_slug).first().localized
    except:
        return Menu.objects.filter(slug=menu_slug).first()
   
@register.filter()
def show_on_menu(item, request):
    try:
        display_when = item.get('options').get('display_when')
        return (display_when in ['ALWAYS', None] or str(request.user.is_authenticated) == display_when)
    except:
        return True

@register.simple_tag(takes_context=True)
def link_active(context, link):
    try:
        return ' active' if link.url() == context['request'].path else ''
    except:
        return ''

@register.simple_tag()
@mark_safe
def menu_icon(image, redition_token='fill-25x25|format-png'):
    if image:
        if image.filename[-4:].lower()==".svg":
            svg_file = image.file.file
            if svg_file.closed: svg_file.open()
            svg = svg_file.read().decode('utf-8')
            svg_file.close()
            return strip_svg_markup(svg)
        else:
            r = image.get_rendition(redition_token)
            return r.img_tag()
    return ''

@register.simple_tag(takes_context=True)
def get_autofill_pages(context):
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
    
    # return only public pages if user not authenticated
    if authenticated:
        children = parent_page.get_children().live().order_by(autofill_block['order_by'])
    else:
        children = parent_page.get_children().live().public().order_by(autofill_block['order_by'])

    # filter by 'Show in Menus' if selected
    if autofill_block['only_show_in_menus']:
        children = children.filter(show_in_menus=True)

    for child in children[:autofill_block['max_items']]:
        if child.url == context['request'].path:
            child.active = 'active'
        links.append(child)

    return links

@register.simple_tag(takes_context=True)
def render_user_info(context, msg):
    user = context['request'].user
    if user and "@username" in msg:
        msg = msg.replace("@username", user.username)
    if user and "@display_name" in msg:
        msg = msg.replace("@display_name", getattr(user, 'display_name', user.get_full_name()))
    return msg