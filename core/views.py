import os

from django.http import HttpResponse
from django.utils.http import http_date
from django.views.generic import View


class SitemapView(View):
    def get(self, request):
        sitemap_path = "sitemap.xml"
        with open(sitemap_path, "r") as file:
            content = file.read()
        last_modified = os.path.getmtime(sitemap_path)
        response = HttpResponse(
            content,
            content_type="application/xml",
            headers={
                "X-Robots-Tag": "noindex, noodp, noarchive",
                "last-modified": http_date(last_modified),
                "vary": "Accept-Encoding",
            },
        )
        return response