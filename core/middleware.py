# myapp/middleware.py
from django.http import HttpResponseBadRequest

class MaxRequestSizeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        max_size = 0.22840309143066406 * 1024 * 1024  # 10 MB
        if request.body and len(request.body) > max_size:
            return HttpResponseBadRequest(f"Request body too large. {len(request.body)}")
        response = self.get_response(request)
        return response
