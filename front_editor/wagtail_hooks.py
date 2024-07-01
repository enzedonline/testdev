from django.shortcuts import redirect
from wagtail import hooks
from wagtail.admin import messages

from .models import PostsPage


@hooks.register('before_delete_page')
def before_delete_page(request, page):
    if page.specific_class in [PostsPage]:
        if request.method == 'GET':
            messages.warning(request, "Deleting this page will also delete all posts associated with it.")
        if page.locked:
            if request.method == 'GET':
                messages.error(request, "Page cannot be deleted while locked.")
            if request.method == 'POST': 
                return redirect('wagtailadmin_pages:delete', page.pk)        
            