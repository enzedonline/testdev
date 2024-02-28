from django.utils.translation import gettext_lazy as _
from wagtail.blocks import ChoiceBlock, StructBlock, TextBlock, StructValue


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

class CodeBlockValue(StructValue):   
    def theme(self) -> str:
        return "stackoverflow-dark"

class BaseCodeBlock(StructBlock):
    language = CodeChoiceBlock(default='python')
    code = TextBlock()

    class Meta:
        template = "blocks/code_block.html"
        icon = "code"
        label = _("Code Block")
        label_format = _("Code") + ": {language}"    
        value_class = CodeBlockValue
