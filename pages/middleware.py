from pages.views import view_page
from django.http import Http404
from django.conf import settings


class PageFallbackMiddleware(object):
    """
    Middleware for serving content pages. The middleware is invoked if
    if the http response code is 404 (file not found). Locating the page
    and rendering is delegated to the view_page view.

    In case no page was found or that the view had errors, the originally
    reponse is returned.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response = self.process_response(request, response)

        return response

    def process_response(self, request, response):
        if response.status_code != 404:
            return response  # No need to check for a flatpage for non-404 responses.

        try:
            response = view_page(request, request.path_info)
            return response
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
