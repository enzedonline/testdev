import json

from django import forms
from django.core.exceptions import ValidationError
from django_tiptap.widgets import TipTapWidget

from quill.widgets import QuillWidget

from .post import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'tiptap',
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'content': QuillWidget(attrs={'class': 'form-control'}),
            'tiptap': TipTapWidget(attrs={'class': 'form-control'}),
        }
        pass

    def clean_content(self):
        content = self.cleaned_data.get('content')
        try:
            content_json = json.loads(content)
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON format")
        if 'html' not in content_json or not content_json['html']:
            raise ValidationError("This field is required")
        return content
    