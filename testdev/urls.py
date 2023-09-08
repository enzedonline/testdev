from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from core.views import SitemapView
from blocks.views import ExternalContentProxy, check_image_url

from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path('sitemap.xml', SitemapView.as_view(), name='sitemap'),
    path('external-content-proxy/', ExternalContentProxy.as_view(), name='external-content-proxy'),
    path('check-image-url/', check_image_url, name='check_image_url'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        re_path(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception("Permission Denied")}),
        re_path(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        re_path(r'^500/$', default_views.server_error), 
    ]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path('', include('chatbot.urls')),
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
