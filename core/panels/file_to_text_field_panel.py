from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel
from django.utils.translation import gettext_lazy as _


class FileToTextFieldPanel(FieldPanel):
    def __init__(self, field_name, file_type_filter=None, *args, **kwargs):
        self.file_type_filter = file_type_filter
        super().__init__(field_name, *args, **kwargs)

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            file_type_filter=self.file_type_filter,
        )
        return kwargs

    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.accepts = (
                f'accept="{self.panel.file_type_filter}" ' if self.panel.file_type_filter else ""
            )


        msg = {
            'file_label': _("Read data from file"),
        }

        def render_html(self, parent_context=None):
            html = super().render_html(parent_context)
            return mark_safe(html + self.file_to_text_field_button())

        def file_to_text_field_button(self):
            file_input_id = f'{self.field_name}File'
            return '''
                <label for="''' + file_input_id + '''"> 
                    <h4 class="w-panel__heading w-panel__heading--label svg-panel-label">
                        ''' + self.msg['file_label'] + '''
                    </h4> 
                </label> 
                <input 
                    type="file" 
                    id="''' + file_input_id + '''" 
                    ''' + self.accepts + ''' 
                    style="border-style: none; padding: 0; display: block; width: fit-content;" 
                />
                <script>
                    input''' + file_input_id + ''' = document.getElementById("''' + file_input_id + '''");
                    textField''' + self.id_for_label() + ''' = document.getElementById("''' + self.id_for_label() + '''");
                    textField''' + self.id_for_label() + '''.style.maxHeight='20em';
                    textField''' + self.id_for_label() + '''.style.overflowY='auto';
                    input''' + file_input_id + '''.addEventListener("change", (e) => {
                        e.preventDefault(); 
                        const input = input''' + file_input_id + '''.files[0]; 
                        const reader = new FileReader(); 
                        reader.onload = function (e) {
                            textField''' + self.id_for_label() + '''.value = e.target.result;
                            textField''' + self.id_for_label() + '''.style.height=0;
                            textField''' + self.id_for_label() + '''.style.height=textField 
                            ''' + self.id_for_label() + '''.scrollHeight + 5 + 'px';
                        }; 
                        reader.readAsText(input); 
                    });                
                </script>
                '''    
