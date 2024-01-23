from django.db import models
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField
from wagtail.models import (DraftStateMixin, LockableMixin, Orderable, Page,
                            PreviewableMixin, RevisionMixin, WorkflowMixin)
from wagtail.snippets.models import register_snippet

from .panels.category import SubCategoryChooser

class NonBreakingError(Exception):
    pass

@register_snippet
class StoreDepartment(ClusterableModel):
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_("Department Code"),
    )    
    name = models.CharField(
        max_length=50,
        verbose_name=_("Name"),
    )    

    panels = [
        FieldPanel("code"),
        FieldPanel("name"),
        MultiFieldPanel(
            [
                InlinePanel("department_subcategories"),
            ],
            heading=_("Department Subcategories"),
        ),
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

class DepartmentSubcategory(Orderable):
    department = ParentalKey(
        "StoreDepartment",
        related_name="department_subcategories",
        verbose_name=_("Store Department")
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_("Department Code"),
    )    
    name = models.CharField(
        max_length=50,
        verbose_name=_("Name"),
    )    

    panels = [
        FieldPanel("code"),
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Department Product Subcategory")

@register_snippet
class Product(
    PreviewableMixin,
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    models.Model,
):
    icon = "cogs"
    
    sku = models.CharField(max_length=10, unique=True, verbose_name=_("SKU"))
    title = models.CharField(max_length=100, verbose_name=_("Product Title"))
    description = RichTextField(verbose_name=_("Product Description"))
    dept_subcategory = models.ForeignKey(
        "product.DepartmentSubcategory",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name="Product Category",
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    panels = [
        FieldPanel("sku"),
        FieldPanel("title"),
        FieldPanel("description"),
        SubCategoryChooser(
            "dept_subcategory", 
            category=StoreDepartment, 
            subcategory=DepartmentSubcategory, 
            subcategory_related_name="department_subcategories"
        ),
        FieldPanel("image"),
    ]

    def __str__(self):
        return f"{self.sku} - {self.title}"

    def get_preview_template(self, request, mode_name):
        return "products/product_detail.html"


""" 
To list all department categories grouped by store department using Django ORM, you can perform a query 
that involves both StoreDepartment and DepartmentCategory. You can use the prefetch_related to fetch the 
related department_categories for each StoreDepartment efficiently. 
This code does the following:
- Uses prefetch_related to efficiently fetch all StoreDepartment instances with their related department_categories.
- Iterates through each StoreDepartment.
- Prints the department name.
- Iterates through the related department_categories and prints each category name.

Make sure to adjust the sorting or filtering conditions as per your requirements. 
The order_by('sort_order') in the Prefetch is optional and depends on whether you want to retrieve the categories in a specific order.

This approach uses efficient database queries to fetch the related data in a single query, avoiding the N+1 query problem.
"""


class ProductPage(RoutablePageMixin, Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = []
    max_count = 1

    intro = RichTextField()

    content_panels = Page.content_panels + [FieldPanel("intro")]

    @path("")
    @path("index/")
    @path("index/<str:sort>/")
    def product_list(self, request, sort=None):
        products = Product.objects.all()
        if sort:
            try:
                products = products.order_by(sort)
            except Exception as e:
                pass       
        return self.render(
            request,
            context_overrides={
                "products": products,
            },
            template="product/product_list.html",
        )

    @path("delete/")
    def delete_products(self, request):
        product_ids = request.POST.getlist('productIDs[]')
        if product_ids:
            products = Product.objects.filter(id__in=product_ids)
            print(products)
        return HttpResponseRedirect(self.url)
        
    @path("<str:sku>/")
    def product_detail(self, request, sku):
        try:
            product = Product.objects.get(sku=sku, live=True)
            return self.render(
                request,
                context_overrides={
                    "product": product,
                },
                template="product/product_detail.html",
            )
        except Product.DoesNotExist:
            return self.render(
                request,
                context_overrides={
                    "sku": sku,
                },
                template="product/product_not_found.html",
            )
        except Exception as e:
            import logging
            logging.exception(e)  
            return HttpResponseRedirect(self.url)




    @property
    def preview(self):
        if self.image:
            return self.image
