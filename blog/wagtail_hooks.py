from urllib.parse import urlparse

from django.contrib import messages
from django.urls import resolve
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.images import get_image_model
from wagtail.models import Collection

from blog.models import BlogPage

from .views import user_chooser_viewset


# @hooks.register('construct_image_chooser_queryset')
# def show_min_size_images_only(images, request):
#     min_width = 350
#     min_height = 250
#     http_referrer = request.META.get('HTTP_REFERER', None) or '/'
#     match = resolve(urlparse(http_referrer)[2])
#     if (match.app_name == 'wagtailsnippets_blog_spacecraft') and (match.url_name == 'edit'):
#         return images.filter(width__gte=min_width, height__gte=min_height)
#     return images

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

# @hooks.register('after_edit_page')
# def count_chars_warning(request, page):
#     errors = []
#     len_search_description = len(page.search_description)

#     if len_search_description < 50 or len_search_description > 160:
#         errors += [str(_(f'Meta Description should be between 50 and 160 characters for improved SEO.'))]

#     len_search_title = len(page.seo_title or page.title)
#     if len_search_title < 15 or len_search_title > 70:
#         if page.seo_title:
#             errors += [str(_(f'Title should be between 15 and 70 characters for improved SEO.'))]
#         else:
#             errors += [str(_(f'Page title is {len_search_title} characters. Create a title tag between 15 and 70 characters for improved SEO.'))]
    
#     if errors:
#         messages.warning(request, f"<div style='display: inline-flex;'>{'<br>'.join(errors)}</div>")