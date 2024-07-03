# api's for dealing with different objects types within WagTail
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

# Init the Wagtail Router
# wagtailapi = url name defined in urls.py
api_router = WagtailAPIRouter('wagtailapi')

# Register 3 API endpoints: Pages, Images and Documents
# register_endpoint takes two parameters: url name (defined in urls.py and an endpoint type)
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)
