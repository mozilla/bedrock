# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
from collections import defaultdict
from copy import deepcopy
from urllib.parse import parse_qs, urlencode

from django.conf import settings
from django.http import (
    Http404,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.urls import NoReverseMatch, URLResolver, re_path, reverse
from django.urls.resolvers import RegexPattern
from django.utils.html import strip_tags
from django.views.decorators.vary import vary_on_headers

import commonware.log

from bedrock.mozorg.decorators import cache_control_expires

log = commonware.log.getLogger("redirects.util")
LOCALE_RE = r"^(?P<locale>\w{2,3}(?:-\w{2})?/)?"
HTTP_RE = re.compile(r"^https?://", re.IGNORECASE)
PROTOCOL_RELATIVE_RE = re.compile(r"^//+")

# redirects registry
redirectpatterns = []


def register(patterns):
    redirectpatterns.extend(patterns)


def get_resolver(patterns=None):
    patterns = patterns or redirectpatterns
    return URLResolver(RegexPattern(r"^/"), patterns)


def header_redirector(header_name, regex, match_dest, nomatch_dest, case_sensitive=False):
    flags = 0 if case_sensitive else re.IGNORECASE
    regex_obj = re.compile(regex, flags)

    def decider(request, *args, **kwargs):
        value = request.headers.get(header_name, "")
        match = regex_obj.search(value)
        if match:
            return match_dest
        else:
            return nomatch_dest

    return decider


def ua_redirector(regex, match_dest, nomatch_dest, case_sensitive=False):
    return header_redirector("user-agent", regex, match_dest, nomatch_dest, case_sensitive)


def is_firefox_redirector(fx_dest, nonfx_dext):
    include_re = re.compile(r"\bFirefox\b", flags=re.I)
    exclude_re = re.compile(r"\b(Camino|Iceweasel|SeaMonkey)\b", flags=re.I)

    def decider(request, *args, **kwargs):
        value = request.headers.get("User-Agent", "")
        if include_re.search(value) and not exclude_re.search(value):
            return fx_dest
        else:
            return nonfx_dext

    return decider


def platform_redirector(desktop_dest, android_dest, ios_dest):
    android_re = re.compile(r"\bAndroid\b", flags=re.I)
    ios_re = re.compile(r"\b(iPhone|iPad|iPod)\b", flags=re.I)

    def decider(request, *args, **kwargs):
        value = request.headers.get("User-Agent", "")
        if android_re.search(value):
            return android_dest
        elif ios_re.search(value):
            return ios_dest
        else:
            return desktop_dest

    return decider


def mobile_app_redirector(request, product, campaign):
    android_re = re.compile(r"\bAndroid\b", flags=re.I)
    value = request.headers.get("User-Agent", "")

    # Map product names to tracking product codes
    product_mapping = {
        "firefox": "firefox_mobile",
        "firefox_beta": "firefox_mobile",
        "firefox_nightly": "firefox_mobile",
        "focus": "focus",
        "klar": "klar",
        "vpn": "vpn",
    }

    tracking_product = product_mapping.get(product, "unrecognized")

    if android_re.search(value):
        base_url = getattr(settings, f"GOOGLE_PLAY_{product.upper()}_LINK")
        params = "&referrer=utm_source%3Dwww.mozilla.org%26utm_medium%3Dreferral%26utm_campaign%3D{cmp}"
    else:
        base_url = getattr(settings, f"APPLE_APPSTORE_{product.upper()}_LINK").replace("/{country}/", "/")
        params = "?pt=373246&ct={cmp}&mt=8&mz_pr={tp}"

    if campaign:
        return base_url + params.format(cmp=campaign, tp=tracking_product)
    else:
        return base_url


def no_redirect(pattern, locale_prefix=True, re_flags=None):
    """
    Return a url matcher that will stop the redirect middleware and force
    Django to continue with regular URL matching. For use when you have a URL pattern
    you want to serve, and a broad catch-all pattern you want to redirect.
    :param pattern: regex URL patter that will definitely not redirect.
    :param locale_prefix: prepend the locale matching pattern.
    :param re_flags: a string of any of the characters: "iLmsux". Will modify the `pattern` regex
        based on the documented meaning of the flags (see python re module docs).
    :return:
    """
    if locale_prefix:
        pattern = pattern.lstrip("^/")
        pattern = LOCALE_RE + pattern

    if re_flags:
        pattern = f"(?{re_flags})" + pattern

    def _view(request, *args, **kwargs):
        return None

    return re_path(pattern, _view)


def _drop_lang_code(path):
    first, slash, rest = path.lstrip("/").partition("/")
    if first in [x[0] for x in settings.LANGUAGES]:
        return slash + rest
    return path


def redirect(
    pattern,
    to,
    permanent=True,
    locale_prefix=True,
    anchor=None,
    name=None,
    query=None,
    vary=None,
    cache_timeout=12,
    decorators=None,
    re_flags=None,
    to_args=None,
    to_kwargs=None,
    prepend_locale=True,
    merge_query=False,
):
    """
    Return a url matcher suited for urlpatterns.

    pattern: the regex against which to match the requested URL.
    to: either a url name that `reverse` will find, a url that will simply be returned,
        or a function that will be given the request and url captures, and return the
        destination.
    permanent: boolean whether to send a 301 or 302 response.
    locale_prefix: automatically prepend `pattern` with a regex for an optional locale
        in the url. This locale (or None) will show up in captured kwargs as 'locale'.
    anchor: if set it will be appended to the destination url after a '#'.
    name: if used in a `urls.py` the redirect URL will be available as the name
        for use in calls to `reverse()`. Does _NOT_ work if used in a `redirects.py` file.
    query: a dict of query params to add to the destination url.
    vary: if you used an HTTP header to decide where to send users you should include that
        header's name in the `vary` arg.
    cache_timeout: number of hours to cache this redirect. just sets the proper `cache-control`
        and `expires` headers.
    decorators: a callable (or list of callables) that will wrap the view used to redirect
        the user. equivalent to adding a decorator to any other view.
    re_flags: a string of any of the characters: "iLmsux". Will modify the `pattern` regex
        based on the documented meaning of the flags (see python re module docs).
    to_args: a tuple or list of args to pass to reverse if `to` is a url name.
    to_kwargs: a dict of keyword args to pass to reverse if `to` is a url name.
    prepend_locale: if true the redirect URL will be prepended with the locale from the
        requested URL.
    merge_query: merge the requested query params from the `query` arg with any query params
        from the request.

    Usage:
    urlpatterns = [
        redirect(r'projects/$', 'mozorg.product'),
        redirect(r'^projects/seamonkey$', 'mozorg.product', locale_prefix=False),
        redirect(r'apps/$', 'https://marketplace.firefox.com'),
        redirect(r'firefox/$', settings.FXC_BASE_URL, name='firefox'),  # note that redirect_source querystring is not added by default
        redirect(r'the/dude$', 'abides', query={'aggression': 'not_stand'}),
    ]
    """
    if permanent:
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect

    if locale_prefix:
        pattern = pattern.lstrip("^/")
        pattern = LOCALE_RE + pattern

    if re_flags:
        pattern = f"(?{re_flags})" + pattern

    view_decorators = []
    if cache_timeout is not None:
        view_decorators.append(cache_control_expires(cache_timeout))

    if vary:
        if isinstance(vary, str):
            vary = [vary]
        view_decorators.append(vary_on_headers(*vary))

    if decorators:
        if callable(decorators):
            view_decorators.append(decorators)
        else:
            view_decorators.extend(decorators)

    if query:
        # prevent updating in place
        query = query.copy()

    def _view(request, *args, **kwargs):
        # Avoid the _view closure capturing the original _query state
        request_query = deepcopy(query)

        # don't want to have 'None' in substitutions
        kwargs = {k: v or "" for k, v in kwargs.items()}
        args = [x or "" for x in args]

        # If it's a callable, call it and get the url out.
        if callable(to):
            to_value = to(request, *args, **kwargs)
        else:
            to_value = to

        if to_value.startswith("/") or HTTP_RE.match(to_value):
            redirect_url = to_value
        else:
            try:
                redirect_url = reverse(to_value, args=to_args, kwargs=to_kwargs)
                # reverse() will give us, by default, a redirection
                # with settings.LANGUAGE_CODE as the prefixed language.
                # We don't want this by default, only if explicitly requested
                redirect_url = _drop_lang_code(redirect_url)
            except NoReverseMatch:
                # Assume it's a URL
                redirect_url = to_value

        if prepend_locale and redirect_url.startswith("/") and kwargs.get("locale"):
            redirect_url = "/{locale}" + redirect_url.lstrip("/")
        elif prepend_locale and "{_locale}" in redirect_url:
            # So this is a full domain / offsite redirect, not a relative one.
            # But do we have a locale already known to us? If so, use it, to avoid
            # a 302 on the destination when the locale is re-detected
            #
            # Note that we're using a variable called _locale in the URL template
            # to deliberately avoid clashing with `locale` in the current variable
            # space.
            if kwargs.get("locale"):  # extracted as, say, "fr/"
                _locale = kwargs.get("locale").rstrip("/")
                redirect_url = redirect_url.format(_locale=_locale)
            else:
                # If we don't yet have a locale to use in the redirect, we have to
                # just live without it
                redirect_url = redirect_url.replace("/{_locale}", "")

        # use info from url captures.
        if args or kwargs:
            if args:
                redirect_url = redirect_url.format(*args)
            if kwargs:
                # Use `defaultdict` to default to empty string for missing kwargs.
                redirect_url = redirect_url.format_map(defaultdict(str, kwargs))
            redirect_url = strip_tags(redirect_url)

        if request_query:
            if merge_query:
                _req_qs_query = parse_qs(request.META.get("QUERY_STRING", ""))
                request_query.update(_req_qs_query)

            querystring = urlencode(request_query, doseq=True)
        elif request_query is None:
            querystring = request.META.get("QUERY_STRING", "")
        else:
            querystring = ""

        if querystring:
            redirect_url = "?".join([redirect_url, querystring])

        if anchor:
            redirect_url = "#".join([redirect_url, anchor])

        if PROTOCOL_RELATIVE_RE.match(redirect_url):
            redirect_url = "/" + redirect_url.lstrip("/")

        return redirect_class(redirect_url)

    # Apply decorators
    try:
        # Decorators should be applied in reverse order so that input
        # can be sent in the order your would write nested decorators
        # e.g. dec1(dec2(_view)) -> [dec1, dec2]
        for decorator in reversed(view_decorators):
            _view = decorator(_view)
    except TypeError:
        log.exception("decorators not iterable or does not contain callable items")

    return re_path(pattern, _view, name=name)


def gone_view(request, *args, **kwargs):
    from bedrock.base.views import page_gone_view

    return page_gone_view(request)


def gone(pattern):
    """Return a url matcher suitable for urlpatterns that returns a 410."""
    return re_path(pattern, gone_view)


def not_found_view(request, *args, **kwargs):
    raise Http404()


def not_found(pattern):
    """Return a url matcher suitable for urlpatterns that raises a 404."""
    return re_path(pattern, not_found_view)
