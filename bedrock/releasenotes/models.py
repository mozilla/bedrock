import codecs
import json
import os
from glob import glob
from hashlib import sha256
from operator import attrgetter

from django.conf import settings
from django.core.cache import caches
from django.http import Http404
from django.utils.dateparse import parse_date, parse_datetime
from django.utils.functional import cached_property
from django.utils.text import slugify

import markdown
from product_details.version_compare import Version
from raven.contrib.django.raven_compat.models import client as sentry_client

from bedrock.base.urlresolvers import reverse


cache = caches['release-notes']
markdowner = markdown.Markdown(extensions=[
    'tables', 'codehilite', 'fenced_code', 'toc', 'nl2br'
])


def release_notes_path():
    return os.path.join(settings.RELEASE_NOTES_PATH, 'releases')


def process_markdown(value):
    return markdowner.reset().convert(value)


def process_notes(notes):
    notes = [Note(d) for d in notes]
    return [n for n in notes if n.is_public]


def process_is_public(is_public):
    if settings.DEV:
        return True

    return is_public


def process_note_release(rel_data):
    return Release(rel_data)


FIELD_PROCESSORS = {
    'release_date': parse_date,
    'created': parse_datetime,
    'modified': parse_datetime,
    'notes': process_notes,
    'is_public': process_is_public,
    'note': process_markdown,
    'text': process_markdown,
    'system_requirements': process_markdown,
    'fixed_in_release': process_note_release,
}


class ReleaseNotFound(Exception):
    pass


class RNModel(object):
    def __init__(self, data):
        for key, value in data.items():
            if not hasattr(self, key):
                continue
            if key in FIELD_PROCESSORS:
                value = FIELD_PROCESSORS[key](value)
            setattr(self, key, value)


class Note(RNModel):
    id = None
    bug = None
    note = ''
    tag = None
    is_public = True
    fixed_in_release = None
    sort_num = None
    created = None
    modified = None


class Release(RNModel):
    CHANNELS = ['release', 'esr', 'beta', 'aurora', 'nightly']
    product = None
    channel = None
    version = None
    slug = None
    title = None
    release_date = None
    text = ''
    is_public = True
    bug_list = None
    bug_search_url = None
    system_requirements = None
    created = None
    modified = None
    notes = None

    @cached_property
    def major_version(self):
        return str(self.version_obj.major)

    @cached_property
    def version_obj(self):
        return Version(self.version)

    def get_absolute_url(self):
        prefix = 'aurora' if self.channel == 'Aurora' else 'release'
        if self.product == 'Thunderbird':
            return reverse('thunderbird.notes', args=[self.version])
        if self.product == 'Firefox for Android':
            return reverse('firefox.android.releasenotes', args=(self.version, prefix))
        if self.product == 'Firefox for iOS':
            return reverse('firefox.ios.releasenotes', args=(self.version, prefix))
        else:
            return reverse('firefox.desktop.releasenotes', args=(self.version, prefix))

    def get_bug_search_url(self):
        if self.bug_search_url:
            return self.bug_search_url

        if self.product == 'Thunderbird':
            return (
                'https://bugzilla.mozilla.org/buglist.cgi?'
                'classification=Client%20Software&query_format=advanced&'
                'bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&'
                'target_milestone=Thunderbird%20{version}.0&product=Thunderbird'
                '&resolution=FIXED'
            ).format(version=self.major_version)

        return (
            'https://bugzilla.mozilla.org/buglist.cgi?'
            'j_top=OR&f1=target_milestone&o3=equals&v3=Firefox%20{version}&'
            'o1=equals&resolution=FIXED&o2=anyexact&query_format=advanced&'
            'f3=target_milestone&f2=cf_status_firefox{version}&'
            'bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&'
            'v1=mozilla{version}&v2=fixed%2Cverified&limit=0'
        ).format(version=self.major_version)

    def equivalent_release_for_product(self, product):
        """
        Returns the release for a specified product with the same
        channel and major version with the highest minor version,
        or None if no such releases exist
        """
        major_version_file_id = get_file_id(product, self.channel, self.major_version + '.*')
        releases = glob(os.path.join(release_notes_path(), major_version_file_id + '.json'))
        if releases:
            releases = [get_release_from_file(fn) for fn in releases]
            releases = [r for r in releases if r.is_public]
            if releases:
                return sorted(releases, reverse=True, key=attrgetter('version_obj'))[0]

        return None

    def equivalent_android_release(self):
        if self.product == 'Firefox':
            return self.equivalent_release_for_product('Firefox for Android')

    def equivalent_desktop_release(self):
        if self.product == 'Firefox for Android':
            return self.equivalent_release_for_product('Firefox')


def get_release(product, version, channel=None):
    channels = [channel] if channel else Release.CHANNELS
    if product.lower() == 'firefox extended support release':
        product = 'firefox'
        channels = ['esr']
    for channel in channels:
        file_name = get_release_file_name(product, channel, version)
        if not file_name:
            continue

        release = get_release_from_file(file_name)
        if release is not None:
            return release

    raise ReleaseNotFound()


def get_data_version():
    """Add the etag from the repo to the cache keys.

    This will ensure that the cache is invalidated when the repo is updated.
    """
    etag_key = 'releasenotes:repo:etag'
    etag = cache.get(etag_key)
    print etag
    if not etag:
        etag_file = os.path.join(release_notes_path(), '.latest-update-etag')
        if os.path.exists(etag_file):
            try:
                with codecs.open(etag_file) as fh:
                    etag = fh.read().strip()
                    cache.set(etag_key, etag, 60)  # 1 min
            except IOError:
                etag = 'default'
        else:
            etag = 'default'

    return etag


def get_cache_key(key):
    """Cache key returned will be a sha256 hash of the key and repo data version.

    This ensures that we can use a long cache for the release files while still
    getting fast invalidation when we check the small repo data version file
    at most once per minute.
    """
    return sha256('%s:%s' % (get_data_version(), key)).hexdigest()


def get_release_from_file(file_name):
    release = cache.get(get_cache_key(file_name))
    if not release:
        release = get_release_from_file_system(file_name)
        if release:
            cache.set(file_name, release, 7200)  # 2 hours

    return release


def get_release_from_file_system(file_name):
    try:
        with codecs.open(file_name, 'r', encoding='utf-8') as rel_fh:
            return Release(json.load(rel_fh))
    except Exception:
        sentry_client.captureException()
        return None


def get_release_file_name(product, channel, version):
    file_id = get_file_id(product, channel, version)
    file_name = os.path.join(release_notes_path(), '{}.json'.format(file_id))
    if os.path.exists(file_name):
        return file_name

    return None


def get_file_id(product, channel, version):
    product = slugify(product)
    channel = channel.lower()
    if product == 'firefox-extended-support-release':
        product = 'firefox'
        channel = 'esr'
    return '-'.join([product, version, channel])


def get_release_or_404(version, product):
    try:
        release = get_release(product, version)
    except ReleaseNotFound:
        raise Http404

    if not release.is_public:
        raise Http404

    return release


def get_releases_or_404(product, channel):
    file_prefix = get_file_id(product, channel, '*')
    releases = glob(os.path.join(release_notes_path(), file_prefix + '.*'))
    if releases:
        return [get_release_from_file(r) for r in releases]

    raise Http404
