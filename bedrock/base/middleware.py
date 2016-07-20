"""
Taken from zamboni.amo.middleware.

This is django-localeurl, but with mozilla style capital letters in
the locale codes.
"""
import base64
import urllib
from warnings import warn

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.utils.encoding import smart_str, force_text

from . import urlresolvers
from .templatetags.helpers import urlparams
from lib.l10n_utils import translation


class LocaleURLMiddleware(object):
    """
    1. Search for the locale.
    2. Save it in the request.
    3. Strip them from the URL.
    """

    def __init__(self):
        if not settings.USE_I18N or not settings.USE_L10N:
            warn("USE_I18N or USE_L10N is False but LocaleURLMiddleware is "
                 "loaded. Consider removing bedrock.base.middleware."
                 "LocaleURLMiddleware from your MIDDLEWARE_CLASSES setting.")

        self.exempt_urls = getattr(settings, 'FF_EXEMPT_LANG_PARAM_URLS', ())

    def _is_lang_change(self, request):
        """Return True if the lang param is present and URL isn't exempt."""
        if 'lang' not in request.GET:
            return False

        return not any(request.path.endswith(url) for url in self.exempt_urls)

    def process_request(self, request):
        prefixer = urlresolvers.Prefixer(request)
        urlresolvers.set_url_prefix(prefixer)
        full_path = prefixer.fix(prefixer.shortened_path)

        if self._is_lang_change(request):
            # Blank out the locale so that we can set a new one. Remove lang
            # from the query params so we don't have an infinite loop.
            prefixer.locale = ''
            new_path = prefixer.fix(prefixer.shortened_path)
            query = dict((smart_str(k), request.GET[k]) for k in request.GET)
            query.pop('lang')
            return HttpResponsePermanentRedirect(urlparams(new_path, **query))

        if full_path != request.path:
            query_string = request.META.get('QUERY_STRING', '')
            full_path = urllib.quote(full_path.encode('utf-8'))

            if query_string:
                full_path = '?'.join(
                    [full_path, force_text(query_string, errors='ignore')])

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


class BasicAuthMiddleware(object):
    """
    Middleware to protect the entire site with a single basic-auth username and password.
    Set the BASIC_AUTH_CREDS environment variable to enable.
    """
    def __init__(self):
        if not settings.BASIC_AUTH_CREDS:
            raise MiddlewareNotUsed

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
            realm = settings.DEIS_APP or 'bedrock-demo'
            response['WWW-Authenticate'] = 'Basic realm="{}"'.format(realm)
            return response
