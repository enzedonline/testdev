from django.urls import resolve
from urllib.parse import urlparse
from wagtail import hooks
from wagtail.models import Collection


@hooks.register('construct_image_chooser_queryset')
def show_images_for_specific_collections_on_page_editing(images, request):
    http_referrer = request.META.get('HTTP_REFERER', None) or '/'
    match = resolve(urlparse(http_referrer)[2])
    if (match.app_name == 'wagtailsnippets_menu_menu') and (match.url_name == 'edit'):
        menu_icons = Collection.objects.filter(name='Menu Icons').first()
        if menu_icons:
            return images.filter(collection=menu_icons.id)
    return images