from bs4 import BeautifulSoup
from core.forms import RestrictedPanelsAdminPageForm
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import InlinePanel

class RestrictedInlinePanel(InlinePanel):
    """
    
    Custom css classes:
        restricted-field-warning - formats read-only label, supplements wagtail help class
        disabled-display-field - formats disabled rich-text fields and fallback/error returns
        restricted-summary - format for collapsible inline panel display heading
    """
    def __init__(
        self,
        relation_name,
        authorised_roles=[],
        allow_on_create=False,
        allow_for_owner=False,
        hide_if_restricted=False,
        **kwargs,
    ):
        super().__init__(relation_name, **kwargs)
        self.relation_name = relation_name
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
        opts["restricted-inline-panels"] = {
            self.relation_name: {
                'authorised_roles': self.authorised_roles,
                'allow_on_create': self.allow_on_create,
                'allow_for_owner': self.allow_for_owner,
                'hide_if_restricted': self.hide_if_restricted,
            }
        }
        return opts

    class BoundPanel(InlinePanel.BoundPanel):
        template_name = "wagtailadmin/panels/inline_panel.html"

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.is_authorised = (
                self.panel.relation_name in getattr(self.form, 'authorised_panels', [])
            )
            self.base_form_error = self._has_base_form_error()
            self.render_soup = BeautifulSoup()
            self.related_instances = getattr(self.instance, self.panel.db_field.related_name, None).all()

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
            html = super().render_html(parent_context)
            # return html
            self.render_soup = BeautifulSoup(html, "html.parser")

            # strip all scripts and link buttons
            for element in self.render_soup('a', class_='button') + self.render_soup('script'): 
            # for element in self.render_soup('a', class_='button'): 
                element.extract()

            # strip all buttons except for comment buttons
            for element in self.render_soup('button'):
                if not (
                    element.has_attr('class') 
                    and 'w-field__comment-button' in element["class"]
                    ):
                    element.extract()

            input_tags = self.render_soup.find_all("input")
            # set panel count forms to 0
            if input_tags:
                for input in input_tags: 
                    if any([x in input['id'] for x in ["TOTAL_FORMS", "INITIAL_FORMS", "MIN_NUM_FORMS", "MAX_NUM_FORMS"]]):
                        input['value'] = 0
                    else:
                        input["disabled"] = ''

            if self.related_instances.count() == 0:
                self.render_empty_value()
            else:
                self.render_sub_panels()

            # add read-only warning below panels
            self.render_soup.append(self.warning_label)

            return mark_safe(self.render_soup.renderContents().decode("utf-8"))

        def render_sub_panels(self):
            # move panels into collapsed <details>, handle richtextfields
            self.render_rich_text_fields()
            display = self.render_soup.find(id=f'id_{self.panel.db_field.related_name}-FORMS')
            svg_id = f'{self.panel.db_field.related_name}-toggler'
            toggler_animation = self.render_soup.new_tag('style')
            display.insert_before(toggler_animation)
            toggler_animation.append(
                f'[open] svg#{svg_id} {{transform: rotate(0deg);}} svg#{svg_id} {{transform: rotate(-90deg);}}'
            )
            details = self.render_soup.new_tag('details')
            display.insert_after(details)
            details['style'] = 'margin-top: 1em;'
            summary = self.render_soup.new_tag('summary')
            summary['class'] = 'w-panel__heading w-panel__heading--label restricted-summary'
            details.append(summary)
            summary_heading = self.render_soup.new_tag('a')
            summary.append(summary_heading)
            svg = self.render_soup.new_tag('svg')
            summary_heading.append(svg)
            svg['class'] = 'icon icon-arrow-down-big w-panel__icon'
            svg['id'] = svg_id
            svg['aria-hidden'] = "true"
            use = self.render_soup.new_tag('use')
            svg.append(use)
            use['href'] = "#icon-arrow-down-big"
            summary_heading_text = self.render_soup.new_tag('span')
            summary_heading.append(summary_heading_text)
            summary_heading_text['style'] = "padding-left: 1em;"
            summary_heading_text.string = f'{_("Details")}'
            details.append(display.extract())

        def render_rich_text_fields(self):
            # get stored value for rtf and render this as HTML instead
            for richtextfield in self.render_soup.find_all('input', {'data-draftail-input':True}):
                name, index, remote_field = richtextfield.attrs['id'].rsplit('-',2)
                value = getattr(self.related_instances[int(index)], remote_field, '')
                rtf = self.render_soup.new_tag('div')
                rtf['class'] = "disabled-display-field"
                rtf.append(BeautifulSoup(value, 'html.parser'))
                richtextfield.insert_after(rtf)
                richtextfield.extract()

        def render_empty_value(self):
            # display placeholder icon in default chooser panel
            container = self.render_soup.find(id=f'id_{self.panel.db_field.related_name}-FORMS')
            container.clear()
            container['style'] = 'margin-top: 1em;'
            chooser_preview = self.render_soup.new_tag('div')
            container.append(chooser_preview)
            chooser_preview['class'] = "chooser__preview"
            chooser_preview['role'] = "presentation"
            chooser_preview['style'] = "display: inline-flex; margin-right: 1.5em;"
            svg = self.render_soup.new_tag('svg')
            chooser_preview.append(svg)
            svg['aria-hidden'] = "false"
            svg['class'] = "icon"
            use = self.render_soup.new_tag('use')
            svg.append(use)
            use['href'] = f"#icon-placeholder"

            chooser_title = self.render_soup.new_tag('span')
            container.append(chooser_title)
            chooser_title['class'] = "chooser__title"
            chooser_title['style'] = "vertical-align: 0.5em;"
            chooser_title['data-chooser-title'] = ""
            chooser_title.string = f'{_("Not Selected")}'

            if self.panel.min_num > 0 and not self.instance.id:
                # display warning on new page if at least 1 instance required
                error = self.render_soup.new_tag('div')
                error['class'] = 'error-message'
                span = self.render_soup.new_tag('span')
                span['style'] = 'padding-left: 0.5em;'
                span.append(f'{_("Read-only access for required field.")}')
                error.append(span)
                container.insert_after(error)

            return container

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
            warning = self.render_soup.new_tag("div")
            warning["class"] = "help restricted-field-warning"
            svg = self.render_soup.new_tag('svg')
            warning.append(svg)
            svg['class'] = "icon"
            svg['style'] = "height: 1.2em; width: 1.2em; vertical-align: -0.3em; margin-right: 0.5em;"
            use = self.render_soup.new_tag('use')
            svg.append(use)
            use['href'] = "#icon-warning"
            warning.append(f'{_("Read Only")}')
            return warning
