import re

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField
from wagtail.models import Page

from core.panels import InfoPanel
from core.utils import get_streamfield_text


class BlogPage(Page):
    wordcount = models.IntegerField(null=True, blank=True, verbose_name="Word Count")
    content = StreamField(
        [
            ("rich_text", RichTextBlock()),
        ],
        verbose_name="Page Content",
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        InfoPanel('<span class="editor-reminder">Some important notice to display</span>'),
        InfoPanel(
            '<h5><a target="_blank" href="{{url}}" style="color: blue; text-decoration: underline;">News Article Editors Guide</a></h5>',
            value_dict={
                'url': [{'module': 'core.utils', 'method': 'page_url', 'slug': 'first-blog', 'target': 'news-article'}]
            },
            style='text-align: center;'
            ),
        InfoPanel(
            '<b>Word Count:</b> {{wordcount}}', {'wordcount': 'wordcount'},
            add_hidden_fields=True
            ),
        InfoPanel(
            '<div class="tagit">\
                Created by <a href="/profiles/{{username}}" style="color: blue; text-decoration: underline;" target="_blank" >\
                {{fullname}}</a>.<br>\
                First published on {{firstpub}}\
             </div>',
            value_dict={
                'username': ['owner', 'username'],
                'fullname': ['owner', 'get_full_name', 'upper'],
                'firstpub': 'first_published_at'
            },
            datetime_format='%d %B %Y'
            ),
        InfoPanel('Random number: {{rnd}}', {'rnd': [{'module': 'random', 'method': 'randint', 'a': 1,'b': 9999}]}),
        InfoPanel(
            'Maximum of 3,56,4,99,5 is {{maximum}}',
            {'maximum': [{'module': 'builtins', 'method': 'max', 'args':[3,56,4,99,5]}]}
            ),
        InfoPanel(
            '<p class="tagit edit-permission-{{perm}}">You do not have publish permission for this page.</p>',
            {'perm': [('permissions_for_user', {'user': ['panel', 'request', 'user']}), 'can_publish']}
        ),
        InfoPanel(
            text="<h5>Siblings</h5>{{siblings}}",
            value_dict={
                "siblings": [
                    {
                        "object": "<br>",
                        "method": (
                            "join",
                            {
                                "args": {
                                    "module": "builtins",
                                    "method": "list",
                                    "args": [
                                        "self",
                                        "get_siblings",
                                        (
                                            "values_list",
                                            {"args": ["title"], "flat": True},
                                        ),
                                    ],
                                }
                            },
                        ),
                    }
                ]
            },
        ),
        FieldPanel("content"),
    ]

    class Meta:
        verbose_name = 'Blog Page'

    def corpus(self):
        return get_streamfield_text(
            self.content
        )

    def get_wordcount(self, corpus=None):
        if not corpus:
            corpus = self.corpus()
        return len(corpus.split(" "))
