from threading import local

from django.conf import settings
from django.core.urlresolvers import reverse as django_reverse
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


def find_supported(test):
    return [settings.LANGUAGE_URL_MAP[x] for
            x in settings.LANGUAGE_URL_MAP if
            x.split('-', 1)[0] == test.lower().split('-', 1)[0]]


def split_path(path_):
    """
    Split the requested path into (locale, path).

    locale will be empty if it isn't found.
    """
    path = path_.lstrip('/')

    # Use partitition instead of split since it always returns 3 parts
    first, _, rest = path.partition('/')

    lang = first.lower()
    if lang in settings.LANGUAGE_URL_MAP:
        return settings.LANGUAGE_URL_MAP[lang], rest
    else:
        supported = find_supported(first)
        if len(supported):
            return supported[0], rest
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
        if 'lang' in self.request.GET:
            lang = self.request.GET['lang'].lower()
            if lang in settings.LANGUAGE_URL_MAP:
                return settings.LANGUAGE_URL_MAP[lang]

        if self.request.META.get('HTTP_ACCEPT_LANGUAGE'):
            best = self.get_best_language(
                self.request.META['HTTP_ACCEPT_LANGUAGE'])
            if best:
                return best
        return settings.LANGUAGE_CODE

    def get_best_language(self, accept_lang):
        """Given an Accept-Language header, return the best-matching language."""
        LUM = settings.LANGUAGE_URL_MAP
        langs = dict(LUM.items() + settings.CANONICAL_LOCALES.items())
        # Add missing short locales to the list. This will automatically map
        # en to en-GB (not en-US), es to es-AR (not es-ES), etc. in alphabetical
        # order. To override this behavior, explicitly define a preferred locale
        # map with the CANONICAL_LOCALES setting.
        langs.update((k.split('-')[0], v) for k, v in LUM.items() if
                     k.split('-')[0] not in langs)
        ranked = parse_accept_lang_header(accept_lang)
        for lang, _ in ranked:
            lang = lang.lower()
            if lang in langs:
                return langs[lang]
            pre = lang.split('-')[0]
            if pre in langs:
                return langs[pre]

    def fix(self, path):
        path = path.lstrip('/')
        url_parts = [self.request.META['SCRIPT_NAME']]

        if path.partition('/')[0] not in settings.SUPPORTED_NONLOCALES:
            locale = self.locale if self.locale else self.get_language()
            url_parts.append(locale)

        url_parts.append(path)

        return '/'.join(url_parts)
