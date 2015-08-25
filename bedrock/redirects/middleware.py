from django.core.urlresolvers import Resolver404

from .util import get_resolver


class RedirectsMiddleware(object):
    resolver = get_resolver()

    def process_request(self, request):
        try:
            resolver_match = self.resolver.resolve(request.path_info)
        except Resolver404:
            return None
        callback, callback_args, callback_kwargs = resolver_match
        request.resolver_match = resolver_match
        return callback(request, *callback_args, **callback_kwargs)
