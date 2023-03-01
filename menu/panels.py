from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel
from django.utils.translation import gettext_lazy as _


class FileToTextFieldPanel(FieldPanel):
    class BoundPanel(FieldPanel.BoundPanel):       
        def render_html(self, parent_context = None):
            html = super().render_html(parent_context)
            return mark_safe(html + self.file_to_text_field_button())

        def file_to_text_field_button(self):
            return '''
                <label for="svgFile"> 
                    <span class="w-panel__heading w-panel__heading--label">''' + _("Read data from file") + '''</span> 
                </label> 
                <input type="file" id="''' + self.field_name + '''File" accept=".svg" style="border-style: none; padding: 0;" />
                <script> 
                    const svgFile = document.getElementById("''' + self.field_name + '''File"); 
                    svgFile.addEventListener("change", (e) => {
                        e.preventDefault(); 
                        const input = svgFile.files[0]; 
                        const reader = new FileReader(); 
                        reader.onload = function (e) {
                            const svgField = document.getElementById("''' + self.id_for_label() + '''"); 
                            svgField.value = e.target.result; 
                        }; 
                        reader.readAsText(input); 
                    }); 
                </script>'''    
