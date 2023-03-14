from wagtail import hooks
from .views import SVGIconChooserViewSet
from wagtail.snippets.models import register_snippet
from .models import SVGIcon
from .views import SVGViewSet

@hooks.register('register_admin_viewset')
def register_svg_icon_chooser_viewset():
    return SVGIconChooserViewSet('svg_icon_chooser', url_prefix='svg-icon-chooser')

register_snippet(SVGIcon, viewset=SVGViewSet)