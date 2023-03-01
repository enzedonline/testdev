from django import template
from menu.models import Menu

register = template.Library()

@register.simple_tag()
def load_menu(menu_slug):
    return Menu.objects.filter(slug=menu_slug).first()

@register.simple_tag(takes_context=True)
def display_item(context):
    display_when = context['self']['display_when']
    is_authenticated = str(context['request'].user.is_authenticated)
    
    return (display_when == 'ALWAYS' or is_authenticated == display_when)

@register.simple_tag(takes_context=True)
def link_appearance(context):
    link_url = context['self'].url
    return {
        'show': display_item(context),
        'active': 'active' if (link_url == context['request'].path) else ''
    }

@register.simple_tag(takes_context=True)
def get_autofill_pages(context):
    autofill_block = context['self']

    try:
        authenticated = context['request'].user.is_authenticated
    except: # 500 error has no request
        authenticated = False

    parent_page = autofill_block['parent_page']
    links=[]

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
