from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page


class SimpleVideoOrderable(Orderable):
    page = ParentalKey("blog.VideoPage", related_name="videos")
    url = models.URLField()
    description = RichTextField(null=True, blank=True)

    panels = [
        FieldPanel('url'),
        FieldPanel('description'),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Video"

class VideoPage(RoutablePageMixin, Page):
    parent_page_types = ['blog.BlogIndex']
    subpage_types = []
    max_count = 1

    intro = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        MultiFieldPanel(
            [InlinePanel("videos", min_num=1)],
            heading="Videos",
        ),
    ]
    
    class Meta:
        verbose_name = _("Video Page")

    @path("")
    def video_list(self, request, sort=None):
        return self.render(
            request,
            template="blog/video-page.html",
        )