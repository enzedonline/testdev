from django.shortcuts import redirect
from wagtail import hooks
from wagtail.admin import messages
from django.templatetags.static import static
from django.utils.safestring import mark_safe

# from .models import PostsPage


# @hooks.register('before_delete_page')
# def before_delete_page(request, page):
#     if page.specific_class in [PostsPage]:
#         if request.method == 'GET':
#             messages.warning(request, "Deleting this page will also delete all posts associated with it.")
#         if page.locked:
#             if request.method == 'GET':
#                 messages.error(request, "Page cannot be deleted while locked.")
#             if request.method == 'POST': 
#                 return redirect('wagtailadmin_pages:delete', page.pk)        
            
@hooks.register('insert_global_admin_css')
def register_admin_css():
    admin_quill_css = static('css/quill/admin-quill-editor.css')
    return mark_safe(
        f'<link rel="stylesheet" href="{admin_quill_css}">' 
    )            