from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.users.forms import UserEditForm, UserCreationForm


class CustomUserEditForm(UserEditForm):
    address = forms.CharField(required=True, label=_("Address"))


class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(required=True, label=_("Address"))
