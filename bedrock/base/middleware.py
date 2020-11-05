"""
Taken from zamboni.amo.middleware.

This is django-localeurl, but with mozilla style capital letters in
the locale codes.
"""
import base64
import urllib.parse
from urllib.parse import unquote
from warnings import warn

from commonware.middleware import FrameOptionsHeader as OldFrameOptionsHeader
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin

from lib.l10n_utils import translation

from . import urlresolvers


class LocaleURLMiddleware:
    """
    1. Search for the locale.
    2. Save it in the request.
    3. Strip them from the URL.
    """

    def __init__(self, get_response=None):
        if not settings.USE_I18N or not settings.USE_L10N:
            warn("USE_I18N or USE_L10N is False but LocaleURLMiddleware is "
                 "loaded. Consider removing bedrock.base.middleware."
                 "LocaleURLMiddleware from your MIDDLEWARE setting.")
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)

    def process_request(self, request):
        prefixer = urlresolvers.Prefixer(request)
        urlresolvers.set_url_prefix(prefixer)
        full_path = prefixer.fix(prefixer.shortened_path)

        if not (request.path in settings.SUPPORTED_LOCALE_IGNORE or full_path == request.path):
            query_string = request.META.get('QUERY_STRING', '')
            full_path = urllib.parse.quote(full_path.encode('utf-8'))

            if query_string:
                full_path = '?'.join(
                    [full_path, unquote(query_string, errors='ignore')])

            response = HttpResponsePermanentRedirect(full_path)

            # Vary on Accept-Language if we changed the locale
            old_locale = prefixer.locale
            new_locale, _ = urlresolvers.split_path(full_path)
            if old_locale != new_locale:
                response['Vary'] = 'Accept-Language'

            return response

        request.path_info = '/' + prefixer.shortened_path
        request.locale = prefixer.locale
        translation.activate(prefixer.locale or settings.LANGUAGE_CODE)


class BasicAuthMiddleware:
    """
    Middleware to protect the entire site with a single basic-auth username and password.
    Set the BASIC_AUTH_CREDS environment variable to enable.
    """
    def __init__(self, get_response=None):
        if not settings.BASIC_AUTH_CREDS:
            raise MiddlewareNotUsed
        self.get_response = None

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)

    def process_request(self, request):
        required_auth = settings.BASIC_AUTH_CREDS
        if required_auth:
            if 'HTTP_AUTHORIZATION' in request.META:
                auth = request.META['HTTP_AUTHORIZATION'].split()
                if len(auth) == 2:
                    if auth[0].lower() == "basic":
                        provided_auth = base64.b64decode(auth[1])
                        if provided_auth == required_auth:
                            # we're good. continue on.
                            return None

            response = HttpResponse(status=401,
                                    content='<h1>Unauthorized. '
                                            'This site is in private demo mode.</h1>')
            realm = settings.APP_NAME or 'bedrock-demo'
            response['WWW-Authenticate'] = 'Basic realm="{}"'.format(realm)
            return response


class FrameOptionsHeader(OldFrameOptionsHeader, MiddlewareMixin):
    pass
