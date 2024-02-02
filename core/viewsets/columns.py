from wagtail.admin.ui.tables import TitleColumn
from django.utils.safestring import mark_safe

class ImageColumn(TitleColumn):
    def get_cell_context_data(self, instance, parent_context):
        context = super().get_cell_context_data(instance, parent_context)
        try:
            context['value'] = mark_safe(
                context['value'].get_rendition('height-50').img_tag({'class':"show-transparency"})
                )
        except:
            context['value'] = mark_safe(
                '<svg class="icon icon-image" height="50px" viewBox="0 0 24 24" aria-hidden="true"><use href="#icon-image"></use></svg>'
                )
        return context

