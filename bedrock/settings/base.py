# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import platform
import socket
import struct
import sys
from os.path import abspath

from django.utils.functional import lazy

import sentry_sdk
from everett.manager import ListOf
from pathlib import Path
from sentry_sdk.integrations.django import DjangoIntegration

from bedrock.base.config_manager import config


# ROOT path of the project. A pathlib.Path object.
DATA_PATH = config('DATA_PATH', default='data')
ROOT_PATH = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT_PATH / DATA_PATH
ROOT = str(ROOT_PATH)


def path(*args):
    return abspath(str(ROOT_PATH.joinpath(*args)))


def data_path(*args):
    return abspath(str(DATA_PATH.joinpath(*args)))


# Is this a dev instance?
DEV = config('DEV', parser=bool, default='false')
PROD = config('PROD', parser=bool, default='false')
DEBUG = config('DEBUG', parser=bool, default='false')
DATABASES = {
    'default': {
        'ENGINE': 'django_prometheus.db.backends.sqlite3',
        'NAME': data_path('bedrock.db'),
    },
}

CACHES = {
    'default': {
        'BACKEND': 'bedrock.base.cache.SimpleDictCache',
        'LOCATION': 'default',
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 5000,
            'CULL_FREQUENCY': 4,  # 1/4 entries deleted if max reached
        },
    }
}

# in case django-pylibmc is in use
PYLIBMC_MIN_COMPRESS_LEN = 150 * 1024
PYLIBMC_COMPRESS_LEVEL = 1  # zlib.Z_BEST_SPEED

# Logging
LOG_LEVEL = config('LOG_LEVEL', default='INFO')
HAS_SYSLOG = True
SYSLOG_TAG = "http_app_bedrock"
LOGGING_CONFIG = None

# CEF Logging
CEF_PRODUCT = 'Bedrock'
CEF_VENDOR = 'Mozilla'
CEF_VERSION = '0'
CEF_DEVICE_VERSION = '0'


# Internationalization.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = config('TIME_ZONE', default='America/Los_Angeles')

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

USE_TZ = True

USE_ETAGS = config('USE_ETAGS', default=str(not DEBUG), parser=bool)

# just here so Django doesn't complain
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

# Tells the product_details module where to find our local JSON files.
# This ultimately controls how LANGUAGES are constructed.
PROD_DETAILS_CACHE_NAME = 'product-details'
PROD_DETAILS_CACHE_TIMEOUT = 60 * 15  # 15 min
PROD_DETAILS_STORAGE = config('PROD_DETAILS_STORAGE',
                              default='product_details.storage.PDDatabaseStorage')
# path into which to clone the p-d json repo
PROD_DETAILS_JSON_REPO_PATH = config('PROD_DETAILS_JSON_REPO_PATH',
                                     default=data_path('product_details_json'))
PROD_DETAILS_JSON_REPO_URI = config('PROD_DETAILS_JSON_REPO_URI',
                                    default='https://github.com/mozilla-releng/product-details.git')
PROD_DETAILS_JSON_REPO_BRANCH = config('PROD_DETAILS_JSON_REPO_BRANCH', default='production')
# path to updated p-d data for testing before loading into DB
PROD_DETAILS_TEST_DIR = str(Path(PROD_DETAILS_JSON_REPO_PATH).joinpath('public', '1.0'))

# Accepted locales
PROD_LANGUAGES = ('ach', 'af', 'an', 'ar', 'ast', 'az', 'azz', 'be', 'bg',
                  'bn', 'br', 'bs', 'ca', 'cak', 'cs',
                  'cy', 'da', 'de', 'dsb', 'el', 'en-CA', 'en-GB', 'en-US',
                  'eo', 'es-AR', 'es-CL', 'es-ES', 'es-MX', 'et',
                  'eu', 'fa', 'ff', 'fi', 'fr', 'fy-NL', 'ga-IE', 'gd',
                  'gl', 'gn', 'gu-IN', 'he', 'hi-IN', 'hr', 'hsb',
                  'hu', 'hy-AM', 'ia', 'id', 'is', 'it', 'ja', 'ja-JP-mac',
                  'ka', 'kab', 'kk', 'km', 'kn', 'ko', 'lij', 'lt', 'ltg', 'lv',
                  'mk', 'ml', 'mr', 'ms', 'my', 'nb-NO', 'ne-NP', 'nl',
                  'nn-NO', 'oc', 'pa-IN', 'pl', 'pt-BR', 'pt-PT',
                  'rm', 'ro', 'ru', 'si', 'sk', 'sl', 'son', 'sq',
                  'sr', 'sv-SE', 'ta', 'te', 'th', 'tl', 'tr', 'trs', 'uk', 'ur',
                  'uz', 'vi', 'xh', 'zh-CN', 'zh-TW', 'zu')

LOCALES_PATH = DATA_PATH / 'locale'
default_locales_repo = 'www.mozilla.org' if DEV else 'bedrock-l10n'
default_locales_repo = 'https://github.com/mozilla-l10n/{}'.format(default_locales_repo)
LOCALES_REPO = config('LOCALES_REPO', default=default_locales_repo)
GITHUB_REPO = 'https://github.com/mozilla/bedrock'

# templates to exclude from having an "edit this page" link in the footer
# these are typically ones for which most of the content is in the DB
EXCLUDE_EDIT_TEMPLATES = [
    'firefox/releases/nightly-notes.html',
    'firefox/releases/dev-browser-notes.html',
    'firefox/releases/esr-notes.html',
    'firefox/releases/beta-notes.html',
    'firefox/releases/aurora-notes.html',
    'firefox/releases/release-notes.html',
    'firefox/releases/notes.html',
    'firefox/releases/system_requirements.html',
    'mozorg/credits.html',
    'mozorg/about/forums.html',
    'security/advisory.html',
    'security/advisories.html',
    'security/product-advisories.html',
    'security/known-vulnerabilities.html',
]


def get_dev_languages():
    try:
        return [lang.name for lang in LOCALES_PATH.iterdir()
                if lang.is_dir() and lang.name != 'templates']
    except OSError:
        # no locale dir
        return list(PROD_LANGUAGES)


DEV_LANGUAGES = get_dev_languages()
DEV_LANGUAGES.append('en-US')

# Map short locale names to long, preferred locale names. This
# will be used in urlresolvers to determine the
# best-matching locale from the user's Accept-Language header.
CANONICAL_LOCALES = {
    'en': 'en-US',
    'es': 'es-ES',
    'ja-jp-mac': 'ja',
    'no': 'nb-NO',
    'pt': 'pt-BR',
    'sv': 'sv-SE',
    'zh-hant': 'zh-TW',     # Bug 1263193
    'zh-hant-tw': 'zh-TW',  # Bug 1263193
    'zh-hk': 'zh-TW',       # Bug 1338072
    'zh-hant-hk': 'zh-TW',  # Bug 1338072
}

# Unlocalized pages are usually redirected to the English (en-US) equivalent,
# but sometimes it would be better to offer another locale as fallback. This map
# specifies such cases.
FALLBACK_LOCALES = {
    'es-AR': 'es-ES',
    'es-CL': 'es-ES',
    'es-MX': 'es-ES',
}


def lazy_lang_group():
    """Groups languages with a common prefix into a map keyed on said prefix"""
    from django.conf import settings

    groups = {}
    langs = settings.DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    for lang in langs:
        if '-' in lang:
            prefix, _ = lang.split('-', 1)
            groups.setdefault(prefix, []).append(lang)

    # add any group prefix to the group list if it is also a supported lang
    for groupid in groups:
        if groupid in langs:
            groups[groupid].append(groupid)

    # exclude groups with a single member
    return {gid: glist for gid, glist in groups.items() if len(glist) > 1}


def lazy_lang_url_map():
    from django.conf import settings

    langs = settings.DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    return {i.lower(): i for i in langs}


# Override Django's built-in with our native names
def lazy_langs():
    from django.conf import settings
    from product_details import product_details

    langs = DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    return {lang.lower(): product_details.languages[lang]['native']
            for lang in langs if lang in product_details.languages}


LANG_GROUPS = lazy(lazy_lang_group, dict)()
LANGUAGE_URL_MAP = lazy(lazy_lang_url_map, dict)()
LANGUAGES = lazy(lazy_langs, dict)()

FEED_CACHE = 3900
# 30 min during dev and 10 min in prod
DOTLANG_CACHE = config('DOTLANG_CACHE', default='1800' if DEBUG else '600', parser=int)

# Global L10n files.
DOTLANG_FILES = ['main']
FLUENT_DEFAULT_FILES = [
    'banners/firefox-daylight-promo',
    'brands',
    'download_button',
    'footer',
    'fxa_form',
    'navigation',
    'newsletter_form',
    'send_to_device',
    'ui',
]

FLUENT_DEFAULT_PERCENT_REQUIRED = config('FLUENT_DEFAULT_PERCENT_REQUIRED', default='80', parser=int)
FLUENT_REPO = config('FLUENT_REPO', default='mozmeao/www-l10n')
FLUENT_REPO_URL = f'https://github.com/{FLUENT_REPO}'
FLUENT_REPO_PATH = DATA_PATH / 'www-l10n'
# will be something like "<github username>:<github token>"
FLUENT_REPO_AUTH = config('FLUENT_REPO_AUTH', default='')
FLUENT_LOCAL_PATH = ROOT_PATH / 'l10n'
FLUENT_L10N_TEAM_REPO = config('FLUENT_L10N_TEAM_REPO', default='mozilla-l10n/www-l10n')
FLUENT_L10N_TEAM_REPO_URL = f'https://github.com/{FLUENT_L10N_TEAM_REPO}'
FLUENT_L10N_TEAM_REPO_PATH = DATA_PATH / 'l10n-team'
# 10 seconds during dev and 10 min in prod
FLUENT_CACHE_TIMEOUT = config('FLUENT_CACHE_TIMEOUT', default='10' if DEBUG else '600', parser=int)
# order matters. first sting found wins.
FLUENT_PATHS = [
    # local FTL files
    FLUENT_LOCAL_PATH,
    # remote FTL files from l10n team
    FLUENT_REPO_PATH,
]
FLUENT_MIGRATIONS = 'lib.fluent_migrations'
FLUENT_MIGRATIONS_PATH = ROOT_PATH / 'lib' / 'fluent_migrations'

# Maxmind Database
# country code for /country-code.json to return in dev mode
DEV_GEO_COUNTRY_CODE = config('DEV_GEO_COUNTRY_CODE', default='US')
MAXMIND_DB_PATH = config('MAXMIND_DB_PATH', default=path('geoip', 'GeoIP2-Country.mmdb'))
MAXMIND_DEFAULT_COUNTRY = config('MAXMIND_DEFAULT_COUNTRY', default=DEV_GEO_COUNTRY_CODE)

# Paths that don't require a locale code in the URL.
# matches the first url component (e.g. mozilla.org/gameon/)
SUPPORTED_NONLOCALES = [
    # from redirects.urls
    'media',
    'static',
    'certs',
    'images',
    'contribute.json',
    'credits',
    'gameon',
    'robots.txt',
    'telemetry',
    'webmaker',
    'contributor-data',
    'healthz',
    'readiness',
    'healthz-cron',
    '2004',
    '2005',
    '2006',
    'keymaster',
    'microsummaries',
    'xbl',
    'country-code.json',
    'revision.txt',
    'locales',
    'prometheus',
    'sitemap_none.xml'
]
# Paths that can exist either with or without a locale code in the URL.
# Matches the whole URL path
SUPPORTED_LOCALE_IGNORE = [
    '/sitemap.xml'
]

# Pages that we don't want to be indexed by search engines.
# Only impacts sitemap generator. If you need to disallow indexing of
# specific URLs, add them to mozorg/templates/mozorg/robots.txt.
NOINDEX_URLS = [
    r'^(404|500)/',
    r'^firefox/welcome/',
    r'^contribute/(embed|event)/',
    r'^firefox/retention/thank-you/',
    r'^firefox/set-as-default/thanks/',
    r'^firefox/sms/sent/',
    r'^firefox/unsupported/',
    r'^firefox/send-to-device-post',
    r'^firefox/feedback',
    r'^firefox/stub_attribution_code/',
    r'^firefox/dedicated-profiles/',
    r'^firefox/installer-help/',
    r'^firefox/this-browser-comes-highly-recommended/',
    r'^firefox/nightly/notes/feed/$',
    r'^firefox.*/all/$',
    r'^firefox/enterprise/signup/',
    r'^.+/(firstrun|whatsnew)/$',
    r'^m/',
    r'^newsletter/(confirm|existing|hacks\.mozilla\.org|recovery|updated|fxa-error)/',
    r'^newsletter/opt-out-confirmation/',
    r'^newsletter/country/success/',
    r'/system-requirements/$',
    r'.*/(firstrun|thanks)/$',
    r'^readiness/$',
    r'^healthz(-cron)?/$',
    r'^country-code\.json$',
    # exclude redirects
    r'^foundation/annualreport/$'
    r'^firefox/notes/$'
    r'^teach/$'
    r'^about/legal/impressum/$',
    r'^security/announce/',
    r'^exp/',
    r'^prometheus/',
]

# Pages we do want indexed but don't show up in automated URL discovery
# or are only available in a non-default locale
EXTRA_INDEX_URLS = {
    '/privacy/firefox-klar/': ['de'],
    '/about/legal/impressum/': ['de'],
}

SITEMAPS_REPO = config('SITEMAPS_REPO',
                       default='https://github.com/mozmeao/www-sitemap-generator.git')
SITEMAPS_PATH = DATA_PATH / 'sitemaps'

# Pages that have different URLs for different locales, e.g.
#   'firefox/private-browsing/': {
#       'en-US': '/firefox/features/private-browsing/',
#   },
ALT_CANONICAL_PATHS = {}

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', parser=ListOf(str),
    default='www.mozilla.org,www.ipv6.mozilla.org,www.allizom.org')
ALLOWED_CIDR_NETS = config('ALLOWED_CIDR_NETS', default='', parser=ListOf(str))

# The canonical, production URL without a trailing slash
CANONICAL_URL = 'https://www.mozilla.org'

# Make this unique, and don't share it with anybody.
SECRET_KEY = config('SECRET_KEY', default='ssssshhhhh')

MEDIA_URL = config('MEDIA_URL', default='/user-media/')
MEDIA_ROOT = config('MEDIA_ROOT', default=path('media'))
STATIC_URL = config('STATIC_URL', default='/media/')
STATIC_ROOT = config('STATIC_ROOT', default=path('static'))
STATICFILES_STORAGE = ('django.contrib.staticfiles.storage.StaticFilesStorage' if DEBUG else
                       'django.contrib.staticfiles.storage.ManifestStaticFilesStorage')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
STATICFILES_DIRS = (
    path('static_final'),
)
if DEBUG:
    STATICFILES_DIRS += (path('media'),)


def set_whitenoise_headers(headers, path, url):
    if '/fonts/' in url or '/caldata/' in url:
        cache_control = 'public, max-age={}'.format(604800)  # one week
        headers['Cache-Control'] = cache_control

    if url.startswith('/.well-known/matrix/'):
        headers['Content-Type'] = 'application/json'


WHITENOISE_ADD_HEADERS_FUNCTION = set_whitenoise_headers
WHITENOISE_ROOT = config('WHITENOISE_ROOT', default=path('root_files'))
WHITENOISE_MAX_AGE = 6 * 60 * 60  # 6 hours

PROJECT_MODULE = 'bedrock'

ROOT_URLCONF = 'bedrock.urls'

# Tells the extract script what files to look for L10n in and what function
# handles the extraction.
PUENTE = {
    'BASE_DIR': ROOT,
    'PROJECT': 'Bedrock',
    'MSGID_BUGS_ADDRESS': 'https://bugzilla.mozilla.org/enter_bug.cgi?'
                          'product=www.mozilla.org&component=L10N',
    'DOMAIN_METHODS': {
        'django': [
            ('bedrock/**.py', 'lib.l10n_utils.extract.extract_python'),
            ('bedrock/**/templates/**.html', 'lib.l10n_utils.extract.extract_jinja2'),
            ('bedrock/**/templates/**.js', 'lib.l10n_utils.extract.extract_jinja2'),
            ('bedrock/**/templates/**.jsonp', 'lib.l10n_utils.extract.extract_jinja2'),
        ],
    }
}


def get_app_name(hostname):
    """
    Get the app name from the host name.

    The hostname in our deployments will be in the form `bedrock-{version}-{type}-{random-ID}`
    where {version} is "dev", "stage", or "prod", and {type} is the process type
    (e.g. "web" or "clock"). Everywhere else it won't be in this form and will return None.
    """
    if hostname.startswith('bedrock-'):
        app_mode = hostname.split('-')[1]
        return 'bedrock-' + app_mode

    return 'bedrock'


HOSTNAME = platform.node()
APP_NAME = get_app_name(HOSTNAME)
CLUSTER_NAME = config('CLUSTER_NAME', default='')
ENABLE_HOSTNAME_MIDDLEWARE = config('ENABLE_HOSTNAME_MIDDLEWARE',
                                    default=str(bool(APP_NAME)), parser=bool)
ENABLE_VARY_NOCACHE_MIDDLEWARE = config('ENABLE_VARY_NOCACHE_MIDDLEWARE',
                                        default='true', parser=bool)
# set this to enable basic auth for the entire site
# e.g. BASIC_AUTH_CREDS="thedude:thewalrus"
BASIC_AUTH_CREDS = config('BASIC_AUTH_CREDS', default='')

# reduce the number of latency buckets for prom
# see https://github.com/korfuri/django-prometheus#configuration
PROMETHEUS_LATENCY_BUCKETS = (
    0.05,
    0.1,
    0.5,
    1.0,
    5.0,
    10.0,
    50.0,
    float("inf"),
)
PROMETHEUS_METRIC_NAMESPACE = APP_NAME.replace('-', '_')

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'allow_cidr.middleware.AllowCIDRMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'bedrock.mozorg.middleware.VaryNoCacheMiddleware',
    'bedrock.base.middleware.BasicAuthMiddleware',
    # must come before LocaleURLMiddleware
    'bedrock.redirects.middleware.RedirectsMiddleware',
    'bedrock.base.middleware.LocaleURLMiddleware',
    'bedrock.mozorg.middleware.ClacksOverheadMiddleware',
    'bedrock.mozorg.middleware.HostnameMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'bedrock.mozorg.middleware.CacheMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ENABLE_CSP_MIDDLEWARE = config('ENABLE_CSP_MIDDLEWARE', default='true', parser=bool)
if ENABLE_CSP_MIDDLEWARE:
    MIDDLEWARE.append('csp.middleware.CSPMiddleware')

INSTALLED_APPS = (
    # Django contrib apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.messages',

    # Third-party apps, patches, fixes
    'commonware.response.cookies',

    # L10n
    'puente',  # for ./manage.py extract
    'product_details',

    # third-party apps
    'django_jinja_markdown',
    'pagedown',
    'localflavor',
    'django_jinja',
    'watchman',
    'django_prometheus',

    # Local apps
    'bedrock.base',
    'bedrock.firefox',
    'bedrock.foundation',
    'bedrock.grants',
    'bedrock.legal',
    'bedrock.legal_docs',
    'bedrock.mozorg',
    'bedrock.newsletter',
    'bedrock.press',
    'bedrock.privacy',
    'bedrock.externalfiles',
    'bedrock.security',
    'bedrock.releasenotes',
    'bedrock.contentcards',
    'bedrock.utils',
    'bedrock.wordpress',
    'bedrock.sitemaps',
    'bedrock.pocketfeed',
    'bedrock.exp',
    # last so that redirects here will be last
    'bedrock.redirects',

    # libs
    'django_extensions',
    'lib.l10n_utils',
    'captcha',
)

# Must match the list at CloudFlare if the
# VaryNoCacheMiddleware is enabled. The home
# page is exempt by default.
VARY_NOCACHE_EXEMPT_URL_PREFIXES = (
    '/firefox/',
    '/contribute/',
    '/about/',
    '/contact/',
    '/newsletter/',
    '/privacy/',
    '/foundation/',
)

# Sessions
#
# By default, be at least somewhat secure with our session cookies.
SESSION_COOKIE_HTTPONLY = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# legacy setting. backward compat.
DISABLE_SSL = config('DISABLE_SSL', default='true', parser=bool)
# SecurityMiddleware settings
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default='0', parser=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default='true', parser=bool)
SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', default='true', parser=bool)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=str(not DISABLE_SSL), parser=bool)
SECURE_REDIRECT_EXEMPT = [
    r'^readiness/$',
    r'^healthz(-cron)?/$',
]
if config('USE_SECURE_PROXY_HEADER', default=str(SECURE_SSL_REDIRECT), parser=bool):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# watchman
WATCHMAN_DISABLE_APM = True
WATCHMAN_CHECKS = (
    'watchman.checks.caches',
    'watchman.checks.databases',
)

LOCALE_PATHS = (
    str(LOCALES_PATH),
)

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': LOCALE_PATHS,
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': None,
            'undefined': 'jinja2.Undefined',
            'finalize': lambda x: x if x is not None else '',
            'translation_engine': 'lib.l10n_utils.template',
            'newstyle_gettext': False,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'bedrock.base.context_processors.i18n',
                'bedrock.base.context_processors.globals',
                'bedrock.mozorg.context_processors.canonical_path',
                'bedrock.mozorg.context_processors.contrib_numbers',
                'bedrock.mozorg.context_processors.current_year',
                'bedrock.mozorg.context_processors.funnelcake_param',
                'bedrock.mozorg.context_processors.facebook_locale',
                'bedrock.firefox.context_processors.latest_firefox_versions',
            ],
            'extensions': [
                'jinja2.ext.do',
                'jinja2.ext.with_',
                'jinja2.ext.loopcontrols',
                'jinja2.ext.autoescape',
                'django_jinja.builtins.extensions.CsrfExtension',
                'django_jinja.builtins.extensions.StaticFilesExtension',
                'django_jinja.builtins.extensions.DjangoFiltersExtension',
                'lib.l10n_utils.template.i18n',
                'lib.l10n_utils.template.l10n_blocks',
                'lib.l10n_utils.template.lang_blocks',
                'django_jinja_markdown.extensions.MarkdownExtension',
            ],
        }
    },
]

# use the Wordpress JSON REST API to get blog data
WP_BLOGS = {
    'firefox': {
        'url': 'https://blog.mozilla.org/firefox/',
        'name': 'The Firefox Frontier',
        # default num_posts is 20
        # uncomment and change this to get more
        # 'num_posts': 20,
    },
    'hacks': {
        'url': 'https://hacks.mozilla.org/',
        'name': 'Hacks',
    },
    'cd': {
        'url': 'https://connected.mozilla.org/',
        'name': 'Connected Devices',
    },
    'futurereleases': {
        'url': 'https://blog.mozilla.org/futurereleases/',
        'name': 'Future Releases',
    },
    'internetcitizen': {
        'url': 'https://blog.mozilla.org/internetcitizen/',
        'name': 'Internet Citizen',
    },
}

# used to connect to @MozillaHQ Pocket account
POCKET_API_URL = config('POCKET_API_URL', default='https://getpocket.com/v3/firefox/profile-recs')
POCKET_CONSUMER_KEY = config('POCKET_CONSUMER_KEY', default='')
POCKET_ACCESS_TOKEN = config('POCKET_ACCESS_TOKEN', default='')

# Contribute numbers
# TODO: automate these
CONTRIBUTE_NUMBERS = {
    'num_mozillians': 10554,
    'num_languages': 87,
}

BASKET_URL = config('BASKET_URL', default='https://basket.mozilla.org')
BASKET_API_KEY = config('BASKET_API_KEY', default='')
BASKET_TIMEOUT = config('BASKET_TIMEOUT', parser=int, default='10')

BOUNCER_URL = config('BOUNCER_URL', default='https://download.mozilla.org/')

# reCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='')
RECAPTCHA_USE_SSL = config('RECAPTCHA_USE_SSL', parser=bool, default='true')

# Use a message storage mechanism that doesn't need a database.
# This can be changed to use session once we do add a database.
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


default_email_backend = ('django.core.mail.backends.console.EmailBackend' if DEBUG else
                         'django.core.mail.backends.smtp.EmailBackend')

EMAIL_BACKEND = config('EMAIL_BACKEND', default=default_email_backend)
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default='25', parser=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default='false', parser=bool)
EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX', default='[bedrock] ')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Google Analytics
GA_ACCOUNT_CODE = ''

EXTERNAL_FILES_PATH = config('EXTERNAL_FILES_PATH', default=data_path('community_data'))
EXTERNAL_FILES_BRANCH = config('EXTERNAL_FILES_BRANCH', default='master')
EXTERNAL_FILES_REPO = config('EXTERNAL_FILES_REPO', default='https://github.com/mozilla/community-data.git')
EXTERNAL_FILES = {
    'credits': {
        'type': 'bedrock.mozorg.credits.CreditsFile',
        'name': 'credits/names.csv',
    },
    'forums': {
        'type': 'bedrock.mozorg.forums.ForumsFile',
        'name': 'forums/raw-ng-list.txt',
    },
}

# Facebook Like button supported locales
# https://www.facebook.com/translations/FacebookLocales.xml
FACEBOOK_LIKE_LOCALES = ['af_ZA', 'ar_AR', 'az_AZ', 'be_BY', 'bg_BG',
                         'bn_IN', 'bs_BA', 'ca_ES', 'cs_CZ', 'cy_GB',
                         'da_DK', 'de_DE', 'el_GR', 'en_GB', 'en_PI',
                         'en_UD', 'en_US', 'eo_EO', 'es_ES', 'es_LA',
                         'et_EE', 'eu_ES', 'fa_IR', 'fb_LT', 'fi_FI',
                         'fo_FO', 'fr_CA', 'fr_FR', 'fy_NL', 'ga_IE',
                         'gl_ES', 'he_IL', 'hi_IN', 'hr_HR', 'hu_HU',
                         'hy_AM', 'id_ID', 'is_IS', 'it_IT', 'ja_JP',
                         'ka_GE', 'km_KH', 'ko_KR', 'ku_TR', 'la_VA',
                         'lt_LT', 'lv_LV', 'mk_MK', 'ml_IN', 'ms_MY',
                         'nb_NO', 'ne_NP', 'nl_NL', 'nn_NO', 'pa_IN',
                         'pl_PL', 'ps_AF', 'pt_BR', 'pt_PT', 'ro_RO',
                         'ru_RU', 'sk_SK', 'sl_SI', 'sq_AL', 'sr_RS',
                         'sv_SE', 'sw_KE', 'ta_IN', 'te_IN', 'th_TH',
                         'tl_PH', 'tr_TR', 'uk_UA', 'vi_VN', 'zh_CN',
                         'zh_HK', 'zh_TW']

# Prefix for media. No trailing slash.
# e.g. '//mozorg.cdn.mozilla.net'
CDN_BASE_URL = config('CDN_BASE_URL', default='')

# newsletters that always show for FxA holders
FXA_NEWSLETTERS = [
    'firefox-accounts-journey',
    'test-pilot',
    'take-action-for-the-internet',
    'knowledge-is-power',
]
FXA_NEWSLETTERS_LOCALES = ['en', 'de', 'fr']

# Regional press blogs map to locales
PRESS_BLOG_ROOT = 'https://blog.mozilla.org/'
PRESS_BLOGS = {
    'de': 'press-de/',
    'en-GB': 'press-uk/',
    'en-US': 'press/',
    'es-AR': 'press-es/',
    'es-CL': 'press-es/',
    'es-ES': 'press-es/',
    'es-MX': 'press-es/',
    'fr': 'press-fr/',
    'it': 'press-it/',
    'pl': 'press-pl/',
    'pt-BR': 'press-br/',
}

DONATE_LINK = ('https://donate.mozilla.org/{locale}/'
    '?presets={presets}&amount={default}'
    '&utm_source=mozilla.org&utm_medium=referral&utm_content={source}'
    '&currency={currency}')

DONATE_PARAMS = {
    'en-US': {
        'currency': 'usd',
        'symbol': '$',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'an': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'as': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'ast': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'az': {
        'currency': 'azn',
        'symbol': u'₼',
        'presets': '34,17,8,5',
        'default': '17'
    },
    'bn': {
        'currency': 'bdt',
        'symbol': u'৳',
        'presets': '1700,840,420,250',
        'default': '840'
    },
    'bn-BD': {
        'currency': 'bdt',
        'symbol': u'৳',
        'presets': '1700,840,420,250',
        'default': '840'
    },
    'bn-IN': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'brx': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'ca': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'cak': {
        'currency': 'gtq',
        'symbol': 'Q',
        'presets': '145,70,35,20',
        'default': '70'
    },
    'cs': {
        'currency': 'czk',
        'symbol': u'Kč',
        'presets': '450,220,110,70',
        'default': '220'
    },
    'cy': {
        'currency': 'gbp',
        'symbol': u'£',
        'presets': '40,25,15,8',
        'default': '25'
    },
    'da': {
        'currency': 'dkk',
        'symbol': 'kr',
        'presets': '130,60,30,20',
        'default': '60'
    },
    'de': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'dsb': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'el': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'en-CA': {
        'currency': 'cad',
        'symbol': u'$',
        'presets': '65,30,15,4',
        'default': '30'
    },
    'en-GB': {
        'currency': 'gbp',
        'symbol': u'£',
        'presets': '40,25,15,8',
        'default': '25'
    },
    'es-AR': {
        'currency': 'ars',
        'symbol': '$',
        'presets': '730,370,200,110',
        'default': '370'
    },
    'es-CL': {
        'currency': 'clp',
        'symbol': '$',
        'presets': '13000,6500,3250,2000',
        'default': '6500'
    },
    'es-ES': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'es-MX': {
        'currency': 'mxn',
        'symbol': '$',
        'presets': '400,200,100,60',
        'default': '200'
    },
    'eo': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'et': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'eu': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'fi': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'fr': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'fy-NL': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'ga-IE': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'gd': {
        'currency': 'gbp',
        'symbol': u'£',
        'presets': '40,25,15,8',
        'default': '25'
    },
    'gl': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'gu-IN': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'he': {
        'currency': 'ils',
        'symbol': u'₪',
        'presets': '60,30,15,9',
        'default': '30'
    },
    'hi-IN': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'hsb': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'hr': {
        'currency': 'hrk',
        'symbol': 'kn',
        'presets': '128,64,32,19',
        'default': '64'
    },
    'hu': {
        'currency': 'huf',
        'symbol': 'Ft',
        'presets': '5600,2800,1400,850',
        'default': '2800'
    },
    'id': {
        'currency': 'idr',
        'symbol': 'Rp',
        'presets': '300000,150000,75000,45000',
        'default': '150000'
    },
    'it': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'ja': {
        'currency': 'jpy',
        'symbol': u'¥',
        'presets': '2240,1120,560,340',
        'default': '1120'
    },
    'ka': {
        'currency': 'gel',
        'symbol': u'₾',
        'presets': '50,25,12,7',
        'default': '25'
    },
    'kab': {
        'currency': 'dzd',
        'symbol': u'د.ج.‏',
        'presets': '2400,1200,600,350',
        'default': '1200'
    },
    'ko': {
        'currency': 'krw',
        'symbol': u'₩',
        'presets': '22320,11160,5580,3350',
        'default': '11160'
    },
    'kn': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'lij': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'lt': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'lv': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'ml': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'mr': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'ms': {
        'currency': 'myr',
        'symbol': 'RM',
        'presets': '85,42,21,13',
        'default': '42'
    },
    'nb-NO': {
        'currency': 'nok',
        'symbol': 'kr',
        'presets': '160,80,40,20',
        'default': '80'
    },
    'nn-NO': {
        'currency': 'nok',
        'symbol': 'kr',
        'presets': '160,80,40,20',
        'default': '80'
    },
    'nl': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'or': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'pa-IN': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'pl': {
        'currency': 'pln',
        'symbol': u'zł',
        'presets': '80,40,20,10',
        'default': '40'
    },
    'pt-BR': {
        'currency': 'brl',
        'symbol': 'R$',
        'presets': '80,40,20,10',
        'default': '40'
    },
    'pt-PT': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'ro': {
        'currency': 'ron',
        'symbol': 'lei',
        'presets': '80,40,20,12',
        'default': '40'
    },
    'ru': {
        'currency': 'rub',
        'symbol': u'₽',
        'presets': '1300,800,500,200',
        'default': '800'
    },
    'sat': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'sk': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'sl': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'sq': {
        'currency': 'all',
        'symbol': 'L',
        'presets': '2280,1140,570,350',
        'default': '1140'
    },
    'sr': {
        'currency': 'eur',
        'symbol': u'€',
        'presets': '50,30,20,10',
        'default': '30'
    },
    'sv-SE': {
        'currency': 'sek',
        'symbol': 'kr',
        'presets': '180,90,45,30',
        'default': '90'
    },
    'ta': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'te': {
        'currency': 'inr',
        'symbol': u'₹',
        'presets': '1000,500,250,150',
        'default': '500'
    },
    'th': {
        'currency': 'thb',
        'symbol': u'฿',
        'presets': '500,250,125,75',
        'default': '250'
    },
    'tr': {
        'currency': 'try',
        'symbol': u'₺',
        'presets': '70,35,18,10',
        'default': '35'
    },
    'uk': {
        'currency': 'uah',
        'symbol': u'₴',
        'presets': '530,260,130,80',
        'default': '260'
    },
    'zh-CN': {
        'currency': 'cny',
        'symbol': u'¥',
        'presets': '140,70,35,20',
        'default': '70'
    },
    'zh-TW': {
        'currency': 'twd',
        'symbol': 'NT$',
        'presets': '480,240,150,70',
        'default': '240'
    },
}

# Official Firefox Twitter accounts
FIREFOX_TWITTER_ACCOUNTS = {
    'de': 'https://twitter.com/firefox_DE',
    'en-US': 'https://twitter.com/firefox',
    'es-ES': 'https://twitter.com/firefox_es',
    'fr': 'https://twitter.com/firefox_FR',
    'pt-BR': 'https://twitter.com/firefoxbrasil',
}

# Fx Accounts iframe-less form & JS endpoint
# ***This URL *MUST* end in a traling slash!***

# other acceptable values below are:
#   - https://accounts.stage.mozaws.net/ (stage)
#   - https://stable.dev.lcip.org/ (demo/local)
FXA_ENDPOINT = config('FXA_ENDPOINT',
                       default='https://accounts.firefox.com/')

FXA_ENDPOINT_MOZILLAONLINE = config('FXA_ENDPOINT_MOZILLAONLINE',
                                    default='https://accounts.firefox.com.cn/')

# Google Play and Apple App Store settings
from .appstores import (GOOGLE_PLAY_FIREFOX_LINK, GOOGLE_PLAY_FIREFOX_LINK_UTMS,  # noqa
                        GOOGLE_PLAY_FIREFOX_LINK_MOZILLAONLINE,  # noqa
                        APPLE_APPSTORE_FIREFOX_LINK, APPLE_APPSTORE_COUNTRY_MAP,
                        APPLE_APPSTORE_FOCUS_LINK, GOOGLE_PLAY_FOCUS_LINK,
                        APPLE_APPSTORE_KLAR_LINK, GOOGLE_PLAY_KLAR_LINK,
                        APPLE_APPSTORE_POCKET_LINK, GOOGLE_PLAY_POCKET_LINK,
                        APPLE_APPSTORE_LOCKWISE_LINK, GOOGLE_PLAY_LOCKWISE_LINK,
                        GOOGLE_PLAY_FIREFOX_BETA_LINK, GOOGLE_PLAY_FIREFOX_NIGHTLY_LINK,
                        AMAZON_FIREFOX_FIRE_TV_LINK, GOOGLE_PLAY_FIREFOX_LITE_LINK,
                        GOOGLE_PLAY_FIREFOX_SEND_LINK,
                        ADJUST_FIREFOX_URL, ADJUST_FOCUS_URL,
                        ADJUST_KLAR_URL, ADJUST_POCKET_URL,
                        ADJUST_LOCKWISE_URL)

# Locales that should display the 'Send to Device' widget
SEND_TO_DEVICE_LOCALES = ['de', 'en-GB', 'en-US',
                          'es-AR', 'es-CL', 'es-ES', 'es-MX',
                          'fr', 'id', 'pl', 'pt-BR', 'ru', 'zh-TW']

SEND_TO_DEVICE_MESSAGE_SETS = {
    'default': {
        'sms_countries': config('STD_SMS_COUNTRIES_DEFAULT', default='US', parser=ListOf(str)),
        'sms': {
            'ios': 'ff-ios-download',
            'android': 'SMS_Android',
        },
        'email': {
            'android': 'download-firefox-android',
            'ios': 'download-firefox-ios',
            'all': 'download-firefox-mobile',
        }
    },
    'fx-android': {
        'sms_countries': config('STD_SMS_COUNTRIES_ANDROID', default='US', parser=ListOf(str)),
        'sms': {
            'ios': 'ff-ios-download',
            'android': 'android-download-embed',
        },
        'email': {
            'android': 'get-android-embed',
            'ios': 'download-firefox-ios',
            'all': 'download-firefox-mobile',
        }
    },
    'fx-mobile-download-desktop': {
        'sms_countries': config('STD_SMS_COUNTRIES_DESKTOP', default='US', parser=ListOf(str)),
        'sms': {
            'all': 'mobile-heartbeat',
        },
        'email': {
            'all': 'download-firefox-mobile-reco',
        }
    },
    'fx-whatsnew': {
        'sms_countries': config('STD_SMS_COUNTRIES_WHATSNEW50', default='US', parser=ListOf(str)),
        'sms': {
            'all': 'whatsnewfifty',
        },
        'email': {
            'all': 'download-firefox-mobile-whatsnew',
        }
    },
    'fx-focus': {
        'sms_countries': config('STD_SMS_COUNTRIES_WHATSNEW61', default='US', parser=ListOf(str)),
        'sms': {
            'all': 'focus_sms_whatsnew',
        },
        'email': {
            'all': 'download-focus-mobile-whatsnew',
        }
    },
    'fx-klar': {
        'sms_countries': config('STD_SMS_COUNTRIES_WHATSNEW61', default='US', parser=ListOf(str)),
        'sms': {
            'all': 'focus_sms_whatsnew',
        },
        'email': {
            'all': 'download-klar-mobile-whatsnew',
        }
    },
    'download-firefox-rocket': {
        'sms_countries': '',
        'email': {
            'all': 'download-firefox-rocket',
        }
    },
    'firefox-mobile-welcome': {
        'sms_countries': config('STD_SMS_COUNTRIES_MOBILE_WELCOME', default='US,DE,FR', parser=ListOf(str)),
        'sms': {
            'all': 'firefox-mobile-welcome',
        },
        'email': {
            'all': 'firefox-mobile-welcome',
        }
    },
    'lockwise-welcome-download': {
        'sms_countries': config('STD_SMS_COUNTRIES_MOBILE_WELCOME', default='US,DE,FR', parser=ListOf(str)),
        'sms': {
            'all': 'lockwise-welcome-download',
        },
        'email': {
            'all': 'lockwise-welcome-download',
        }
    }
}

if DEV:
    content_cards_default_branch = 'dev-processed'
else:
    content_cards_default_branch = 'prod-processed'

CONTENT_CARDS_PATH = config('CONTENT_CARDS_PATH', default=data_path('content_cards'))
CONTENT_CARDS_REPO = config('CONTENT_CARDS_REPO', default='https://github.com/mozmeao/www-admin.git')
CONTENT_CARDS_BRANCH = config('CONTENT_CARDS_BRANCH', default=content_cards_default_branch)
CONTENT_CARDS_URL = config('CONTENT_CARDS_URL', default=STATIC_URL)

RELEASE_NOTES_PATH = config('RELEASE_NOTES_PATH', default=data_path('release_notes'))
RELEASE_NOTES_REPO = config('RELEASE_NOTES_REPO', default='https://github.com/mozilla/release-notes.git')
RELEASE_NOTES_BRANCH = config('RELEASE_NOTES_BRANCH', default='master')

WWW_CONFIG_PATH = config('WWW_CONFIG_PATH', default=data_path('www_config'))
WWW_CONFIG_REPO = config('WWW_CONFIG_REPO', default='https://github.com/mozmeao/www-config.git')
WWW_CONFIG_BRANCH = config('WWW_CONFIG_BRANCH', default='master')

LEGAL_DOCS_PATH = DATA_PATH / 'legal_docs'
LEGAL_DOCS_REPO = config('LEGAL_DOCS_REPO', default='https://github.com/mozilla/legal-docs.git')
LEGAL_DOCS_BRANCH = config('LEGAL_DOCS_BRANCH', default='master' if DEV else 'prod')
LEGAL_DOCS_DMS_URL = config('LEGAL_DOCS_DMS_URL', default='')
LEGAL_DOCS_CACHE_TIMEOUT = config('LEGAL_DOCS_CACHE_TIMEOUT', default='60' if DEV else '600', parser=int)

MOFO_SECURITY_ADVISORIES_PATH = config('MOFO_SECURITY_ADVISORIES_PATH',
                                       default=data_path('mofo_security_advisories'))
MOFO_SECURITY_ADVISORIES_REPO = config('MOFO_SECURITY_ADVISORIES_REPO',
                                       default='https://github.com/mozilla/'
                                               'foundation-security-advisories.git')
MOFO_SECURITY_ADVISORIES_BRANCH = config('MOFO_SECURITY_ADVISORIES_BRANCH', default='master')

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/([a-zA-Z-]+/)?(newsletter)/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

PASSWORD_HASHERS = ['django.contrib.auth.hashers.PBKDF2PasswordHasher']
ADMINS = MANAGERS = config('ADMINS', parser=json.loads,
                           default='[]')

GTM_CONTAINER_ID = config('GTM_CONTAINER_ID', default='')
GMAP_API_KEY = config('GMAP_API_KEY', default='')
STUB_ATTRIBUTION_HMAC_KEY = config('STUB_ATTRIBUTION_HMAC_KEY', default='')
STUB_ATTRIBUTION_RATE = config('STUB_ATTRIBUTION_RATE', default=str(1 if DEV else 0), parser=float)
STUB_ATTRIBUTION_MAX_LEN = config('STUB_ATTRIBUTION_MAX_LEN', default='600', parser=int)


# via http://stackoverflow.com/a/6556951/107114
def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    try:
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                    continue

                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
        return 'localhost'
    except IOError:
        return 'localhost'


FIREFOX_MOBILE_SYSREQ_URL = 'https://support.mozilla.org/kb/will-firefox-work-my-mobile-device'

MOZILLA_LOCATION_SERVICES_KEY = 'a9b98c12-d9d5-4015-a2db-63536c26dc14'

DEAD_MANS_SNITCH_URL = config('DEAD_MANS_SNITCH_URL', default='')

SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        release=config('GIT_SHA', default=''),
        server_name=".".join(x for x in [APP_NAME, CLUSTER_NAME] if x),
        integrations=[DjangoIntegration()],
    )

# Django-CSP
CSP_DEFAULT_SRC = ["'self'", '*.mozilla.net', '*.mozilla.org', '*.mozilla.com']
EXTRA_CSP_DEFAULT_SRC = config('CSP_DEFAULT_SRC', parser=ListOf(str), default='')
if EXTRA_CSP_DEFAULT_SRC:
    CSP_DEFAULT_SRC += EXTRA_CSP_DEFAULT_SRC

CSP_IMG_SRC = CSP_DEFAULT_SRC + [
    'data:',
    'mozilla.org',
    'www.googletagmanager.com',
    'www.google-analytics.com',
    'adservice.google.com',
    'adservice.google.de',
    'adservice.google.dk',
    'creativecommons.org',
    'cdn-3.convertexperiments.com',
    'logs.convertexperiments.com',
]
CSP_SCRIPT_SRC = CSP_DEFAULT_SRC + [
    # TODO fix things so that we don't need this
    "'unsafe-inline'",
    # TODO snap.svg.js passes a string to Function() which is
    # blocked without unsafe-eval. Find a way to remove that.
    "'unsafe-eval'",
    'www.googletagmanager.com',
    'www.google-analytics.com',
    'tagmanager.google.com',
    'www.youtube.com',
    's.ytimg.com',
    'cdn-3.convertexperiments.com',
    'app.convert.com',
    'data.track.convertexperiments.com',
    '1003350.track.convertexperiments.com',
    '1003343.track.convertexperiments.com',
]
CSP_STYLE_SRC = CSP_DEFAULT_SRC + [
    # TODO fix things so that we don't need this
    "'unsafe-inline'",
    'app.convert.com',
]
CSP_CHILD_SRC = CSP_DEFAULT_SRC + [
    'www.googletagmanager.com',
    'www.google-analytics.com',
    'www.youtube-nocookie.com',
    'trackertest.org',  # mozilla service for tracker detection
    'www.surveygizmo.com',
    'accounts.firefox.com',
    'accounts.firefox.com.cn',
    'www.youtube.com',
]
CSP_CONNECT_SRC = CSP_DEFAULT_SRC + [
    'www.googletagmanager.com',
    'www.google-analytics.com',
    'logs.convertexperiments.com',
    '1003350.metrics.convertexperiments.com',
    '1003343.metrics.convertexperiments.com',
    'sentry.prod.mozaws.net',
    FXA_ENDPOINT,
    FXA_ENDPOINT_MOZILLAONLINE,
]
CSP_REPORT_ONLY = config('CSP_REPORT_ONLY', default='false', parser=bool)
CSP_REPORT_URI = config('CSP_REPORT_URI', default='') or None

CSP_EXTRA_FRAME_SRC = config('CSP_EXTRA_FRAME_SRC', default='', parser=ListOf(str))
if CSP_EXTRA_FRAME_SRC:
    CSP_CHILD_SRC += tuple(CSP_EXTRA_FRAME_SRC)

# support older browsers (mainly Safari)
CSP_FRAME_SRC = CSP_CHILD_SRC

# Bug 1331069 - Double Click tracking pixel for download page.
AVAILABLE_TRACKING_PIXELS = {
    'doubleclick': ('https://ad.doubleclick.net/ddm/activity/src=6417015;type=deskt0;cat=mozil0;dc_lat=;dc_rdid=;'
                    'tag_for_child_directed_treatment=;tfua=;npa=;ord=1'),
}
ENABLED_PIXELS = config('ENABLED_PIXELS', default='doubleclick', parser=ListOf(str))
TRACKING_PIXELS = [AVAILABLE_TRACKING_PIXELS[x] for x in ENABLED_PIXELS if x in AVAILABLE_TRACKING_PIXELS]

if config('SWITCH_TRACKING_PIXEL', default=str(DEV), parser=bool):
    if 'doubleclick' in ENABLED_PIXELS:
        CSP_IMG_SRC += ('ad.doubleclick.net',)

# Bug 1345467: Funnelcakes are now explicitly configured in the environment.
# Set experiment specific variables like the following:
#
# FUNNELCAKE_103_PLATFORMS=win,win64
# FUNNELCAKE_103_LOCALES=de,fr,en-US
#
# where "103" in the variable name is the funnelcake ID.

# Issue 7508 - Convert.com experiment sandbox
CONVERT_PROJECT_ID = ('10039-1003350' if DEV else '10039-1003343')
