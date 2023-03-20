import threading

from django.utils.deprecation import MiddlewareMixin

request_local = threading.local()


def get_request():
    return getattr(request_local, 'request', None)


def get_current_user():
    request = get_request()
    return request.user


class CurrentUserMiddleware(MiddlewareMixin):

    def __call__(self, request):
        request_local.request = request
        return self.get_response(request)

    def process_exception(self, request, exception):
        request_local.request = None

    def process_template_response(self, request, response):
        request_local.request = None
        return response
