from bs4 import BeautifulSoup
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Prefetch
from django.forms.widgets import HiddenInput
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable


class SubcategoryChooser(FieldPanel):
    """
    FieldPanel with pop-over chooser style form to select subcategories from a ClusterableModel/Orderable class pair where
    the ClusterableModel is assumed to be the category and the orderable the subcategory.
    Chosen category not returned since this is redundant and found by {subcategory}.{ParentalKey field name}
    Chooser modal will present orderable instances (subcategories) grouped by parent ClusterableModel instance (category).
    Search filter will partial match on subcategory names.
    Returns pk of chosen subcategory to hidden input field and displays chosen value as text in form `{category} - {subcategory}`
    Modal title will be the verbose_name used in the `field` definition (the BoundPanel.heading value)
    Inputs:
      category - ClusterableModel class object (display value will be str representation of each instance)
      subcategory - Orderable class object (display value will be str representation of each instance)
      subcategory_related_name - the related_name value passed into the ParentalKey field definition in the subcategory model
      subcategory_sort_order (optional) - sort order for the subcategory groups on the chooser, defaults to 'ordering' meta value
      add_button_text, change_button_text, clear_button_text, search_text, cancel_text, clear_filter_text (optional) - text for the panel and chooser
      standard FieldPanel kwargs with the exception that any widget value passed will be ignored
    """

    def __init__(
            self,
            field_name,
            category,
            subcategory,
            subcategory_related_name,
            subcategory_sort_order=None,
            add_button_text=_("Select"),
            change_button_text=_("Change"),
            clear_button_text=_("Clear Choice"),
            search_text=_("Search"),
            cancel_text=_("Close without changes"),
            clear_filter_text=_("Clear filter"),
            widget=None,
            disable_comments=None,
            permission=None,
            read_only=False,
            **kwargs
    ):
        super().__init__(
            field_name=field_name,
            widget=HiddenInput(),  # override any widget with HiddenInput
            disable_comments=disable_comments,
            permission=permission,
            read_only=read_only,
            **kwargs
        )
        self.category = category
        self.subcategory = subcategory
        self.subcategory_related_name = subcategory_related_name
        self.subcategory_sort_order = subcategory_sort_order or subcategory.Meta.ordering
        self.add_button_text = add_button_text
        self.change_button_text = change_button_text
        self.clear_button_text = clear_button_text
        self.search_text = search_text
        self.cancel_text = cancel_text
        self.clear_filter_text = clear_filter_text

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            category=self.category,
            subcategory=self.subcategory,
            subcategory_related_name=self.subcategory_related_name,
            subcategory_sort_order=self.subcategory_sort_order,
            add_button_text=self.add_button_text,
            change_button_text=self.change_button_text,
            clear_button_text=self.clear_button_text,
            search_text=self.search_text,
            cancel_text=self.cancel_text,
            clear_filter_text=self.clear_filter_text,
        )
        return kwargs

    def on_model_bound(self):
        """
        Check category, subcategory and subcategory_related_name relationship, only in DEBUG mode
        """
        if settings.DEBUG:
            if not issubclass(self.category, ClusterableModel):
                raise ImproperlyConfigured(
                    "Category model must inherit from ClusterableModel.")
            if not issubclass(self.subcategory, Orderable):
                raise ImproperlyConfigured(
                    "Subcategory model must inherit from Orderable.")
            related_field = getattr(
                self.category, self.subcategory_related_name, False)
            if not related_field:
                raise ImproperlyConfigured(
                    f"""
                    subcategory_related_name {self.subcategory_related_name} is not the related_name of a ParentalKey field 
                    in {self.subcategory} or is the related_name of a ParentalKey that does not point to {self.category}.
                    """
                )
            elif not related_field.rel.remote_field.model == self.subcategory:
                raise ImproperlyConfigured(
                    f"""
                    subcategory_related_name {self.subcategory_related_name} is not the related name of a 
                    {self.subcategory.__name__} ParentalKey field that points to {self.category.__name__}.
                    """
                )

    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # display text values for the panel and chooser
            self.opts = {
                "field_id": str(self.id_for_label()),
                "heading": self.heading,
                "add_button_text": self.panel.add_button_text,
                "change_button_text": self.panel.change_button_text,
                "clear_button_text": self.panel.clear_button_text,
                "search_text": self.panel.search_text,
                "cancel_text": self.panel.cancel_text,
                "clear_filter_text": self.panel.clear_filter_text
            }

        def get_categories(self):
            """
            Returns a list of nested dictionaries of categories and associated subcategories
            """
            # Prefetch all categories with related subcategories
            if isinstance(self.panel.subcategory_sort_order, list):
                sort_order = self.panel.subcategory_sort_order 
            else:
                sort_order = [self.panel.subcategory_sort_order]
            categories = self.panel.category.objects.prefetch_related(
                Prefetch(
                    self.panel.subcategory_related_name,
                    queryset=self.panel.subcategory.objects.order_by(*sort_order)
                )
            )
            # Iterate through categories and build the result list
            return [
                {
                    'id': category.id,
                    'name': str(category),
                    'subcategories': [
                        {'id': subcategory.id, 'name': str(subcategory)}
                        for subcategory in getattr(category, self.panel.subcategory_related_name).all()
                    ]
                }
                for category in categories
            ]

        def get_context_data(self, parent_context=None):
            context = super().get_context_data(parent_context)
            # if instance has a subcategory value, construct initial display value
            initial_value = getattr(self.instance, self.field_name)
            if initial_value:
                parental_related_field = getattr(
                    self.panel.category, self.panel.subcategory_related_name).field.name
                initial_value = f'{str(getattr(initial_value, parental_related_field))} - {str(initial_value)}'
            # add panel texts, category list and initial value to panel context
            context.update(
                {
                    "opts": self.opts,
                    "category_index": self.get_categories(),
                    "initial_value": initial_value
                }
            )
            return context

        @mark_safe
        def render_html(self, parent_context=None):
            # manipulate default FieldPanel HTML to append rendered panel template inside Wagtail field wrapper element
            html = super().render_html(parent_context)
            soup = BeautifulSoup(html, "html.parser")
            # create uid on wrapper element
            wrapper = soup.find(class_="w-field__wrapper")
            wrapper["data-subcategory-chooser"] = self.opts["field_id"]
            # add rendered chooser html to wrapper element
            chooser_html = render_to_string(
                "panels/subcategory_chooser.html",
                self.get_context_data()
            )
            wrapper.append(BeautifulSoup(chooser_html, "html.parser"))
            return str(soup)
