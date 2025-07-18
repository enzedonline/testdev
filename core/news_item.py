from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.ui.tables import LiveStatusTagColumn, UpdatedAtColumn
from wagtail.blocks import RichTextBlock, StreamBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageBlock
from wagtail.models import (DraftStateMixin, LockableMixin, PreviewableMixin,
                            RevisionMixin, WorkflowMixin)
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet


class NewsStreamBlock(StreamBlock):
    text = RichTextBlock(
        label=_("Text")
    )
    image = ImageBlock(
        label=_("Image")
    )
    # other block types to include


class NewsPost(
    PreviewableMixin,
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    models.Model,
):
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    featured = models.BooleanField(
        default=False,
        verbose_name=_("Featured"),
        help_text=_(
            "Check this box to feature this news post on the homepage."),
    )
    card_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name=_("Card Image"),
    )
    body = StreamField(
        NewsStreamBlock(),
        verbose_name=_("News Article Body")
    )

    panels = ["title", "featured", "card_image", "body"]

    def get_preview_template(self, request, mode_name):
        return "news/preview.html"

    def __str__(self) -> str:
        return self.title

class Meta:
    verbose_name = _('News Item')


class NewsViewSet(SnippetViewSet):
    model = NewsPost
    list_display = ["title", "featured",
                    UpdatedAtColumn(), LiveStatusTagColumn()]
    ordering = ["-first_published_at"]


register_snippet(NewsViewSet)
