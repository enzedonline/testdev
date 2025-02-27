import django_filters
from django.contrib.auth import get_user_model
from wagtail.admin.auth import permission_denied
from wagtail.admin.filters import DateRangePickerWidget, WagtailFilterSet
from wagtail.admin.views.reports import PageReportView
from wagtail.models import Page


def get_users_for_filter():
    User = get_user_model()
    return (
        User.objects.filter(locked_pages__isnull=False)
        .order_by(User.USERNAME_FIELD)
        .distinct()
    )

class UnpublishedChangesPagesReportFilterSet(WagtailFilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    last_published_at = django_filters.DateFromToRangeFilter(widget=DateRangePickerWidget)
    author = django_filters.ModelChoiceFilter(
        field_name="owner", queryset=lambda request: get_users_for_filter()
    )
    class Meta:
        model = Page
        fields = ["title", "author", "last_published_at", "live"]

class UnpublishedChangesReportView(PageReportView):
    index_url_name = "unpublished_changes_report"
    index_results_url_name = "unpublished_changes_report_results"
    header_icon = 'doc-empty-inverse'
    results_template_name = 'reports/unpublished_changes_report_results.html'
    page_title = "Pages with unpublished changes"

    list_export = PageReportView.list_export + ['owner', 'last_published_at']
    export_headings = dict(last_published_at='Last Published', owner='Author', **PageReportView.export_headings)
    filterset_class = UnpublishedChangesPagesReportFilterSet

    def get_queryset(self):
        return Page.objects.filter(has_unpublished_changes=True)

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return permission_denied(request)
        return super().dispatch(request, *args, **kwargs)