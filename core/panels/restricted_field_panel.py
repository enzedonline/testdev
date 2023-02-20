from bs4 import BeautifulSoup
from core.forms import RestrictedPanelsAdminPageForm
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.admin.rich_text.editors.draftail import DraftailRichTextArea
from wagtail.admin.widgets import AdminPageChooser
from wagtail.blocks.base import BlockField
from wagtail.blocks.stream_block import StreamBlock
from wagtail.documents.widgets import AdminDocumentChooser
from wagtail.images.widgets import AdminImageChooser
from wagtail.snippets.widgets import AdminSnippetChooser


class RestrictedFieldPanel(FieldPanel):
    """
    
    Custom css classes:
        restricted-field-warning - formats read-only label, supplements wagtail help class
        disabled-display-field - formats disabled rich-text fields, streamfields and fallback/error returns
    """
    def __init__(
        self,
        field_name,
        authorised_roles=[],
        allow_on_create=False,
        allow_for_owner=False,
        hide_if_restricted=False,
        **kwargs,
    ):
        super().__init__(field_name, **kwargs)
        self.field_name = field_name
        self.authorised_roles = (
            authorised_roles
            if isinstance(authorised_roles, list)
            else [authorised_roles]
        )
        self.allow_on_create = allow_on_create
        self.allow_for_owner = allow_for_owner
        self.hide_if_restricted = hide_if_restricted

    def clone_kwargs(self):
        kwargs = super().clone_kwargs()
        kwargs.update(
            authorised_roles=self.authorised_roles,
            allow_on_create=self.allow_on_create,
            allow_for_owner=self.allow_for_owner,
            hide_if_restricted=self.hide_if_restricted,
        )
        return kwargs

    def get_form_options(self):
        opts = {"restricted": []}
        opts = opts | super().get_form_options()
        opts["restricted-field-panels"] = {
            self.field_name: {
                'authorised_roles': self.authorised_roles,
                'allow_on_create': self.allow_on_create,
                'allow_for_owner': self.allow_for_owner,
                'hide_if_restricted': self.hide_if_restricted,
            }
        }
        return opts

    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.is_authorised = (
                getattr(self, 'field_name', None) in getattr(self.form, 'authorised_panels', [])
            )
            self.base_form_error = self._has_base_form_error()
            self.render_soup = None

        def render_html(self, parent_context=None):
            if self.base_form_error:
                return mark_safe(f'<p class="disabled-display-field">{_("Base Form Error")}</p>')
            else:
                return (
                    super().render_html(parent_context)
                    if self.is_authorised
                    else self.disable_input(parent_context)
                )

        def disable_input(self, parent_context):
            # default render, set input element to disabled, add warning sub-label
            # not called if hide_if_restricted=True and no default error
            field = object
            if self.field_name in self.form.fields.keys():
                field = self.form.fields[self.field_name]
                field.disabled = True
            widget = getattr(field, 'widget', None)

            try:
                if (
                    issubclass(field.__class__, BlockField) 
                    and issubclass(field.block.__class__, StreamBlock)
                    ):
                    return self.render_streamfield()

                # RichTextField just render contents as html
                if issubclass(widget.__class__, DraftailRichTextArea):
                    return self.render_richtextfield()

                # Render html and button elements
                html = super().render_html(parent_context)
                self.render_soup = BeautifulSoup(html, "html.parser")

                # strip all scripts and link buttons
                for element in self.render_soup('a', class_='button') + self.render_soup('script'): 
                    element.extract()

                # strip all buttons except for comment buttons
                for element in self.render_soup('button'):
                    if not (
                        element.has_attr('class') 
                        and 'w-field__comment-button' in element["class"]
                        ):
                        element.extract()

                # add default display for empty choosers
                if not getattr(self.form.instance, self.field_name, False):
                    unchosen = self.render_soup.find(class_="unchosen")
                    if unchosen:
                        unchosen = self.render_empty_chooser(widget, unchosen)

                # look for input field
                input = self.render_soup.find("input")
                if input:
                    # Add hover title and warning label, force input to disabled (in case field=None)
                    if self.panel.authorised_roles:
                        input["title"] = f'{_("Restricted to")} {", ".join(self.panel.authorised_roles)}'
                    input["disabled"] = ''
                    self.render_soup.append(self.warning_label)
                    return mark_safe(self.render_soup.renderContents().decode("utf-8"))

            except Exception as e:
                print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")       

            # fallback in case of error or widget/field type not handled above
            return mark_safe(
                f'<p class="disabled-display-field">{_("Restricted Field")}</p>{str(self.warning_label)}'
            )

        def render_richtextfield(self):
            # RichTextField - CharField with DraftailRichTextArea widget
            # Return instance value (plain HTML)
            return mark_safe(
                f'<div class="disabled-display-field">\
                {getattr(self.form.instance, self.field_name, {_("Restricted Field")})}</div>\
                {str(self.warning_label)}'
            )

        def render_streamfield(self):   
            # Return rendered streamfield in collapsed <details> tag if streamfield has value
            # Add input field field_name-count with value=0 
            # field validation uses this pre-clean - because we don't return anything, count needs to be 0
            soup = BeautifulSoup()
            streamfield = soup.new_tag('div')
            streamfield_value = getattr(self.form.instance, self.field_name, None)
            contents_container = soup.new_tag('div')
            contents_container['class'] = 'disabled-display-field'
            contents_container['style'] = 'margin-top: 1em;'

            if streamfield_value:
                svg_id = f'{self.field_name}-toggler'
                toggler_animation = soup.new_tag('style')
                streamfield.append(toggler_animation)
                toggler_animation.append(
                    f'[open] svg#content-toggler {{transform: rotate(0deg);}} svg#content-toggler {{transform: rotate(-90deg);}}'
                )
                streamfield_contents = BeautifulSoup(streamfield_value.render_as_block(), 'html.parser')
                details = soup.new_tag('details')
                streamfield.append(details)
                summary = soup.new_tag('summary')
                details.append(summary)
                summary_heading = soup.new_tag('a')
                summary.append(summary_heading)
                summary_heading['style'] = 'cursor: pointer;'
                svg = soup.new_tag('svg')
                summary_heading.append(svg)
                svg['class'] = 'icon w-panel__icon restricted-streamfield-arrow'
                svg['id'] = svg_id
                use = soup.new_tag('use')
                svg.append(use)
                use['href'] = "#icon-arrow-down-big"
                summary_heading_text = soup.new_tag('span')
                summary_heading.append(summary_heading_text)
                summary_heading_text['style'] = "padding-left: 1em;"
                summary_heading_text.string = f'{_("StreamField Contents")}'
                details.append(contents_container)
            else:
                streamfield_contents = soup.new_tag('p')
                streamfield_contents.string = f'{_("Empty Streamfield")}'
                streamfield.append(contents_container)

            contents_container.append(streamfield_contents)
            input_field = soup.new_tag('input')
            streamfield.append(input_field)
            input_field['type'] = 'hidden'
            input_field['name'] = f'{self.field_name}-count'
            input_field['data-streamfield-stream-count'] = ''
            input_field['value'] = '0'
            streamfield.append(self.warning_label)
            return mark_safe(streamfield.renderContents().decode("utf-8"))

        def render_empty_chooser(self, widget, unchosen):

            svg_icon_href = None
            soup = BeautifulSoup()
            unchosen.clear()
            widget_class = widget.__class__

            if issubclass(widget_class, AdminImageChooser):
                svg_icon_href = 'icon-image'
            elif issubclass(widget_class, AdminDocumentChooser):
                svg_icon_href = 'icon-doc-full-inverse'
            elif issubclass(widget_class, AdminPageChooser):
                svg_icon_href = 'icon-doc-empty-inverse'
            elif issubclass(widget_class, AdminSnippetChooser):
                svg_icon_href = 'icon-snippet'
            else:
                svg_icon_href = 'icon-placeholder'

            chooser_preview = soup.new_tag('div')
            unchosen.append(chooser_preview)
            chooser_preview['class'] = "chooser__preview"
            chooser_preview['role'] = "presentation"
            chooser_preview['style'] = "display: inline-flex; margin-right: 1.5em;"
            svg = soup.new_tag('svg')
            chooser_preview.append(svg)
            svg['aria-hidden'] = "false"
            svg['class'] = "icon"
            use = soup.new_tag('use')
            svg.append(use)
            use['href'] = f"#{svg_icon_href}"

            chooser_title = soup.new_tag('span')
            unchosen.append(chooser_title)
            chooser_title['class'] = "chooser__title"
            chooser_title['style'] = "vertical-align: 0.5em;"
            chooser_title['data-chooser-title'] = ""
            chooser_title.string = f'{_("Not Selected")}'
            return unchosen

        def _has_base_form_error(self):
            try:
                if not issubclass(self.form.__class__, RestrictedPanelsAdminPageForm):
                    raise TypeError(
                        f'{self.instance.__class__.__name__}: {_("Incorrect form type for RestrictedFieldPanel")}'
                    )
                return False
            except Exception as e:
                print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")       
                messages.error(
                    self.request, 
                    _("RestrictedFieldPanel should only be used with a base_form_class inherited from RestrictedPanelsAdminPageForm")
                )
                referer = self.request.META.get('HTTP_REFERER', '/admin/')
                if referer == self.request.build_absolute_uri():
                    referer = '/admin/'
                return referer

        @property
        def warning_label(self):
            soup = BeautifulSoup()
            warning = soup.new_tag("div")
            warning["class"] = "help restricted-field-warning"
            svg = soup.new_tag('svg')
            warning.append(svg)
            svg['class'] = "icon"
            svg['style'] = "height: 1.2em; width: 1.2em; vertical-align: -0.3em; margin-right: 0.5em;"
            use = soup.new_tag('use')
            svg.append(use)
            use['href'] = "#icon-warning"
            warning.append(f'{_("Read Only")}')
            return warning

  