from bs4 import BeautifulSoup
from wagtail.blocks import RichTextBlock


class ParsedRichTextBlock(RichTextBlock):
    pass

    class Meta:
        icon="pilcrow"
        label = "Parsed Rich Text"

    def clean(self, value):

        soup = BeautifulSoup(value.source, "html.parser")
        for item in soup.find_all():
            self.rich_text_parser(item)
        value.source = str(soup)
        return super().clean(value)

    def rich_text_parser(self, element):
        import re
        if element.name != None:
            for child in element.children:
                self.rich_text_parser(child)
            match element.name:
                case 'br':
                    # delete <br> tags
                    element.decompose()
                case 'p':
                    try:
                        if not (element.string == '' or element.string == None):
                            # delete excess white space
                            element.string.replace_with(re.sub(r' +', ' ', element.string).strip())
                        if (element.string == '' or element.string == None) and len(list(element.children)) == 0:
                            # delete empty <p> tags
                            element.decompose()
                    except AttributeError:
                        element.decompose()
