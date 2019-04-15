from builtins import object
from threading import local

from django.conf import settings
from django.urls import reverse as django_reverse
from django.utils.encoding import iri_to_uri
from django.utils.functional import lazy
from django.utils.translation.trans_real import parse_accept_lang_header


# Thread-local storage for URL prefixes. Access with (get|set)_url_prefix.
_local = local()


def set_url_prefix(prefix):
    """Set the ``prefix`` for the current thread."""
    _local.prefix = prefix


def get_url_prefix():
    """Get the prefix for the current thread, or None."""
    return getattr(_local, 'prefix', None)


def reverse(viewname, urlconf=None, args=None, kwargs=None, prefix=None):
    """Wraps Django's reverse to prepend the correct locale."""
    prefixer = get_url_prefix()

    if prefixer:
        prefix = prefix or '/'
    url = django_reverse(viewname, urlconf, args, kwargs, prefix)
    if prefixer:
        url = prefixer.fix(url)

    # Ensure any unicode characters in the URL are escaped.
    return iri_to_uri(url)


reverse_lazy = lazy(reverse, str)


def _get_language_map():
    """
    Return a complete dict of language -> URL mappings, including the canonical
    short locale maps (e.g. es -> es-ES and en -> en-US).
    :return: dict
    """
    LUM = settings.LANGUAGE_URL_MAP
    langs = dict(list(LUM.items()) + list(settings.CANONICAL_LOCALES.items()))
    # Add missing short locales to the list. This will automatically map
    # en to en-GB (not en-US), es to es-AR (not es-ES), etc. in alphabetical
    # order. To override this behavior, explicitly define a preferred locale
    # map with the CANONICAL_LOCALES setting.
    langs.update((k.split('-')[0], v) for k, v in list(LUM.items()) if
                 k.split('-')[0] not in langs)
    return langs


# lazy for easier testing mostly
FULL_LANGUAGE_MAP = lazy(_get_language_map, dict)()


def find_supported(lang):
    lang = lang.lower()
    if lang in FULL_LANGUAGE_MAP:
        return FULL_LANGUAGE_MAP[lang]
    pre = lang.split('-')[0]
    if pre in FULL_LANGUAGE_MAP:
        return FULL_LANGUAGE_MAP[pre]


def split_path(path_):
    """
    Split the requested path into (locale, path).

    locale will be empty if it isn't found.
    """
    path = path_.lstrip('/')

    # Use partition instead of split since it always returns 3 parts
    first, _, rest = path.partition('/')

    supported = find_supported(first)
    if supported:
        return supported, rest
    else:
        return '', path


class Prefixer(object):
    def __init__(self, request):
        self.request = request
        split = split_path(request.path_info)
        self.locale, self.shortened_path = split

    def get_language(self):
        """
        Return a locale code we support on the site using the
        user's Accept-Language header to determine which is best. This
        mostly follows the RFCs but read bug 439568 for details.
        """
        accept_lang = self.request.META.get('HTTP_ACCEPT_LANGUAGE')
        if accept_lang:
            best = self.get_best_language(accept_lang)
            if best:
                return best

        return settings.LANGUAGE_CODE

    def get_best_language(self, accept_lang):
        """Given an Accept-Language header, return the best-matching language."""
        ranked = parse_accept_lang_header(accept_lang)
        for lang, _ in ranked:
            supported = find_supported(lang)
            if supported:
                return supported

    def fix(self, path):
        path = path.lstrip('/')
        url_parts = [self.request.META['SCRIPT_NAME']]

        if path.partition('/')[0] not in settings.SUPPORTED_NONLOCALES:
            locale = self.locale if self.locale else self.get_language()
            url_parts.append(locale)

        url_parts.append(path)

        return '/'.join(url_parts)
