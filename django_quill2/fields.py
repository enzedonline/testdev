import copy
import html
import json
import logging
import re

import execjs
from bs4 import BeautifulSoup, NavigableString
from django.contrib.staticfiles import finders
from django.db import models

from .forms import QuillFormField
from .quill import Quill

__all__ = (
    "FieldQuill",
    "QuillDescriptor",
    "QuillField",
)


class FieldQuill:
    def __init__(self, instance, field, json_string):
        self.instance = instance
        self.field = field
        self.json_string = json_string or '{"delta":"","html":""}'
        self._committed = True

    def __eq__(self, other):
        if hasattr(other, "json_string"):
            return self.json_string == other.json_string
        return self.json_string == other

    def __hash__(self):
        return hash(self.json_string)

    def _require_quill(self):
        if not self:
            raise ValueError(
                "The '%s' attribute has no Quill JSON String associated with it."
                % self.field.name
            )

    def _get_quill(self):
        self._require_quill()
        self._quill = Quill(self.json_string)
        return self._quill

    def _set_quill(self, quill):
        self._quill = quill

    def _del_quill(self):
        del self._quill

    quill = property(_get_quill, _set_quill, _del_quill)

    @property
    def html(self):
        self._require_quill()
        return self.quill.html

    @property
    def delta(self):
        self._require_quill()
        return self.quill.delta

    @property
    def plain(self):
        self._require_quill()
        return self.quill.plain

    def save(self, json_string, save=True):
        setattr(self.instance, self.field.name, json_string)
        self._committed = True
        if save:
            self.instance.save()


class QuillDescriptor:
    def __init__(self, field):
        self.field = field

    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        if self.field.name in instance.__dict__:
            quill = instance.__dict__[self.field.name]
        else:
            instance.refresh_from_db(fields=[self.field.name])
            quill = getattr(instance, self.field.name)

        if isinstance(quill, str) or quill is None:
            attr = self.field.attr_class(instance, self.field, quill)
            instance.__dict__[self.field.name] = attr

        elif isinstance(quill, Quill) and not isinstance(quill, FieldQuill):
            quill_copy = self.field.attr_class(
                instance, self.field, quill.json_string)
            quill_copy.quill = quill
            quill_copy._committed = False
            instance.__dict__[self.field.name] = quill_copy

        elif isinstance(quill, FieldQuill) and not hasattr(quill, "field"):
            quill.instance = instance
            quill.field = self.field

        elif isinstance(quill, FieldQuill) and instance is not quill.instance:
            quill.instance = instance

        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value


class QuillField(models.TextField):
    attr_class = FieldQuill
    descriptor_class = QuillDescriptor

    def formfield(self, **kwargs):
        kwargs.update({"form_class": QuillFormField})
        return super().formfield(**kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def _get_form_class():
        return QuillFormField

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        """
        Expect a JSON string with 'delta' and 'html' keys
        ex) b'{"delta": "...", "html": "..."}'
        :param value: JSON string with 'delta' and 'html' keys
        :return: Quill's 'Delta' JSON String
        """
        if isinstance(value, Quill):
            return value
        if isinstance(value, FieldQuill):
            return value.quill
        if value is None or isinstance(value, str):
            return value
        return Quill(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return value
        if isinstance(value, Quill):
            return value.json_string
        return value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def clean(self, value, model_instance):
        # fix issues with value returned from quill.getSemanticHTML()
        # 1. video embeds returned as hyperlink - recreate iframe
        # 2. code blocks returned as simple <pre data-language>...</pre>
        #    wrap inner text in <code class="language-xx"> to enable
        #    highlighting with hljs.highlightAll()
        # Finally, wrap returned html in "quill-rich-text" div container
        quill_html = copy.copy(value.html)
        quill_html = self.fix_embeds(value.delta, quill_html)
        quill_html = self.fix_code(quill_html)
        quill_html = f'<div class="quill-rich-text">{quill_html}</div>'
        value.json_string = json.dumps({'delta': value.delta, 'html': quill_html})
        return super().clean(value, model_instance)

    def fix_embeds(self, delta, quill_html):
        # getSemanticHTML returns anchor link in place of iframe
        # search delta for video insterts, replace corresponding anchor link with iframe + attributes
        try:
            videos = []
            for op in json.loads(delta)['ops']:
                if 'insert' in op and isinstance(op['insert'], dict) and 'video' in op['insert']:
                    video_info = {
                        'url': op['insert']['video'],
                        'height': op.get('attributes', {}).get('height'),
                        'width': op.get('attributes', {}).get('width'),
                        'iframeAlign': op.get('attributes', {}).get('iframeAlign')
                    }
                    videos.append(video_info)
            if videos:
                for video in videos:
                    video_url = video['url']
                    height = video['height']
                    width = video['width']
                    iframe_align = video['iframeAlign']

                    # Construct the iframe HTML
                    iframe_html = f'<iframe src="{video_url}"'
                    if width:
                        iframe_html += f' width="{width}px"'
                    if height:
                        iframe_html += f' height="{height}px"'
                    if iframe_align:
                        iframe_html += f' class="ql-iframe-align-{iframe_align}"'
                    iframe_html += '></iframe>'

                    # Replace the anchor tag with the iframe in the HTML string
                    quill_html = re.sub(
                        rf'<a href="{re.escape(video_url)}">{re.escape(video_url)}</a>',
                        iframe_html,
                        quill_html
                    )
        except Exception as e:
            logging.warning(
                f"\n{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
            )
        return quill_html 


    def fix_code(self, quill_html):
        # getSemanticHTML converts code to block to <pre data-language>...</pre>
        # wrap pre inner html in a code block, set class value from data-language value
        # strip data-language attribute from pre block
        try:
            soup = BeautifulSoup(quill_html, 'html.parser')
            for pre in soup.find_all('pre', attrs={'data-language': True}):
                # Create a new <code> tag
                code_tag = soup.new_tag('code')
                # Move the contents of <pre> to the new <code> tag, strip leading/trailing \n
                code_tag.string = pre.get_text(strip=True, separator='\n').strip('\n')
                # Add the language class to the <code> tag
                code_tag['class'] = f'language-{pre["data-language"]}'
                # Clear the contents of <pre> and insert the <code> tag
                pre.clear()
                del pre.attrs['data-language']
                pre.append(code_tag)
            return str(soup)
        except Exception as e:
            logging.warning(
                f"\n{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
            )
            return quill_html
