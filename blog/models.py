import re

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import RichTextBlock
from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page
from core.forms import RestrictedPanelsAdminPageForm
from core.panels import InfoPanel, RestrictedFieldPanel
from core.utils import get_streamfield_text
from django.contrib.auth.models import Group

class BlogPage(Page):
    wordcount = models.IntegerField(null=True, blank=True, verbose_name="Word Count", default=0)
    some_date = models.DateTimeField(null=True, blank=True, help_text="Some helpful text")
    some_text = models.CharField(max_length=255)
    some_rich_text = RichTextField(null=True, blank=True)
    some_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name='Some Image',
    )
    some_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name='Some Document',
    )
    some_product = models.ForeignKey(
        'site_settings.Product',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name='Some Product',
    )
    some_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name='Some Page',
    )



    content = StreamField(
        [
            ("rich_text", RichTextBlock()),
        ],
        verbose_name="Page Content",
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        RestrictedFieldPanel('some_date', ['Event Management', 'Marketing VPs']),
        RestrictedFieldPanel('some_text'),
        RestrictedFieldPanel('some_rich_text'),
        RestrictedFieldPanel('some_image'),
        RestrictedFieldPanel('some_document'),
        RestrictedFieldPanel('some_product'),
        RestrictedFieldPanel('some_page'),
        # InfoPanel('<span class="editor-reminder">Some important notice to display</span>'),
        # InfoPanel(
        #     '<h5><a target="_blank" href="{{url}}" style="color: blue; text-decoration: underline;">News Article Editors Guide</a></h5>',
        #     value_dict={
        #         'url': [{'module': 'core.utils', 'method': 'page_url', 'slug': 'first-blog', 'target': 'news-article'}]
        #     },
        #     style='text-align: center;'
        #     ),
        # InfoPanel(
        #     '<b>Word Count:</b> {{wordcount}}', {'wordcount': 'wordcount'},
        #     add_hidden_fields=True
        #     ),
        # InfoPanel(
        #     '<div class="tagit">\
        #         Created by <a href="/profiles/{{username}}" style="color: blue; text-decoration: underline;" target="_blank" >\
        #         {{fullname}}</a>.<br>\
        #         First published on {{firstpub}}\
        #      </div>',
        #     value_dict={
        #         'username': ['owner', 'username'],
        #         'fullname': ['owner', 'get_full_name', 'upper'],
        #         'firstpub': 'first_published_at'
        #     },
        #     datetime_format='%d %B %Y'
        #     ),
        # InfoPanel('Random number: {{rnd}}', {'rnd': [{'module': 'random', 'method': 'randint', 'a': 1,'b': 9999}]}),
        # InfoPanel(
        #     'Maximum of 3,56,4,99,5 is {{maximum}}',
        #     {'maximum': [{'module': 'builtins', 'method': 'max', 'args':[3,56,4,99,5]}]}
        #     ),
        # InfoPanel(
        #     '<p class="tagit edit-permission-{{perm}}">You do not have publish permission for this page.</p>',
        #     {'perm': [('permissions_for_user', {'user': ['panel', 'request', 'user']}), 'can_publish']}
        # ),
        # InfoPanel(
        #     text="<h5>Siblings</h5>{{siblings}}",
        #     value_dict={
        #         "siblings": [
        #             {
        #                 "object": "<br>",
        #                 "method": (
        #                     "join",
        #                     {
        #                         "args": {
        #                             "module": "builtins",
        #                             "method": "list",
        #                             "args": [
        #                                 "self",
        #                                 "get_siblings",
        #                                 (
        #                                     "values_list",
        #                                     {"args": ["title"], "flat": True},
        #                                 ),
        #                             ],
        #                         }
        #                     },
        #                 ),
        #             }
        #         ]
        #     },
        # ),
        RestrictedFieldPanel("content"),
    ]

    base_form_class = RestrictedPanelsAdminPageForm

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
