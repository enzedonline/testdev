import json

from django import forms
from django.core.exceptions import ValidationError

from quill.widgets import QuillWidget

from .post import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'content',
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control-lg', 'placeholder': 'Post title'}),
            'content': QuillWidget(),
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
    