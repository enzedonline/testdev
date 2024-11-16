from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.admin.forms.choosers import BaseFilterForm, LocaleFilterMixin
from wagtail.admin.ui.tables import TitleColumn
from wagtail.admin.views.generic.chooser import (BaseChooseView,
                                                 ChooseResultsViewMixin,
                                                 ChooseViewMixin,
                                                 CreationFormMixin)
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.models import TranslatableMixin


class UserSearchFilterMixin(forms.Form):

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
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query) | 
                Q(email__icontains=search_query)
            )
            self.is_searching = True
            self.search_query = search_query
        return objects

class BaseUserChooseView(BaseChooseView):
    ordering = ["last_name", "first_name"]

    @property
    def columns(self):
        return [
            TitleColumn(
                name="username",
                label=_("Username"),
                accessor="username",
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
            TitleColumn(
                name="get_full_name",
                label=_("Name"),
                accessor="get_full_name",
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
            TitleColumn(
                name="email",
                label=_("Email"),
                accessor="email",
                url_name=self.chosen_url_name,
                link_attrs={"data-chooser-modal-choice": True},
            ),
        ]

    def get_filter_form_class(self):
        bases = [UserSearchFilterMixin, BaseFilterForm]

        i18n_enabled = getattr(settings, "WAGTAIL_I18N_ENABLED", False)
        if i18n_enabled and issubclass(self.model_class, TranslatableMixin):
            bases.insert(0, LocaleFilterMixin)

        return type(
            "FilterForm",
            tuple(bases),
            {},
        )

class UserChooseView(ChooseViewMixin, CreationFormMixin, BaseUserChooseView):
    pass

class UserChooseResultsView(ChooseResultsViewMixin, CreationFormMixin, BaseUserChooseView):
    pass

class UserChooserViewSet(ChooserViewSet):
    model = User

    choose_view_class = UserChooseView
    choose_results_view_class = UserChooseResultsView

    icon = "user"
    choose_one_text = _("Choose a user")
    choose_another_text = _("Choose another user")

    @cached_property
    def widget_class(self):
        widget = super().widget_class
        try:
            widget.show_edit_link = False
        except:
            pass
        return widget

user_chooser_viewset = UserChooserViewSet("user_chooser")
