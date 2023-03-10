from wagtail import hooks
from .views import user_chooser_viewset

@hooks.register('register_admin_viewset')
def register_user_chooser_viewset():
    return user_chooser_viewset