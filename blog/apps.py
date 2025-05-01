from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        from wagtail.models.reference_index import ReferenceIndex
        # Import the model here to ensure it's registered with the app
        from .video_page import VideoPage
        from .categories import BlogCategory
        ReferenceIndex.register_model(BlogCategory)

