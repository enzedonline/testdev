from django.urls import path

from .views.external_link import ExternalContentProxy, check_image_url
from .views.csv_table import RenderCSVTableProxy

urlpatterns = [
    path('render-csv-table-proxy/', RenderCSVTableProxy.as_view(), name='render-csv-table-proxy'),
    path('external-content-proxy/', ExternalContentProxy.as_view(), name='external-content-proxy'),
    path('check-image-url/', check_image_url, name='check_image_url'),
]