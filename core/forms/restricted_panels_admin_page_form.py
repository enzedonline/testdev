from wagtail.admin.forms import WagtailAdminPageForm
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class RestrictedPanelsAdminPageForm(WagtailAdminPageForm):
    """ 
    To be used as baseform for page with RestrictedFieldPanels (direct or inherited).
    For restricted fields only:
    Editor authorised to edit restricted fields if one of the following conditions satisfied:
    - Editor belongs to a role specified in panel.authorised_roles
    - Form is for a new page instance and panel.allow_on_create=True
    - Editor is page owner and panel.allow_for_owner=True (implies allow_on_create)
    - Editor is a member of roles specified in optional settings.RESTRICTED_FIELD_PANEL_OVERRIDE_ROLES
    - Editor is a superuser
    Field will be displayed disabled with warning sub-label and dropped from form on clean if not authorised.
    Field will be dropped from form (and not displayed) if not authorised and panel.hide_if_restricted=True
    No data for non-authorised fields will be submitted.
    If a required field with no default value is not-authorised for a new page instance, an error is displayed.
    - The setting panel.hide_if_restricted=True is ignored in this case.
    - The form will not pass validation in this case.
    For use with auto-filled required fields such as slug, use allow_on_create=True
    For multi-lingual sites, either use gettext_lazy or custom translation model
    Editor language preference can be found in user.wagtail_userprofile.get_preferred_language()
    """
    
    ERROR_NO_DEFAULT = _("Read-only mode for required field with no default value.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.authorised_fields = [] # field must be implicitly authorised to be editable
        self.declined_fields = [] # fields that fail authorisation but are displayed on form
        self.no_default_errors = []
        self.authorise_panels()

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        # strip out disabled fields except for those with no-default-value error
        for field_name in self.declined_fields:
            if field_name in self.no_default_errors: 
                self.add_error(field_name, self.ERROR_NO_DEFAULT)
            else:
                self.fields.pop(field_name, None)
                cleaned_data.pop(field_name, None)
                self.errors.pop(field_name, None)
        return cleaned_data

    @property
    def restricted_panels(self):
        restricted_field_panels = list(getattr(self.Meta, "restricted-field-panels", {}).items())
        restricted_inline_panels = list(getattr(self.Meta, "restricted-inline-panels", {}).items())
        return restricted_field_panels + restricted_inline_panels

    def authorise_panels(self):        
        for field_name, parameters in self.restricted_panels:
            # each item should be a tuple with field name and a list of authorised groups
            hide_if_restricted = parameters.pop('hide_if_restricted', False)
            if self.is_authorised(**parameters):
                self.authorised_fields.append(field_name)
            else:
                if self.field_has_default_error(self.fields[field_name]):
                    # new page with read-only on required field but no default
                    self.no_default_errors.append(field_name)
                    # don't use add_error() here as it requires form.cleaned_data instance
                    self.errors[field_name] = [self.ERROR_NO_DEFAULT]
                if hide_if_restricted and not field_name in self.no_default_errors:
                    # remove from form fields
                    # don't hide if field has error due to new instance with no default value
                    self.fields.pop(field_name, None)
                else:
                    # defer removing field otherwise field is hidden
                    # add to restricted fields for clean
                    self.declined_fields.append(field_name)

    def is_authorised(self, authorised_roles, allow_on_create, allow_for_owner):
        # logic to determine if editor has authorisation on restricted field panel
        try:
            authorised_roles = self.get_authorised_roles(authorised_roles)
            if self.for_user.is_superuser:
                return True
            elif allow_for_owner and self.instance.owner == self.for_user:
                # this includes allow on create since a new instance is owned by the logged in user
                return True
            elif not self.instance.id and allow_on_create:
                return True
            else:
                return self.for_user.groups.get_queryset().filter(
                    name__in=authorised_roles
                ).exists()
        except Exception as e:
            print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")       
            return False

    def field_has_default_error(self, field):
        # new page instance with no default set for restricted field
        return (not self.instance.id) and field.required and (not field.initial)

    def get_authorised_roles(self, user_roles):
        # combine any panel declared authorised user roles with any declared admin roles in settings
        user_roles = (
            user_roles
            if isinstance(user_roles, list)
            else [user_roles]
        )
        admin_roles = getattr(settings, 'RESTRICTED_FIELD_PANEL_OVERRIDE_ROLES', None)
        if admin_roles:
            return [*set(
                user_roles + (
                admin_roles
                if isinstance(admin_roles, list)
                else [admin_roles]
                )
            )]
        else:
            return user_roles
