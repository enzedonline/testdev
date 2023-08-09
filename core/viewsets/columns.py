from wagtail.admin.ui.tables import TitleColumn

class ImageColumn(TitleColumn):
    cell_template_name = "viewsets/image_cell.html"