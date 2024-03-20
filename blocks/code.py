from django.utils.translation import gettext_lazy as _
from wagtail.blocks import ChoiceBlock, StructBlock, TextBlock, StructValue, CharBlock


class CodeChoiceBlock(ChoiceBlock):
    choices=[
        ('python', 'Python'),
        ('css', 'CSS'),
        ('django', 'Django Template'),
        ('javascript', 'Javascript'),
        ('xml', 'HTML / XML'),
        ('shell', 'Bash/Shell'),
        ('json', 'JSON'),
        ('markdown', 'Markdown'),
        ('nginx', 'Nginx'),
        ('sql', 'SQL'),
        ('r', 'R'),
        ('powershell', 'PowerShell'),
    ]

class CollapsibleChoiceBlock(ChoiceBlock):
    choices=[
        ('simple', 'Not Collapsible'),
        ('collapsible', 'Collapsible'),
        ('collapsed', 'Collapsed'),
    ]    

class CodeBlockValue(StructValue):   
    def theme(self) -> str:
        return "stackoverflow-dark"

class BaseCodeBlock(StructBlock):
    title = CharBlock(required=False)
    type = CollapsibleChoiceBlock(required=True, default='simple')
    language = CodeChoiceBlock(default='python')
    code = TextBlock()

    class Meta:
        template = "blocks/code-wrapper.html"
        icon = "code"
        label = _("Code Block")
        label_format = _("Code") + ": {language}"    
        value_class = CodeBlockValue
