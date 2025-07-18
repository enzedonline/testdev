from wagtail.admin.panels import InlinePanel

class LabelledInlinePanel(InlinePanel):
    class BoundPanel(InlinePanel.BoundPanel):
        template_name = "panels/labelled_inline_panel.html"
