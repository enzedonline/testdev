import json
from collections.abc import Mapping
from urllib.parse import urlparse

from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.renderers import get_default_renderer
from django.forms.utils import flatatt
from django.templatetags.static import static
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.safestring import mark_safe

from .config import DEFAULT_CONFIG, MEDIA_CSS, MEDIA_JS, TOOLBAR_LABELS

__all__ = (
    "LazyEncoder",
    "QuillWidget",
)


def is_absolute_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_str(obj)
        return super(LazyEncoder, self).default(obj)


json_encode = LazyEncoder().encode


def convert_lazy_to_str(obj):
    if isinstance(obj, Promise):
        return str(obj)
    return obj


class QuillWidget(forms.Textarea):
    class Media:
        def widget_js():
            custom_js = getattr(settings, "QUILL_MEDIA_JS", None)
            if custom_js:
                return [url if is_absolute_url(url) else static(url) for url in custom_js]
            else:
                return MEDIA_JS

        def widget_css():
            custom_css = getattr(settings, "QUILL_MEDIA_CSS", None)
            if custom_css:
                return [url if is_absolute_url(url) else static(url) for url in custom_css]
            else:
                return MEDIA_CSS
        js = widget_js()
        css = {"all": widget_css()}

    def __init__(self, config_name="default", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = DEFAULT_CONFIG.copy()
        configs = getattr(settings, "QUILL_CONFIGS", None)
        if configs:
            if isinstance(configs, Mapping):
                if config_name in configs:
                    config = configs[config_name]
                    if not isinstance(config, Mapping):
                        raise ImproperlyConfigured(
                            'QUILL_CONFIGS["%s"] setting must be a Mapping object'
                            % config_name
                        )
                    self.config.update(config)
                else:
                    raise ImproperlyConfigured(
                        'No configuration named "%s" found in your QUILL_CONFIGS'
                        % config_name
                    )
            else:
                raise ImproperlyConfigured(
                    "QUILL_CONFIGS settings must be a Mapping object"
                )
        self.toolbar_labels = TOOLBAR_LABELS.copy()
        toolbar_labels = getattr(settings, "QUILL_TOOLBAR_LABELS", None)
        if toolbar_labels and isinstance(toolbar_labels, list) and all(isinstance(item, tuple) for item in toolbar_labels):
            dict_toolbar_labels = dict(self.toolbar_labels)
            for key, value in toolbar_labels:
                dict_toolbar_labels[key] = value
            self.toolbar_labels = list(dict_toolbar_labels)

    def render(self, name, value, attrs=None, renderer=None):
        if renderer is None:
            renderer = get_default_renderer()
        if value is None:
            value = ""

        attrs = attrs or {}
        attrs["name"] = name
        if hasattr(value, "quill"):
            attrs["quill"] = value.quill
        else:
            attrs["value"] = value
        final_attrs = self.build_attrs(self.attrs, attrs)
        labels = [(convert_lazy_to_str(k), convert_lazy_to_str(v))
                  for k, v in self.toolbar_labels]
        return mark_safe(
            renderer.render(
                "quill/widget.html",
                {
                    "final_attrs": flatatt(final_attrs),
                    "id": final_attrs["id"],
                    "name": final_attrs["name"],
                    "config": json_encode(self.config),
                    "quill": final_attrs.get("quill", None),
                    "value": final_attrs.get("value", None),
                    "labels": json.dumps(labels),
                },
            )
        )
