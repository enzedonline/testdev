from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from wagtail import hooks

from blog.models import BlogPage

from .views import user_chooser_viewset


@hooks.register("after_edit_page")
@hooks.register("after_create_page")
def get_wordcount(request, page):
    if page.specific_class == BlogPage:
        try:
            page.wordcount = page.words
            if page.has_unpublished_changes:
                page.save_revision()
            else:
                page.save()
        except Exception as e:
            print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")       
            messages.error(request, _('There was a problem generating the word count'))

@hooks.register('register_admin_viewset')
def register_user_chooser_viewset():
    return user_chooser_viewset