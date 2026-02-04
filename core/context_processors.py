from wagtail.models import Site

def current_site(request):
    return {
        "current_site": Site.find_for_request(request)
    }