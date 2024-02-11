from django import forms
from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from wagtail.admin.forms.choosers import BaseFilterForm, LocaleFilterMixin
from wagtail.admin.ui.tables import Column, TitleColumn, UpdatedAtColumn
from wagtail.models import TranslatableMixin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.chooser import (BaseSnippetChooseView,
                                            ChooseResultsView, ChooseView)
from wagtail.snippets.views.snippets import SnippetViewSet

from core.viewsets.columns import ImageColumn
from core.widgets.models import SnippetPreviewChooserViewSet

from .models import Product


class ProductViewSet(SnippetViewSet):
    model = Product
    list_display = ["title", "sku", "get_department_subcategory", ImageColumn("image"), UpdatedAtColumn()]
    list_filter = {"title": ["icontains"], "sku": ["icontains"], "dept_subcategory": ["exact"]}
    list_per_page = 50
    ordering = ["sku"]

setattr(Product.get_department_subcategory, 'admin_order_field', "dept_subcategory")
setattr(Product.get_department_subcategory, 'short_description', Product.dept_subcategory.field.verbose_name)
register_snippet(ProductViewSet)

class ProductFilterMixin(forms.Form):

    q = forms.CharField(
        label=_("Search term"),
        widget=forms.TextInput(attrs={"placeholder": _("Search")}),
        required=False,
    )

    def filter(self, objects):
        objects = super().filter(objects)
        search_query = self.cleaned_data.get("q")
        if search_query:
            objects = objects.filter(
                Q(title__icontains=search_query) |
                Q(sku__icontains=search_query) |
                Q(dept_subcategory__name__icontains=search_query) |
                Q(dept_subcategory__department__name__icontains=search_query) 
            )
            self.is_searching = True
            self.search_query = search_query
        return objects
    
class BaseProductChooseView(BaseSnippetChooseView):
    ordering=["sku"]
    @property
    def columns(self):
        return [
            ImageColumn(
                name="image",
                label="",
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
            TitleColumn(
                name="sku",
                label=_("SKU"),
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
            TitleColumn(
                name="title",
                label=_("Title"),
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
            Column(
                name="get_department_subcategory",
                label=_("Category"),
            ),
        ]
    
    def get_filter_form_class(self):
        bases = [ProductFilterMixin, BaseFilterForm]

        i18n_enabled = getattr(settings, "WAGTAIL_I18N_ENABLED", False)
        if i18n_enabled and issubclass(self.model_class, TranslatableMixin):
            bases.insert(0, LocaleFilterMixin)

        return type(
            "FilterForm",
            tuple(bases),
            {},
        )
    
class ProductChooseView(ChooseView, BaseProductChooseView):
    pass

class ProductChooseResultsView(ChooseResultsView, BaseProductChooseView):
    pass

class ProductChooserViewSet(SnippetPreviewChooserViewSet):
    model = Product
    choose_view_class = ProductChooseView
    choose_results_view_class = ProductChooseResultsView


product_chooser_viewset = ProductChooserViewSet()
