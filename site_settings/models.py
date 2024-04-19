from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.blocks import StreamBlock, CharBlock, StructBlock, TextBlock
from wagtail.fields import StreamField

@register_setting(icon='password')
class Tokens(BaseGenericSetting):
    mapbox = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Mapbox Access Token")
    )
    google_analytics = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Google Analytics Site ID")
    )
    facebook_app_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Facebook App ID")
    )
    fontawesome = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("FontAwesome Kit ID")
    )
    openai = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("OpenAI Key")
    )
    gmail_service_account = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("Gmail Service Account Details")
    )


@register_snippet
class TemplateText(ClusterableModel):
    template_set = models.CharField(
        unique=True,
        max_length=50,
        verbose_name="Set Name",
        help_text=_(
            "The set needs to be loaded in template tags then text references as {{set.tag}}")
    )

    panels = [
        FieldPanel("template_set"),
        MultiFieldPanel(
            [
                InlinePanel("templatetext_items"),
            ],
            heading=_("Text Items"),
        ),
    ]

    def __str__(self):
        return self.template_set

    class Meta:
        verbose_name = _('Template Text')


class TemplateTextSetItem(Orderable):
    set = ParentalKey(
        "TemplateText",
        related_name="templatetext_items",
        help_text=_("Template Set to which this item belongs."),
        verbose_name="Set Name",
    )
    template_tag = models.CharField(
        max_length=50,
        help_text=_("Enter a tag without spaces, consisting of lowercase letters, numbers, and underscores.\nThe first character must be a lowercase letter."),
        verbose_name="Template Tag",
    )
    text = models.TextField(
        null=True,
        blank=True,
        help_text=_("The text to be inserted in the template.")
    )

    panels = [
        FieldPanel('template_tag'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.template_tag

    class Meta:
        unique_together = ('set', 'template_tag')
        # constraints = [
        #     models.UniqueConstraint(fields=['set', 'template_tag'], name='unique_set_template_tag')
        # ]


@register_snippet
class NumericRange(models.Model):
    from core.fields.numeric_range import NumericRangeField, NumericRangeScaleOptions
    minmax = NumericRangeField(
        options=NumericRangeScaleOptions(
            min_value=-2, max_value=2, step=0.1, pip_count=11, pip_decimals=2, minor_tick_density=2, pip_prefix='$', unit='c', vertical_labels=True
            )
        )
    title = models.CharField()

class QuestionBlock(StructBlock):
    question = CharBlock()
    help_text = TextBlock()

class QuestionSetBlock(StructBlock):
    title = CharBlock()
    condition = TextBlock()
    questions = StreamBlock(
        [
            ('question', QuestionBlock(label=_("Text Question"))),
        ]
    )

@register_snippet
class Survey(models.Model):
    title = models.CharField(verbose_name=_("Survey Label"))
    question_sets = StreamField(
        [
            ("question_set", QuestionSetBlock()),
        ],
        verbose_name=_("Question Sets"), use_json_field=True
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _('Survey')