from django.utils.translation import gettext_lazy as _
# from bs4 import BeautifulSoup
# from django import forms
# from django.contrib.auth.models import User
# from django.db import models
# from django.utils.functional import cached_property
# from django.utils.safestring import mark_safe
# from django.utils.translation import gettext_lazy as _
# from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.panels import (FieldPanel, InlinePanel, MultiFieldPanel,
                                  MultipleChooserPanel)
from wagtail.admin.widgets.slug import SlugInput
# from wagtail.blocks import RawHTMLBlock, RichTextBlock
# from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page

from blocks.models import *

# from core.forms import RestrictedPanelsAdminPageForm
# from core.panels import (ImportTextAreaPanel, M2MChooserPanel, RegexPanel,
#                          RestrictedFieldPanel, RestrictedInlinePanel,
#                          UtilityPanel)
# from core.utils import count_words, get_streamfield_text
# from core.widgets.import_textarea_widget import ImportTextAreaWidget
# from product.blocks import ProductChooserBlock

# from .categories import BlogCategory

class AuthorPanel(FieldPanel):
    class BoundPanel(FieldPanel.BoundPanel):
        def render_html(self, parent_context=None):
            html = super().render_html(parent_context)
            if self.instance.id==None:
                from bs4 import BeautifulSoup
                from django.utils.safestring import mark_safe
                soup = BeautifulSoup(html, "html.parser")
                chosen = soup.find("input")
                chosen['value'] = self.request.user.id
                chooser = soup.find(class_='chooser')
                chooser['class'].remove('blank')
                title = soup.find(class_='chooser__title')
                title.string = self.request.user.__str__()
                html = mark_safe(str(soup))
            return html
        
class BlogIndex(Page):
    from wagtail.fields import RichTextField
    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogPage', 'blog.VideoPage']
    max_count = 1

    intro = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

class CarouselImages(Orderable):
    from django.db import models
    from modelcluster.fields import ParentalKey
    from wagtail.fields import RichTextField

    """Between 1 and 5 images for the blog page carousel."""

    page = ParentalKey("blog.BlogPage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Image",
    )
    caption = RichTextField(null=True, blank=True)
    some_date = models.DateTimeField(
        null=True, blank=True, help_text="Some helpful text"
    )
    some_text = models.CharField(max_length=255, default="some default value")
    some_text_area = models.TextField(default="some default value")
    some_choice_field = models.CharField(
        max_length=255,
        default="a",
        choices=[("a", "Choice A"), ("b", "Choice B"), ("c", "Choice C")],
    )

    panels = [
        FieldPanel("carousel_image"),
        FieldPanel("caption"),
        FieldPanel("some_date"),
        FieldPanel("some_text"),
        FieldPanel("some_text_area"),
        FieldPanel("some_choice_field"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Carousel Image"


class BlogPage(Page):
    from django.contrib.auth.models import User
    from django.db import models
    from django.utils.functional import cached_property
    from django.utils.translation import gettext_lazy as _
    from modelcluster.fields import ParentalManyToManyField
    from wagtail.blocks import RawHTMLBlock, RichTextBlock
    from wagtail.fields import RichTextField, StreamField

    from blocks.models import (CollapsibleCardBlock, CSVTableBlock,
                               ExternalLinkEmbedBlock, FlexCardBlock,
                               HeadingBlock, ImportTextBlock, LinkBlock,
                               SEOImageChooserBlock)
    from core.forms.restricted_panels_admin_forms import \
        RestrictedPanelsAdminPageForm
    from core.panels.models import (ImportTextAreaPanel, M2MChooserPanel,
                                    RegexPanel, RestrictedFieldPanel,
                                    RestrictedInlinePanel, UtilityPanel)
    from core.widgets.import_textarea_widget import ImportTextAreaWidget
    from core.widgets.input_char_limit import (CharLimitTextArea,
                                               CharLimitTextInput)
    from product.blocks import ProductChooserBlock

    from .categories import BlogCategory

    parent_page_types = ['blog.BlogIndex']
    subpage_types = []
    wordcount = models.IntegerField(
        null=True, blank=True, verbose_name="Word Count", default=0
    )
    author = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    some_date = models.DateTimeField(
        null=True, blank=True, help_text="Some helpful text"
    )
    some_text = models.CharField(null=True, blank=True, max_length=255, default="some default value")
    some_text_area = models.TextField(null=True, blank=True)
    some_rich_text = RichTextField(null=True, blank=True, editor="basic")
    some_slug = models.SlugField(null=True, blank=True)
    some_choice_field = models.CharField(
        max_length=255,
        default="a",
        choices=[("a", "Choice A"), ("b", "Choice B"), ("c", "Choice C")],
    )
    some_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Some Image",
    )
    some_document = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Some Document",
    )
    # some_product = models.ForeignKey(
    #     "product.Product",
    #     null=True,
    #     blank=True,
    #     related_name="+",
    #     on_delete=models.SET_NULL,
    #     verbose_name="Product",
    # )
    some_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Some Page",
    )
    content = StreamField(
        [
            ("rich_text", RichTextBlock()),
            ("html", RawHTMLBlock()),
            ("code", BaseCodeBlock()),
            ("import_text_block", ImportTextBlock()),
            ("csv_table", CSVTableBlock()),
            ("collapsible_card_block", CollapsibleCardBlock()),
            ("product", ProductChooserBlock()),
            ("external_link", ExternalLinkEmbedBlock()),
            ("link", LinkBlock(required=False)),
            ("flex_card", FlexCardBlock()),
            ("seo_image", SEOImageChooserBlock()),
            ("heading", HeadingBlock()),
            ("django_template_fragment", DjangoTemplateFragmentBlock()),
        ],
        verbose_name="Page Content",
        blank=True,
        use_json_field=True,
        # block_counts={'heading': {'min_num': 1, 'max_num': 1},}
    )
    categories = ParentalManyToManyField(
        BlogCategory,
        verbose_name=_("Blog Categories"),
        related_name="categories",
    )

    content_panels = Page.content_panels + [
        # AuthorPanel('author'),
        # UtilityPanel(
        #     '<b>Word Count:</b> {{wordcount}}', {'wordcount': 'wordcount'},
        #     style = 'margin-bottom: 2em;display: block;background-color: antiquewhite;padding: 1em;border-radius: 1em;'
        # ),
        # FieldPanel('owner'),
        # RegexPanel('some_slug'),
        # ImportTextFieldPanel('some_text_area', file_type_filter=".csv, .tsv"),
        # MultiFieldPanel(
        #     [RestrictedInlinePanel("carousel_images", max_num=5, min_num=1)],
        #     heading="Carousel Images",
        # ),
        # RestrictedFieldPanel('some_date'),
        # FieldPanel('some_text', widget=CharLimitTextInput(min=10, max=20, enforced=True)),
        # FieldPanel('some_text_area', widget=CharLimitTextArea(min=10, max=20)),
        # ImportTextAreaPanel('some_text_area', file_type_filter='.csv'),
        # RestrictedFieldPanel('some_choice_field'),
        # RestrictedFieldPanel('some_rich_text'),
        # RestrictedFieldPanel('some_image'),
        # RestrictedFieldPanel('some_document'),
        # FieldPanel("some_product"),
        # RestrictedFieldPanel('some_page'),
        FieldPanel("content"),
        # UtilityPanel('<span class="editor-reminder">Some important notice to display</span>'),
        # UtilityPanel(
        #     '<h5><a target="_blank" href="{{url}}" style="color: blue; text-decoration: underline;">News Article Editors Guide</a></h5>',
        #     value_dict={
        #         'url': [{'module': 'core.utils', 'method': 'page_url', 'slug': 'first-blog', 'target': 'news-article'}]
        #     },
        #     style='text-align: center;'
        #     ),
        # UtilityPanel(
        #     '<b>Word Count:</b> {{wordcount}}', {'wordcount': 'wordcount'},
        #     add_hidden_fields=True
        #     ),
        # UtilityPanel(
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
        # UtilityPanel('Random number: {{rnd}}', {'rnd': [{'module': 'random', 'method': 'randint', 'a': 1,'b': 9999}]}),
        # UtilityPanel(
        #     'Maximum of 3,56,4,99,5 is {{maximum}}',
        #     {'maximum': [{'module': 'builtins', 'method': 'max', 'args':[3,56,4,99,5]}]}
        #     ),
        # UtilityPanel(
        #     '<p class="tagit edit-permission-{{perm}}">You do not have publish permission for this page.</p>',
        #     {'perm': [('permissions_for_user', {'user': ['panel', 'request', 'user']}), 'can_publish']}
        # ),
        # UtilityPanel(
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
        # FieldPanel('some_text_area'),
        # UtilityPanel(
        #     '{{file_reader}}',
        #     {
        #         'file_reader': {'module': 'core.utils', 'method': 'import_text_field_button', 'field': 'some_text_area'}
        #     }
        # ),
        M2MChooserPanel("categories"),
    ]

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug', widget=SlugInput),
            FieldPanel('seo_title', widget=CharLimitTextInput(min=15, max=70, enforced=True)),
            FieldPanel('search_description', widget=CharLimitTextArea(min=50, max=160, enforced=False)),
        ], _('For search engines')),
    ]

    base_form_class = RestrictedPanelsAdminPageForm

    class Meta:
        verbose_name = "Blog Page"

    @cached_property
    def corpus(self):
        from core.utils import get_streamfield_text
        return get_streamfield_text(self.content)

    @cached_property
    def words(self, corpus=None):
        from core.utils import count_words
        if not corpus:
            corpus = self.corpus
        return count_words(corpus)
