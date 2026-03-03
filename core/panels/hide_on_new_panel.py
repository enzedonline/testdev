from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel

class HideOnNewPanel(FieldPanel):    
    class BoundPanel(FieldPanel.BoundPanel):
        def is_shown(self):
            show_panel = super().is_shown()
            # Do not show this panel if the instance does not exists (i.e. it has no primary key)
            return show_panel and (self.instance.id is not None)
