from wagtail.admin.panels import Panel, FieldPanel

class RestrictedPanel(Panel):
    def __init__(self, authorised_groups, **kwargs):
        self.authorised_groups = authorised_groups if isinstance(authorised_groups, list) else [authorised_groups]
        super().__init__(self.field_name, **kwargs)

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            authorised_groups=self.authorised_groups
        )
        return kwargs

    class BoundPanel(Panel.BoundPanel):
        def is_shown(self):
            show_field = super().is_shown()
            is_authorised = self.request.user.groups.get_queryset().filter(name__in=self.panel.authorised_groups).exists()
            return (show_field and is_authorised)
