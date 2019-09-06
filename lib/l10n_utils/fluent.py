import json
import re
from functools import wraps
from hashlib import md5

from django.conf import settings
from django.core.cache import caches
from django.utils.encoding import force_bytes
from django.utils.functional import lazy, cached_property

from fluent.runtime import FluentLocalization, FluentResourceLoader
from fluent.syntax.ast import GroupComment, Message

from lib.l10n_utils import translation

__all__ = [
    'fluent_l10n',
    'ftl',
    'ftl_file_is_active',
    'ftl_has_messages',
    'ftl_lazy',
    'get_metadata_file_path',
    'has_messages',
    'translate',
]
cache = caches['l10n']
REQUIRED_RE = re.compile(r'^required\b', re.MULTILINE | re.IGNORECASE)


class FluentL10n(FluentLocalization):
    def _localized_bundles(self):
        for bundle in self._bundles():
            if bundle.locales[0] == self.locales[0]:
                yield bundle

    @cached_property
    def _message_ids(self):
        messages = set()
        for bundle in self._bundles():
            messages.update(bundle._messages.keys())

        return list(messages)

    @cached_property
    def _localized_message_ids(self):
        messages = set()
        for bundle in self._localized_bundles():
            messages.update(bundle._messages.keys())

        return list(messages)

    @cached_property
    def required_message_ids(self):
        """
        Look in the "en" file for message IDs grouped by a comment that starts with "Required"

        :return: list of message IDs
        """
        messages = set()
        for resources in self.resource_loader.resources('en', self.resource_ids):
            for resource in resources:
                in_required = False
                for item in resource.body:
                    if isinstance(item, GroupComment):
                        in_required = REQUIRED_RE.search(item.content)
                        continue

                    if isinstance(item, Message) and in_required:
                        messages.add(item.id.name)

        return list(messages)

    @cached_property
    def has_required_messages(self):
        return all(self.has_message(m) for m in self.required_message_ids)

    @cached_property
    def active_locales(self):
        if settings.DEV:
            return settings.DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES

        # first resource is the one to check for activation
        return get_active_locales(self.resource_ids[0])

    @cached_property
    def percent_translated(self):
        return (float(len(self._localized_message_ids)) / float(len(self._message_ids))) * 100

    def has_message(self, message_id):
        # assume English locales have the message
        if self.locales[0].startswith('en-'):
            return True

        return message_id in self._localized_message_ids


def _cache_key(*args, **kwargs):
    key = f'fluent:{args}:{kwargs}'
    return md5(force_bytes(key)).hexdigest()


def memoize(f):
    """Decorator to cache the results of expensive functions"""
    @wraps(f)
    def inner(*args, **kwargs):
        key = _cache_key(f.__name__, *args, **kwargs)
        value = cache.get(key)
        if value is None:
            value = f(*args, **kwargs)
            cache.set(key, value)

        return value

    return inner


def l10nize(f):
    """Decorator to create and pass in the l10n object"""
    @wraps(f)
    def inner(ftl_files, *args, **kwargs):
        locale = kwargs.get('locale') or translation.get_language(True)
        l10n = fluent_l10n([locale, 'en'], ftl_files)
        return f(l10n, *args, **kwargs)

    return inner


def get_metadata_file_path(ftl_file):
    return settings.FLUENT_REPO_PATH.joinpath('metadata', ftl_file).with_suffix('.json')


def get_metadata(ftl_file):
    path = get_metadata_file_path(ftl_file)
    try:
        with path.open() as mdf:
            return json.load(mdf)
    except (IOError, ValueError):
        return {}


@memoize
def get_active_locales(ftl_file):
    locales = {settings.LANGUAGE_CODE}
    metadata = get_metadata(ftl_file)
    if metadata and 'active_locales' in metadata:
        locales.update(metadata['active_locales'])
        i_locales = metadata.get('inactive_locales')
        if i_locales:
            locales.difference_update(i_locales)

    return sorted(locales)


def ftl_file_is_active(ftl_file, locale=None):
    """Return True if the given FTL file is active in the given locale."""
    locale = locale or translation.get_language(True)
    return locale in get_active_locales(ftl_file)


@memoize
def fluent_l10n(locales, files):
    if isinstance(locales, str):
        locales = [locales]

    # file IDs may not have file extension
    files = [f'{f}.ftl' if not f.endswith('.ftl') else f for f in files]
    paths = [f'{path}/{{locale}}/' for path in settings.FLUENT_PATHS]
    loader = FluentResourceLoader(paths)
    return FluentL10n(locales, files, loader)


@memoize
def ftl_has_messages(l10n, *message_ids, require_all=True):
    test = all if require_all else any
    return test([l10n.has_message(mid) for mid in message_ids])


@memoize
def translate(l10n, message_id, fallback=None, **kwargs):
    # check the `locale` bundle for the message if we have a fallback defined
    if fallback and not l10n.has_message(message_id):
        message_id = fallback

    return l10n.format_value(message_id, kwargs)


# View Utils

# for use in python views
has_messages = l10nize(ftl_has_messages)
ftl = l10nize(translate)

# for use in python outside of a view
ftl_lazy = lazy(ftl, str)
