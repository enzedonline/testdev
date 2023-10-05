from django.db import models
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField
from wagtail.models import (
    DraftStateMixin,
    Locale,
    LockableMixin,
    Page,
    PreviewableMixin,
    RevisionMixin,
    WorkflowMixin,
)
from wagtail.snippets.models import register_snippet


@register_snippet
class Product(
    PreviewableMixin,
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    models.Model,
):
    sku = models.CharField(max_length=10, verbose_name=_("SKU"))
    title = models.CharField(max_length=100, verbose_name=_("Product Title"))
    description = RichTextField(verbose_name=_("Product Description"))
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    icon = "cogs"
    
    panels = [
        FieldPanel("sku"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("image"),
    ]
    
    def __str__(self):
        return f"{self.sku} - {self.title}"

    def get_preview_template(self, request, mode_name):
        return "products/product_detail.html"

class ProductPage(RoutablePageMixin, Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 1

    intro = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    @path("")
    def product_list(self, request):
        products = Product.objects.all()
        return self.render(
            request,
            context_overrides={
                'products': products,
            },
            template="products/product_list.html",
        )

    @path("<str:sku>/")
    def product_detail(self, request, sku):
        product = Product.objects.filter(sku=sku, live=True).first()
        if product:
            return self.render(
                request,
                context_overrides={
                    'product': product.localized,
                },
                template="products/product_detail.html",
            )
        else:
            return HttpResponseRedirect(self.url)
			
    @property
    def preview(self):
        if self.image:
            return self.image