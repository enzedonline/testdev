from bs4 import BeautifulSoup
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.admin.rich_text.editors.draftail import DraftailRichTextArea
from wagtail.blocks.base import BlockField
from wagtail.blocks.stream_block import StreamBlock

from ..forms.restricted_panels_admin_forms import RestrictedPanelsAdminFormMixin


class msg:
    """
    Translatable strings for restricted panels
    """

    BASE_FORM_ERROR = _("Base Form Error")
    BASE_FORM_ERROR_VERBOSE = _(
        "Restricted panels need to use a base_form_class inherited from RestrictedPanelsAdminFormMixin"
    )
    DETAILS = _("Details")
    EMPTY_STREAMFIELD = _("Empty Streamfield")
    INCORRECT_FORM_TYPE = _("Incorrect form type")
    NOT_SELECTED = _("Not Selected")
    READ_ONLY = _("Read Only")
    REQUIRED_FIELD = _("Read-only access for required field.")
    RESTRICTED_FIELD = _("Restricted Field")
    RESTRICTED_TO = _("Restricted to")
    STREAMFIELD_CONTENTS = _("StreamField Contents")

class RestrictedBoundPanelMixin:
    # Common code for Restricted Panel BoundPanels
    def render_empty_chooser(self, chooser):
        unchosen = chooser.find("div", class_="unchosen")
        if unchosen:
            svg_icon_href = None
            if "image-chooser" in chooser["class"]:
                svg_icon_href = "icon-image"
            elif "document-chooser" in chooser["class"]:
                svg_icon_href = "icon-doc-full-inverse"
            elif "page-chooser" in chooser["class"]:
                svg_icon_href = "icon-doc-empty-inverse"
            elif "snippet-chooser" in chooser["class"]:
                svg_icon_href = "icon-snippet"
            else:
                svg_icon_href = "icon-placeholder"

            unchosen.clear()
            chooser_preview = self.render_soup.new_tag("div")
            unchosen.append(chooser_preview)
            chooser_preview["class"] = "chooser__preview"
            chooser_preview["role"] = "presentation"
            chooser_preview["style"] = "display: inline-flex; margin-right: 1.5em;"
            svg = self.render_soup.new_tag("svg")
            chooser_preview.append(svg)
            svg["aria-hidden"] = "false"
            svg["class"] = "icon"
            use = self.render_soup.new_tag("use")
            svg.append(use)
            use["href"] = f"#{svg_icon_href}"

            chooser_title = self.render_soup.new_tag("span")
            unchosen.append(chooser_title)
            chooser_title["class"] = "chooser__title"
            chooser_title["style"] = "vertical-align: 0.5em;"
            chooser_title["data-chooser-title"] = ""
            chooser_title.string = f"{msg.NOT_SELECTED}"

    def _has_base_form_error(self):
        try:
            if not issubclass(self.form.__class__, RestrictedPanelsAdminFormMixin):
                raise TypeError(
                    f"{self.instance.__class__.__name__}: {self.form.__class__.__name__} - {msg.INCORRECT_FORM_TYPE}"
                )
            return False
        except Exception as e:
            print(
                f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
            )
            messages.error(
                self.request, f"{self.field_name}: {msg.BASE_FORM_ERROR_VERBOSE}"
            )
            referer = self.request.META.get("HTTP_REFERER", "/admin/")
            if referer == self.request.build_absolute_uri():
                referer = "/admin/"
            return referer

    @property
    def warning_label(self):
        warning = self.render_soup.new_tag("div")
        warning["class"] = "help readonly-field-warning"
        svg = self.render_soup.new_tag("svg")
        warning.append(svg)
        svg["class"] = "icon"
        svg["style"] = "height: 1.2em; width: 1.2em; vertical-align: -0.3em; margin-right: 0.5em;"
        use = self.render_soup.new_tag("use")
        svg.append(use)
        use["href"] = "#icon-warning"
        warning.append(f"{msg.READ_ONLY}")
        return warning

class RestrictedFieldPanel(FieldPanel):
    """
    Panel to restrict editing fields based on logged in user's role membership (see also RestrictedInlinePanel)
    IMPORTANT: Must be used with base_form_class that inherits RestrictedPanelsAdminFormMixin
      - See RestrictedPanelsAdminFormMixin for additional notes.
    Adds the following kwargs to field panel to determine if panel should be editable, read-only or hidden
        authorised_roles=[] - list of roles to pass on to form to determine if authorised to edit.
                            - superusers and roles listed in RESTRICTED_PANEL_OVERRIDE_ROLES will always be authorised.
        allow_on_create=False - if true, for a restricted user, panel will be editable on a new page/model only 
        allow_for_owner=False - if true, for a restricted user, panel will be editable pages/models owned (created by default) by that user 
        hide_if_restricted=False - if true, panel will not be present on form for restricted users
    StreamFields and RichTextFields will be rendered as is if restricted. Admin CSS rules may differ to front end
      causing the read-only display to differ from that displayed on website.
    Custom css classes (see example hook at base of this file):
        readonly-field-warning - formats read-only label, supplements wagtail help class
        restricted-summary - format for collapsible streamfield display heading
        restricted-summary-arrow - format for collapsed streamfield summary arrow (use to animate direction)
        readonly-display-field - formats disabled rich-text fields, streamfields and fallback/error returns
                               - inline css is added to handle lists in these fields
    For multi-lingual sites:
      - Either use gettext_lazy or custom translation model
      - Panel affects source page/model only, translation pages must be handled seperately
      - Editor language preference can be found in self.for_user.wagtail_userprofile.get_preferred_language()
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
                "authorised_roles": self.authorised_roles,
                "allow_on_create": self.allow_on_create,
                "allow_for_owner": self.allow_for_owner,
                "hide_if_restricted": self.hide_if_restricted,
            }
        }
        return opts

    class BoundPanel(RestrictedBoundPanelMixin, FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.is_authorised = getattr(self, "field_name", None) in getattr(
                self.form, "authorised_panels", []
            )
            self.base_form_error = self._has_base_form_error()
            self.render_soup = BeautifulSoup()

        def render_html(self, parent_context=None):
            if self.base_form_error:
                return mark_safe(
                    f'<p class="readonly-display-field">{msg.BASE_FORM_ERROR}</p>'
                )
            else:
                return (
                    super().render_html(parent_context)
                    if self.is_authorised
                    else self.disable_input(parent_context)
                )

        def disable_input(self, parent_context):
            # default render, set input element to readonly, add warning sub-label
            # 'radio', 'checkbox' & 'file' input types will be set to disabled
            # not called if hide_if_restricted=True and no default error
            field = object
            if self.field_name in self.form.fields.keys():
                field = self.form.fields[self.field_name]
            widget = getattr(field, "widget", None)

            try:
                if issubclass(field.__class__, BlockField) and issubclass(
                    field.block.__class__, StreamBlock
                ):  # streamfield - render HTML and wrap in collapsed <display>
                    return self.render_streamfield()

                # RichTextField just render contents as html
                if issubclass(widget.__class__, DraftailRichTextArea):
                    return self.render_richtextfield()

                # Render html and button elements
                html = super().render_html(parent_context)
                self.render_soup = BeautifulSoup(html, "html.parser")

                # strip all scripts and link buttons
                for element in self.render_soup("a", class_="button") + self.render_soup("script"):
                    element.extract()

                # strip all buttons except for comment buttons
                for element in self.render_soup("button"):
                    if not (
                        element.has_attr("class")
                        and "w-field__comment-button" in element["class"]
                    ):
                        element.extract()

                # add default display for empty choosers
                if not getattr(self.form.instance, self.field_name, False):
                    chooser = self.render_soup.find("div", class_="chooser")
                    if chooser: self.render_empty_chooser(chooser)

                # look for input, textarea or select field
                inputs = self.render_soup(["input", "textarea", "select"])
                for element in inputs:
                    # Add hover title and warning label, force input to disabled (in case field=None)
                    if self.panel.authorised_roles:
                        element["title"] = f'{msg.RESTRICTED_TO} {", ".join(self.panel.authorised_roles)}'
                    if element.has_attr('type') and element['type'] in ['radio', 'checkbox', 'file']:
                        element["disabled"] = ""
                    else:
                        element["readonly"] = ""
                    element["class"] = element.get('class', []) + ['readonly-display-field']
                self.render_soup.append(self.warning_label)
                return mark_safe(self.render_soup.renderContents().decode("utf-8"))

            except Exception as e:
                print(
                    f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
                )

            # fallback in case of error or widget/field type not handled above
            return mark_safe(
                f'<p class="readonly-display-field">{msg.RESTRICTED_FIELD}</p>{str(self.warning_label)}'
            )

        def render_richtextfield(self):
            # RichTextField - CharField with DraftailRichTextArea widget
            # Return instance value (plain HTML)
            rtf = self.render_soup.new_tag("div")
            self.render_soup.append(rtf)
            rtf["class"] = "readonly-display-field"
            rtf.append(
                BeautifulSoup(
                    getattr(self.form.instance, self.field_name, {msg.RESTRICTED_FIELD}),
                    "html.parser"
                )
            )
            self.render_soup.append(self.warning_label)
            return mark_safe(self.render_soup.renderContents().decode("utf-8"))

        def render_streamfield(self):
            # Return rendered streamfield in collapsed <details> tag if streamfield has value
            # Add input field field_name-count with value=0
            # field validation uses this pre-clean - because we don't return anything, count needs to be 0

            streamfield = self.render_soup.new_tag("div")
            streamfield_value = getattr(self.form.instance, self.field_name, None)
            contents_container = self.render_soup.new_tag("div")
            contents_container["class"] = "readonly-display-field"
            contents_container["style"] = "margin-top: 1em;"

            if streamfield_value:
                streamfield_contents = BeautifulSoup(
                    streamfield_value.render_as_block(), "html.parser"
                )
                details = self.render_soup.new_tag("details")
                streamfield.append(details)
                summary = self.render_soup.new_tag("summary")
                details.append(summary)
                summary_heading = self.render_soup.new_tag("h2")
                summary_heading["class"] = "w-panel__heading w-panel__heading--label restricted-summary"
                summary.append(summary_heading)
                svg = self.render_soup.new_tag("svg")
                summary_heading.append(svg)
                svg["class"] = "icon w-panel__icon restricted-summary-arrow"
                use = self.render_soup.new_tag("use")
                svg.append(use)
                use["href"] = "#icon-arrow-down-big"
                summary_heading_text = self.render_soup.new_tag("span")
                summary_heading.append(summary_heading_text)
                summary_heading_text["style"] = "padding-left: 1em;"
                summary_heading_text.string = f"{msg.STREAMFIELD_CONTENTS}"
                details.append(contents_container)
            else:
                streamfield_contents = self.render_soup.new_tag("p")
                streamfield_contents.string = f"{msg.EMPTY_STREAMFIELD}"
                streamfield.append(contents_container)

            contents_container.append(streamfield_contents)
            input_field = self.render_soup.new_tag("input")
            streamfield.append(input_field)
            input_field["type"] = "hidden"
            input_field["name"] = f"{self.field_name}-count"
            input_field["data-streamfield-stream-count"] = ""
            input_field["value"] = "0"
            streamfield.append(self.warning_label)
            return mark_safe(streamfield.renderContents().decode("utf-8"))


class RestrictedInlinePanel(InlinePanel):
    """
    Panel to restrict editing inline models based on logged in user's role membership (see also RestrictedFieldPanel)
    IMPORTANT: Must be used with base_form_class that inherits RestrictedPanelsAdminFormMixin
      - See RestrictedPanelsAdminFormMixin for additional notes.
    Adds the following kwargs to field panel to determine if panel should be editable, read-only or hidden
        authorised_roles=[] - list of roles to pass on to form to determine if authorised to edit.
                            - superusers and roles listed in RESTRICTED_PANEL_OVERRIDE_ROLES will always be authorised.
        allow_on_create=False - if true, for a restricted user, panel will be editable on a new page/model only 
        allow_for_owner=False - if true, for a restricted user, panel will be editable pages/models owned (created by default) by that user 
        hide_if_restricted=False - if true, panel will not be present on form for restricted users
    RichTextFields will be rendered as is if panel is restricted. Admin CSS rules may differ to front end
      causing the read-only display to differ from that displayed on website.
    Custom css classes (see example hook at base of this file):
        readonly-field-warning - formats read-only label, supplements wagtail help class
        restricted-summary - format for collapsible streamfield display heading
        restricted-summary-arrow - format for collapsed summary arrow (use to animate direction)
        readonly-display-field - formats disabled rich-text fields, streamfields and fallback/error returns
                               - inline css is added to handle lists in these fields
    For multi-lingual sites:
      - Either use gettext_lazy or custom translation model
      - Panel affects source page/model only, translation pages must be handled seperately
      - Editor language preference can be found in self.for_user.wagtail_userprofile.get_preferred_language()
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
                "authorised_roles": self.authorised_roles,
                "allow_on_create": self.allow_on_create,
                "allow_for_owner": self.allow_for_owner,
                "hide_if_restricted": self.hide_if_restricted,
            }
        }
        return opts

    class BoundPanel(RestrictedBoundPanelMixin, InlinePanel.BoundPanel):
        template_name = "wagtailadmin/panels/inline_panel.html"

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.is_authorised = self.panel.relation_name in getattr(
                self.form, "authorised_panels", []
            )
            self.base_form_error = self._has_base_form_error()
            self.render_soup = BeautifulSoup()
            self.related_instances = getattr(
                self.instance, self.panel.db_field.related_name, None
            ).all()

        def render_html(self, parent_context=None):
            if self.base_form_error:
                return mark_safe(
                    f'<p class="readonly-display-field">{msg.BASE_FORM_ERROR}</p>'
                )
            else:
                return (
                    super().render_html(parent_context)
                    if self.is_authorised
                    else self.disable_input(parent_context)
                )

        def disable_input(self, parent_context):
            # default render, set input elements to readonly, add warning sub-label
            # 'radio', 'checkbox' & 'file' input types will be set to disabled
            # simple "Restricted Field" displayed if hide_if_restricted=True
            try:
                if self.panel.hide_if_restricted:
                    # TODO: find a way to prevent section from loading
                    return self.render_restricted_message()

                html = super().render_html(parent_context)
                self.render_soup = BeautifulSoup(html, "html.parser")

                # strip all scripts and link buttons
                for element in self.render_soup("a", class_="button") + self.render_soup("script"):
                    element.extract()

                # strip all buttons except for comment buttons
                for element in self.render_soup("button"):
                    if not (
                        element.has_attr("class")
                        and "w-field__comment-button" in element["class"]
                    ):
                        element.extract()

                inputs = self.render_soup.find_all(["input", "textarea", "select"])              
                for element in inputs:
                    if any(
                        [
                            x in element["id"]
                            for x in ["TOTAL_FORMS", "INITIAL_FORMS", "MIN_NUM_FORMS", "MAX_NUM_FORMS"]
                        ]
                    ):  # set panel count forms to 0
                        element["value"] = 0
                    else:
                        if element.has_attr('type') and element['type'] in ['radio', 'checkbox', 'file']:
                            element["disabled"] = ""
                        else:
                            element["readonly"] = ""
                        element["class"] = element.get('class', []) + ['readonly-display-field']

                if self.related_instances.count() == 0:
                    self.render_empty_value()
                else:
                    self.render_sub_panels()

                # add read-only warning below panels
                self.render_soup.append(self.warning_label)

                return mark_safe(self.render_soup.renderContents().decode("utf-8"))
            except Exception as e:
                print(
                    f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
                )

            # fallback in case of error or widget/field type not handled above
            return self.render_restricted_message()

        def render_restricted_message(self):
            return mark_safe(
                f'<p class="readonly-display-field">{msg.RESTRICTED_FIELD}</p>{str(self.warning_label)}'
            )

        def render_sub_panels(self):
            # move panels into collapsed <details>, handle richtextfields
            self.render_rich_text_fields()
            self.render_empty_choosers()
            display = self.render_soup.find(
                id=f"id_{self.panel.db_field.related_name}-FORMS"
            )
            details = self.render_soup.new_tag("details")
            display.insert_after(details)
            details["style"] = "margin-top: 1em;"
            summary = self.render_soup.new_tag("summary")
            details.append(summary)
            summary_heading = self.render_soup.new_tag("h2")
            summary_heading["class"] = "w-panel__heading w-panel__heading--label restricted-summary"
            summary.append(summary_heading)
            svg = self.render_soup.new_tag("svg")
            summary_heading.append(svg)
            svg["class"] = "icon w-panel__icon restricted-summary-arrow"
            svg["aria-hidden"] = "true"
            use = self.render_soup.new_tag("use")
            svg.append(use)
            use["href"] = "#icon-arrow-down-big"
            summary_heading_text = self.render_soup.new_tag("span")
            summary_heading.append(summary_heading_text)
            summary_heading_text["style"] = "padding-left: 1em;"
            summary_heading_text.string = f"{msg.DETAILS}"
            details.append(display.extract())

        def render_rich_text_fields(self):
            # get stored value for rtf and render this as HTML instead
            richtextfields = self.render_soup.find_all(
                "input", {"data-draftail-input": True}
            )
            if richtextfields:
                for richtextfield in richtextfields:
                    name, index, remote_field = richtextfield.attrs["id"].rsplit("-", 2)
                    value = getattr(
                        self.related_instances[int(index)], remote_field, ""
                    )
                    rtf = self.render_soup.new_tag("div")
                    rtf["class"] = "readonly-display-field"
                    rtf.append(BeautifulSoup(value, "html.parser"))
                    richtextfield.insert_after(rtf)
                    richtextfield.extract()

        def render_empty_value(self):
            # display placeholder icon in default chooser panel
            container = self.render_soup.find(
                id=f"id_{self.panel.db_field.related_name}-FORMS"
            )
            container.clear()
            container["style"] = "margin-top: 1em;"
            chooser_preview = self.render_soup.new_tag("div")
            container.append(chooser_preview)
            chooser_preview["class"] = "chooser__preview"
            chooser_preview["role"] = "presentation"
            chooser_preview["style"] = "display: inline-flex; margin-right: 1.5em;"
            svg = self.render_soup.new_tag("svg")
            chooser_preview.append(svg)
            svg["aria-hidden"] = "false"
            svg["class"] = "icon"
            use = self.render_soup.new_tag("use")
            svg.append(use)
            use["href"] = f"#icon-placeholder"

            chooser_title = self.render_soup.new_tag("span")
            container.append(chooser_title)
            chooser_title["class"] = "chooser__title"
            chooser_title["style"] = "vertical-align: 0.5em;"
            chooser_title["data-chooser-title"] = ""
            chooser_title.string = f"{msg.NOT_SELECTED}"

            if self.panel.min_num > 0 and not self.instance.id:
                # display warning on new page if at least 1 instance required
                error = self.render_soup.new_tag("div")
                error["class"] = "error-message"
                span = self.render_soup.new_tag("span")
                span["style"] = "padding-left: 0.5em;"
                span.append(f"{msg.REQUIRED_FIELD}")
                error.append(span)
                container.insert_after(error)

            return container

        def render_empty_choosers(self):
            choosers = self.render_soup.find_all("div", class_="chooser")
            for chooser in choosers:
                self.render_empty_chooser(chooser)


@hooks.register('insert_global_admin_css')
def restricted_panel_admin_css():
    style = ("""
    <style>
        .readonly-field-warning {
          color: red;
          margin-top: 1em;
        }
        .readonly-display-field {
          appearance: none;
          border: 1px solid var(--w-color-grey-100);
          border-radius: 0.3125rem;
          color: var(--w-color-grey-600) !important;
          font-size: 1.125rem;
          font-weight: 400;
          line-height: 1.5;
          padding: 0.375rem 1.25rem;
          width: 100%;
          background-color: var(--w-color-grey-50) !important;
          color: var(--w-color-grey-400);
          cursor: not-allowed !important;
          background-image: none !important;
        }
        select.readonly-display-field {
          width: unset;
        }
        textarea.readonly-display-field {
          overflow: auto;
          overflow-wrap: break-word;
          resize: vertical;
          height: 10em;
        }
        .readonly-display-field ol {
          padding: 0 0 0 40px !important;
        }
        .readonly-display-field ol li {
          list-style-type: decimal !important;
        }
        .readonly-display-field ul {
          padding: 0 0 0 40px !important; margin: 1em 0 !important;
        }
        .readonly-display-field ul li {
          list-style-type: disc !important;
        }
        select[readonly].readonly-display-field option, select[readonly].readonly-display-field optgroup {
          display: none;
        }
        .restricted-summary {
          font-weight: 600;
        }
        [open] .restricted-summary-arrow {
          transform: rotate(0deg);
        }
        .restricted-summary-arrow {
          transform: rotate(-90deg);
        }
    </style>
    """)
    return mark_safe(style)