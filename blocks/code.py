from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.blocks import (CharBlock, ChoiceBlock, StructBlock, StructValue,
                            TextBlock)
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.telepath import register


class CodeChoiceBlock(ChoiceBlock):
    choices=[
        ('plaintext', _('Plain Text')),
        ('python', 'Python'),
        ('css', 'CSS'),
        ('django', _('Django Template')),
        ('javascript', 'Javascript'),
        ('typescript', 'Typescript'),
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
    title = CharBlock(label=_("Title"), required=False)
    format = CollapsibleChoiceBlock(label=_("Format"), default='simple')
    language = CodeChoiceBlock(label=_("Language"), default='python')
    code = TextBlock(label=_("Code"), )

    class Meta:
        template = "blocks/code-wrapper.html"
        icon = "code"
        label = _("Code Block")
        label_format = _("Code") + ": {language}"    
        value_class = CodeBlockValue
        form_classname = "struct-block code-block"

        
class CodeBlockAdapter(StructBlockAdapter):
    @cached_property
    def media(self):
        return forms.Media(
            css={"all": ("css/admin/code-block.css",)},
        )


register(CodeBlockAdapter(), BaseCodeBlock)