from bs4 import BeautifulSoup
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel


class ProductCategoryPanel(FieldPanel):
    """
    FieldPanel with pop-over chooser style form to select Product Categories.
    """

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            widget=None,
        )
        return kwargs

    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.opts = {
                "field_id": str(self.id_for_label()),
                "heading": self.heading,
                "select_button_text": _("Select Category"),
                "change_button_text": _("Change Category"),
                "search_text": _("Search"),
                "cancel_text": _("Close without changes"),
                "clear_filter_text": _("Clear filter")
            }

        def get_context_data(self, parent_context=None):
            context = super().get_context_data(parent_context)
            context.update(
                {
                    "opts": self.opts,
                    "category_index": self.panel.model.get_categories()
                }
            )
            return context

        def render_html(self, parent_context=None):
            html = super().render_html(parent_context)
            soup = BeautifulSoup(html, "html.parser")
            select = soup.find("select")
            if not select:
                raise ImproperlyConfigured(_("The <select> element was not found."))
            else:
                # hide default select element
                select["hidden"] = "true"
            # create uid on wrapper element
            wrapper = soup.find(class_="w-field__wrapper")
            wrapper["class"] = wrapper.get("class", []) + [
                f'product-category-chooser-{self.opts["field_id"]}'
            ]
            # add rendered chooser html to wrapper element
            chooser_html = render_to_string(
                "panels/product_category_chooser.html", 
                self.get_context_data()
            )
            wrapper.append(BeautifulSoup(chooser_html, "html.parser"))
            return mark_safe(str(soup))

