from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel
from django.utils.translation import gettext_lazy as _


class SVGFieldPanel(FieldPanel):
    class BoundPanel(FieldPanel.BoundPanel):       
        def render_html(self, parent_context = None):
            html = super().render_html(parent_context)
            return mark_safe(html + self.file_to_text_field_button())

        def file_to_text_field_button(self):
            return '''
                <label for="svgFile"> 
                    <span class="w-panel__heading w-panel__heading--label">''' + _("Read data from file") + '''</span> 
                </label> 
                <input type="file" id="''' + self.field_name + '''File" accept=".svg" style="border-style: none; padding: 0; display: block; width: fit-content;" />
                <p class="w-panel__heading w-panel__heading--label" id="''' + self.field_name + '''-svgPreviewLabel">
                    ''' + _("Preview") + '''
                </p> 
                <div id="''' + self.field_name + '''-svgPreview" style="width: 200px;"></div>
                <script> 
                    const svgFile = document.getElementById("''' + self.field_name + '''File"); 
                    const svgField = document.getElementById("''' + self.id_for_label() + '''")
                    const svgPreview = document.getElementById("''' + self.field_name + '''-svgPreview")
                    const renderPreview = (svg) => {
                        if (svg.includes('<script')) {
                            svgPreview.innerHTML='<p class="error-message">''' + _("SVG with embedded JavaScript not supported") + '''</p>';
                        } else if (svg.includes('<svg') && svg.includes('</svg>')) {
                            svgPreview.innerHTML=svg;
                            svg_tag = svgPreview.getElementsByTagName('svg')[0];
                            svg_tag.removeAttribute('height');
                            svg_tag.removeAttribute('width');
                        } else {
                            svgPreview.innerHTML='<p>''' + _("Please enter a valid SVG element") + '''</p>';
                        }
                    }
                    renderPreview(svgField.value);
                    svgFile.addEventListener("change", (e) => {
                        e.preventDefault(); 
                        const input = svgFile.files[0]; 
                        const reader = new FileReader(); 
                        reader.onload = function (e) {
                            svgField.value = e.target.result; 
                            renderPreview(e.target.result); 
                        }; 
                        reader.readAsText(input); 
                    }); 
                    svgField.addEventListener("input", () => {
                        renderPreview(svgField.value);
                    });
                </script>'''    
