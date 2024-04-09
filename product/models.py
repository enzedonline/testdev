from django.db import models
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

from core.panels.models import SubcategoryChooser
from core.forms.restricted_panels_admin_forms import \
    RestrictedPanelsAdminModelForm

@register_snippet
class StoreDepartment(ClusterableModel):
    base_form_class = RestrictedPanelsAdminModelForm

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
        verbose_name = _("Store Department")
        verbose_name_plural = _("Store Departments")

class DepartmentSubcategory(Orderable):
    department = ParentalKey(
        "StoreDepartment",
        related_name="department_subcategories"
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_("Subcategory Code"),
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
        verbose_name = _("Department Subcategory")
        verbose_name_plural = _("Department Subcategories")
        constraints = [
            models.UniqueConstraint(
                fields=['department', 'name'], 
                name='unique_department_departmentsubcategory_name'
            ),
        ]

class Product(
    PreviewableMixin,
    WorkflowMixin,
    DraftStateMixin,
    LockableMixin,
    RevisionMixin,
    models.Model,
):
    icon = "cogs"
    base_form_class = RestrictedPanelsAdminModelForm
    
    sku = models.CharField(max_length=10, unique=True, verbose_name=_("SKU"))
    title = models.CharField(max_length=100, verbose_name=_("Product Title"))
    description = RichTextField(verbose_name=_("Product Description"))
    dept_subcategory = models.ForeignKey(
        "product.DepartmentSubcategory",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name=_("Department Subcategory"),
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
        SubcategoryChooser(
            "dept_subcategory", 
            category=StoreDepartment, 
            subcategory=DepartmentSubcategory, 
            subcategory_related_name="department_subcategories", 
            search_text=_("Search Department Subcategories")
        ),
        FieldPanel("image"),
    ]

    def __str__(self):
        return f"{self.sku} - {self.title}"
    
    @property
    def preview(self):
        return self.image or self.icon
    
    def get_preview_template(self, request, mode_name):
        return "product/product_preview.html"
    
    def get_department_subcategory(self):
        return f'{self.dept_subcategory.department} - {self.dept_subcategory}'

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
        products = Product.objects.filter(live=True)
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
