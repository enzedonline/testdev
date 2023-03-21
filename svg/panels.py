from django.utils.html import json_script
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel


class SVGFieldPanel(FieldPanel):
    class BoundPanel(FieldPanel.BoundPanel):       

        msg = {
            'file_label': _("Read data from file"),
            'preview': _("Preview"),
            'noScript': _("SVG with embedded JavaScript not supported"),
            'noViewbox': _("SVG must have a valid viewBox attribute"),
            'pleaseEnter': _("Please enter a valid SVG element"),
        }

        def render_html(self, parent_context = None):
            html = super().render_html(parent_context)
            return mark_safe(html + self.import_text_with_preview() + self.json_vars())

        def import_text_with_preview(self):
            return '''
                <label for="''' + self.field_name + '''File"> 
                    <h4 class="w-panel__heading w-panel__heading--label svg-panel-label">
                        ''' + self.msg['file_label'] + '''
                    </h4> 
                </label> 
                <input 
                    type="file" 
                    id="''' + self.field_name + '''File" 
                    accept=".svg" 
                    style="border-style: none; padding: 0; display: block; width: fit-content;" 
                />
                <h4 
                    class="w-panel__heading w-panel__heading--label svg-panel-label" 
                    id="''' + self.field_name + '''-svgPreviewLabel"
                >
                    ''' + self.msg['preview'] + '''
                </h4> 
                <div class="svg-preview" id="''' + self.field_name + '''-svgPreview"></div>
                <script>initialiseSvgPanel()</script>
                '''    

        def json_vars(self):
            return json_script(self.field_name, 'svg_field_name') + \
                   json_script(self.id_for_label(), 'svg_textfield_id') + \
                   json_script(self.msg, 'svg_msg') 

