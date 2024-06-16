from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_tiptap.fields import TipTapTextField
from django_tiptap.widgets import TipTapWidget
from wagtail.admin.panels import FieldPanel
from wagtail.admin.ui.tables import UpdatedAtColumn, UserColumn
from wagtail.models import DraftStateMixin, PreviewableMixin, RevisionMixin
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from quill.fields import QuillField
from quill.widgets import QuillWidget


class Post(PreviewableMixin, DraftStateMixin, RevisionMixin, index.Indexed, models.Model):
    icon = "cogs"

    title = models.CharField(
        max_length=100
    )
    content = QuillField()
    tiptap = TipTapTextField(null=True, blank=True)
    author = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=False,
        on_delete=models.SET_NULL
    )
    page = models.ForeignKey(
        'front_editor.PostsPage',
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=False,
    )
    
    @property
    def plain_text(self):
        return BeautifulSoup(self.content.html, 'lxml').get_text()

    @property
    def username(self):
        try:
            return self.author.username
        except:
            return ''
        
    def page_title(self):
        try:
            return self.page.title
        except:
            return ''
            
    panels = [
        FieldPanel("title"),
        FieldPanel("content", widget=QuillWidget),
        # FieldPanel("tiptap", widget=TipTapWidget),
        FieldPanel("author"),
        FieldPanel("page"),
    ]

    search_fields = [
        index.SearchField('title'),
        index.SearchField('plain_text'),
        index.SearchField('username'),
        index.AutocompleteField('title'),
        index.AutocompleteField('username'),
        index.FilterField('live'),
        index.FilterField('page_id'),
    ]

    def get_preview_template(self, request, mode_name):
        return "posts/post-preview.html"

    def __str__(self):
        return self.title

class PostViewSet(SnippetViewSet):
    model = Post
    list_display = ["title", UserColumn("author"), "page_title", "first_published_at", UpdatedAtColumn()]
    list_per_page = 20
    ordering = ["-first_published_at"]

setattr(Post.page_title, 'short_description', 'Page')
register_snippet(PostViewSet)
