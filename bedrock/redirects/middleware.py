from django.urls import Resolver404

from .util import get_resolver


class RedirectsMiddleware:
    def __init__(self, get_response=None, resolver=None):
        self.get_response = get_response
        self.resolver = resolver or get_resolver()

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)

    def process_request(self, request):
        try:
            resolver_match = self.resolver.resolve(request.path_info)
        except Resolver404:
            return None
        callback, callback_args, callback_kwargs = resolver_match
        request.resolver_match = resolver_match
        return callback(request, *callback_args, **callback_kwargs)
