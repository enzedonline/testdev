import logging
import math
import random
import string
from urllib.parse import parse_qs, urlparse

from django.db import models
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.embeds.embeds import get_embed
from wagtail.embeds.exceptions import EmbedException
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

    def __str__(self) -> str:
        return self.url

    @cached_property
    def video_id(self):
        """
        Get youtube video ID from url
        ID is last element of url path for youtu.be and shorts
        """
        id = None
        parse = urlparse(self.url)
        if parse.netloc.lower() == 'youtu.be' or parse.path.lower().startswith('/shorts'):
            id = parse.path.split('/')[-1:]
        elif parse.query:
            id = parse_qs(parse.query).get('v')
        return id[0] if id else ''
    
    @cached_property
    def embed_attrs(self):
        """
        Get cached embed attributes from the db
        """
        try:
            embed = get_embed(self.url)
            return {
                'video_id': self.video_id,
                'thumbnail_url': embed.thumbnail_url,
                'title': embed.title,
                'author_name': embed.author_name,
                'last_updated': embed.last_updated,
            }
        except EmbedException as e:
            logging.warning(
                f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: Unable to embed {self.url}"
            )

class VideoPage(RoutablePageMixin, Page):
    """
    Video index page with api for auto pagination via routable mixin
    Page size - number of video cards to load per auto pagination (loaded via api)
    Initial pages - number of card 'pages' for initial page load (loaded via context/template)
    """
    parent_page_types = ['blog.BlogIndex']
    subpage_types = []
    page_size = 6
    initial_pages = 2

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

    def video_range(self, page=1, pages_to_load=1):
        """
        Return video card details for requested page.
        Request multiple pages with pages_to_load.
        Returns dictionary of videos and pagination status.
        Number of cards per page set by page_size class attribute.
        """
        # ensure parameters are positive whole numbers       
        try:
            page = max(int(page), 1)
        except (TypeError, ValueError):
            page = 1
        try:
            pages_to_load = max(int(pages_to_load), 1)
        except (TypeError, ValueError):
            pages_to_load = 1

        # caculate total pages including any final partial page
        all_videos = self.videos.all()
        total_pages = math.ceil(all_videos.count() / self.page_size)

        # get video card set if requested page is <= total pages
        videos = []
        if page <= total_pages:
            # caculate slice start & end
            start = (page - 1) * self.page_size
            if page + pages_to_load - 1 >= total_pages:
                end = None # last page, get everything from slice start 
            else:
                end = start + (self.page_size * pages_to_load)
            # create card set
            for video in all_videos[start:end]:
                details = video.embed_attrs
                # only return card if embed valid
                if details:
                    # use random id for card to ensure each is unique on the page
                    details['card_id'] = ''.join(random.choice(string.ascii_letters) for _ in range(8))
                    details['description'] = video.description
                    videos.append(details)
                    
        # disable pagination if last page reached (stops JS class auto-requesting new cards)
        # current page calculated from requested page and pages_to_load
        pagination = {
            'enabled': page < total_pages,
            'current_page': min((page - 1) + pages_to_load, total_pages),
        }

        return {'videos': videos, 'pagination': pagination}


    @path("")
    def video_index_page(self, request):
        """ default page response """
        # pre-load video cards on page load
        # use initial_pages class attribute to pre-load multiple video card sets
        # e.g. self.page_size = 6, self.initial_pages = 2 : pre-load 6x2=12 cards
        video_range = self.video_range(page=1, pages_to_load=self.initial_pages)
        return self.render(
            request,
            context_overrides={
                "videos": video_range['videos'],
                "pagination": video_range['pagination']
            },
            template="blog/video-page.html",
        )
    
    @path("api/page/<int:page>/")
    def paginated_video_json_response(self, request, page):
        """ Endless scroll json response """
        return JsonResponse(
            self.video_range(page=page), 
            safe=False
        )
    