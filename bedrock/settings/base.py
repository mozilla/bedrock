# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import platform
import sys
from os.path import abspath

from django.utils.functional import lazy

import dj_database_url
from decouple import Csv, config
from pathlib2 import Path

from .static_media import PIPELINE_CSS, PIPELINE_JS  # noqa


# ROOT path of the project. A pathlib.Path object.
ROOT_PATH = Path(__file__).resolve().parents[2]
ROOT = str(ROOT_PATH)


def path(*args):
    return abspath(str(ROOT_PATH.joinpath(*args)))


# Is this a dev instance?
DEV = config('DEV', cast=bool, default=False)
PROD = config('PROD', cast=bool, default=False)

DEBUG = config('DEBUG', cast=bool, default=False)

DATABASES = {
    'default': dj_database_url.parse('sqlite:///bedrock.db'),
}

CACHES = config(
    'CACHES',
    cast=json.loads,
    default=json.dumps(
        {'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'translations'}}))

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

USE_ETAGS = config('USE_ETAGS', default=not DEBUG, cast=bool)

# just here so Django doesn't complain
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

# Use Ship It as the source for product_details
PROD_DETAILS_URL = config('PROD_DETAILS_URL',
                          default='https://product-details.mozilla.org/1.0/')

# Tells the product_details module where to find our local JSON files.
# This ultimately controls how LANGUAGES are constructed.
PROD_DETAILS_CACHE_NAME = 'product-details'
PROD_DETAILS_CACHE_TIMEOUT = 60 * 15  # 15 min
default_pdstorage = 'PDDatabaseStorage' if PROD else 'PDFileStorage'
PROD_DETAILS_STORAGE = config('PROD_DETAILS_STORAGE',
                              default='product_details.storage.' + default_pdstorage)
# path into which to clone the p-d json repo
PROD_DETAILS_JSON_REPO_PATH = config('PROD_DETAILS_JSON_REPO_PATH',
                                     default=path('product_details_json'))
PROD_DETAILS_JSON_REPO_URI = config('PROD_DETAILS_JSON_REPO_URI',
                                    default='https://github.com/mozilla/product-details-json.git')
# path to updated p-d data for testing before loading into DB
PROD_DETAILS_TEST_DIR = str(Path(PROD_DETAILS_JSON_REPO_PATH).joinpath('product-details'))
# if the repo is cloned it will be most up-to-date
if Path(PROD_DETAILS_TEST_DIR).is_dir():
    PROD_DETAILS_DIR = PROD_DETAILS_TEST_DIR

# Accepted locales
PROD_LANGUAGES = ('ach', 'af', 'an', 'ar', 'as', 'ast', 'az', 'azz', 'be', 'bg',
                  'bn-BD', 'bn-IN', 'br', 'bs', 'ca', 'cak', 'cs',
                  'cy', 'da', 'de', 'dsb', 'el', 'en-GB', 'en-US',
                  'en-ZA', 'eo', 'es-AR', 'es-CL', 'es-ES', 'es-MX', 'et',
                  'eu', 'fa', 'ff', 'fi', 'fr', 'fy-NL', 'ga-IE', 'gd',
                  'gl', 'gn', 'gu-IN', 'he', 'hi-IN', 'hr', 'hsb',
                  'hu', 'hy-AM', 'ia', 'id', 'is', 'it', 'ja', 'ja-JP-mac',
                  'ka', 'kab', 'kk', 'km', 'kn', 'ko', 'lij', 'lt', 'ltg', 'lv',
                  'mai', 'mk', 'ml', 'mr', 'ms', 'my', 'nb-NO', 'ne-NP', 'nl',
                  'nn-NO', 'oc', 'or', 'pa-IN', 'pl', 'pt-BR', 'pt-PT',
                  'rm', 'ro', 'ru', 'si', 'sk', 'sl', 'son', 'sq',
                  'sr', 'sv-SE', 'ta', 'te', 'th', 'tr', 'trs', 'uk', 'ur',
                  'uz', 'vi', 'xh', 'zh-CN', 'zh-TW', 'zu')

LOCALES_PATH = ROOT_PATH / 'locale'
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
    'firefox/releases/system_requirements.html',
    'mozorg/credits.html',
    'mozorg/about/forums.html',
    'security/advisory.html',
    'security/advisories.html',
    'security/product-advisories.html',
    'security/known-vulnerabilities.html',
    'thunderbird/releases/beta-notes.html',
    'thunderbird/releases/release-notes.html',
    'thunderbird/releases/system_requirements.html',
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
    for groupid in groups.keys():
        if groupid in langs:
            groups[groupid].append(groupid)

    # exclude groups with a single member
    return {gid: glist for gid, glist in groups.iteritems() if len(glist) > 1}


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
DOTLANG_CACHE = 600

DOTLANG_FILES = ['main', 'download_button']

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
    'csp-violation-capture',
    'country-code.json',
]

# Pages that we don't want to be indexed by search engines.
# Only impacts sitemap generator. If you need to disallow indexing of
# specific URLs, add them to mozorg/templates/mozorg/robots.txt.
NOINDEX_URLS = [
    r'^(404|500)/',
    r'^contribute/(embed|event)/',
    r'^csp-violation-capture',
    r'^firefox/sms/sent/',
    r'^firefox/unsupported/',
    r'^firefox/send-to-device-post',
    r'^firefox/feedback',
    r'^firefox/stub_attribution_code/',
    r'^.+/tracking-protection/start/$',
    r'^.+/(firstrun|whatsnew)/$',
    r'^l10n_example/',
    r'^m/',
    r'^newsletter/(confirm|existing|hacks\.mozilla\.org|recovery|updated)/',
    r'/system-requirements/$',
    r'.*/(firstrun|thanks)/$',
    r'^readiness/$',
    r'^healthz(-cron)?/$',
    r'^country-code\.json$',
    # exclude redirects
    r'^foundation/annualreport/$'
    r'^firefox/notes/$'
    r'^teach/$'
    r'^thunderbird/(release)?notes/$'
    r'^about/legal/impressum/$',
    r'^security/announce/',
    r'^etc/',
]

# Pages we do want indexed but don't show up in automated URL discovery
# or are only available in a non-default locale
EXTRA_INDEX_URLS = [
    '/de/privacy/firefox-klar/',
    '/de/about/legal/impressum/',
]

# Pages that have different URLs for different locales, e.g.
#   'firefox/private-browsing/': {
#       'en-US': '/firefox/features/private-browsing/',
#   },
ALT_CANONICAL_PATHS = {}

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', cast=Csv(),
    default='www.mozilla.org,www.ipv6.mozilla.org,www.allizom.org')
ALLOWED_CIDR_NETS = config('ALLOWED_CIDR_NETS', default='', cast=Csv())

# The canonical, production URL without a trailing slash
CANONICAL_URL = 'https://www.mozilla.org'

# Make this unique, and don't share it with anybody.
SECRET_KEY = config('SECRET_KEY', default='ssssshhhhh')

MEDIA_URL = config('MEDIA_URL', default='/user-media/')
MEDIA_ROOT = config('MEDIA_ROOT', default=path('media'))
STATIC_URL = config('STATIC_URL', default='/media/')
STATIC_ROOT = config('STATIC_ROOT', default=path('static'))
STATICFILES_STORAGE = ('pipeline.storage.NonPackagingPipelineStorage' if DEBUG else
                       'bedrock.base.pipeline_storage.ManifestPipelineStorage')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
)
STATICFILES_DIRS = (
    path('media'),
)

PIPELINE = {
    'STYLESHEETS': PIPELINE_CSS,
    'JAVASCRIPT': PIPELINE_JS,
    'DISABLE_WRAPPER': True,
    'SHOW_ERRORS_INLINE': False,
    'COMPILERS': (
        'pipeline.compilers.less.LessCompiler',
        'pipeline.compilers.sass.SASSCompiler',
    ),
    'SASS_BINARY': config('PIPELINE_SASS_BINARY',
                          default=path('node_modules', '.bin', 'node-sass')),
    'SASS_ARGUMENTS': config('PIPELINE_SASS_ARGUMENTS', default=''),
    'LESS_BINARY': config('PIPELINE_LESS_BINARY',
                          default=path('node_modules', 'less', 'bin', 'lessc')),
    'LESS_ARGUMENTS': config('PIPELINE_LESS_ARGUMENTS', default='-s'),
    'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.UglifyJSCompressor',
    'UGLIFYJS_BINARY': config('PIPELINE_UGLIFYJS_BINARY',
                              default=path('node_modules', '.bin', 'uglifyjs')),
    'UGLIFYJS_ARGUMENTS': config('PIPELINE_UGLIFYJS_ARGUMENTS', default='--support-ie8'),
    'CSS_COMPRESSOR': 'bedrock.base.pipeline_compressors.CleanCSSCompressor',
    'CLEANCSS_BINARY': config('PIPELINE_CLEANCSS_BINARY',
                              default=path('node_modules', '.bin', 'cleancss')),
    'CLEANCSS_ARGUMENTS': config('PIPELINE_CLEANCSS_ARGUMENTS', default='--compatibility ie7'),
    'PIPELINE_ENABLED': config('PIPELINE_ENABLED', not DEBUG, cast=bool),
    'PIPELINE_COLLECTOR_ENABLED': config('PIPELINE_COLLECTOR_ENABLED', not DEBUG, cast=bool),
}


def set_whitenoise_headers(headers, path, url):
    if '/fonts/' in url or '/caldata/' in url:
        cache_control = 'public, max-age={}'.format(604800)  # one week
        headers['Cache-Control'] = cache_control


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

HOSTNAME = platform.node()
DEIS_APP = config('DEIS_APP', default=None)
DEIS_DOMAIN = config('DEIS_DOMAIN', default=None)
ENABLE_HOSTNAME_MIDDLEWARE = config('ENABLE_HOSTNAME_MIDDLEWARE',
                                    default=bool(DEIS_APP), cast=bool)
ENABLE_VARY_NOCACHE_MIDDLEWARE = config('ENABLE_VARY_NOCACHE_MIDDLEWARE',
                                        default=True, cast=bool)
# set this to enable basic auth for the entire site
# e.g. BASIC_AUTH_CREDS="thedude:thewalrus"
BASIC_AUTH_CREDS = config('BASIC_AUTH_CREDS', default=None)

MIDDLEWARE_CLASSES = [
    'allow_cidr.middleware.AllowCIDRMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'bedrock.mozorg.middleware.MozorgRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'bedrock.mozorg.middleware.VaryNoCacheMiddleware',
    'bedrock.base.middleware.BasicAuthMiddleware',
    # must come before LocaleURLMiddleware
    'bedrock.redirects.middleware.RedirectsMiddleware',
    'bedrock.base.middleware.LocaleURLMiddleware',
    'commonware.middleware.RobotsTagHeader',
    'bedrock.mozorg.middleware.ClacksOverheadMiddleware',
    'bedrock.mozorg.middleware.HostnameMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'bedrock.mozorg.middleware.CacheMiddleware',
]

ENABLE_CSP_MIDDLEWARE = config('ENABLE_CSP_MIDDLEWARE', default=True, cast=bool)
if ENABLE_CSP_MIDDLEWARE:
    MIDDLEWARE_CLASSES.append('csp.middleware.CSPMiddleware')

INSTALLED_APPS = (
    'cronjobs',  # for ./manage.py cron * cmd line tasks

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
    'django_statsd',
    'pagedown',
    'pipeline',
    'localflavor',
    'django_jinja',
    'raven.contrib.django.raven_compat',
    'watchman',

    # Local apps
    'bedrock.base',
    'bedrock.firefox',
    'bedrock.foundation',
    'bedrock.grants',
    'bedrock.legal',
    'bedrock.mozorg',
    'bedrock.newsletter',
    'bedrock.press',
    'bedrock.privacy',
    'bedrock.styleguide',
    'bedrock.teach',
    'bedrock.externalfiles',
    'bedrock.security',
    'bedrock.events',
    'bedrock.releasenotes',
    'bedrock.thunderbird',
    'bedrock.shapeoftheweb',
    'bedrock.utils',
    'bedrock.wordpress',
    'bedrock.sitemaps',
    'bedrock.etc',
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
    '/plugincheck/',
    '/firefox/',
    '/contribute/',
    '/about/',
    '/contact/',
    '/thunderbird/',
    '/newsletter/',
    '/privacy/',
    '/foundation/',
    '/teach/',
)

# Sessions
#
# By default, be at least somewhat secure with our session cookies.
SESSION_COOKIE_HTTPONLY = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# legacy setting. backward compat.
DISABLE_SSL = config('DISABLE_SSL', default=True, cast=bool)
# SecurityMiddleware settings
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default='0', cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=True, cast=bool)
SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=bool)
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=not DISABLE_SSL, cast=bool)
SECURE_REDIRECT_EXEMPT = [
    r'^readiness/$',
    r'^healthz(-cron)?/$',
]
if config('USE_SECURE_PROXY_HEADER', default=SECURE_SSL_REDIRECT, cast=bool):
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
                'pipeline.jinja2.PipelineExtension',
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

EVENTS_ICAL_FEEDS = (
    'https://reps.mozilla.org/events/period/future/ical/',
    'https://www.google.com/calendar/ical/mozilla.com_l9g7ie050ngr3g4qv6bgiinoig'
    '%40group.calendar.google.com/public/basic.ics',
)

# Twitter accounts to retrieve tweets with the API
TWITTER_ACCOUNTS = (
    'firefox',
    'firefox_es',
    'firefoxbrasil',
    'mozstudents',
)
# Add optional parameters specific to accounts here
# e.g. 'firefox': {'exclude_replies': False}
TWITTER_ACCOUNT_OPTS = {}
TWITTER_APP_KEYS = {
    'consumer_key': config('TWITTER_CONSUMER_KEY', default=''),
    'consumer_secret': config('TWITTER_CONSUMER_SECRET', default=''),
    'access_token': config('TWITTER_ACCESS_TOKEN', default=''),
    'access_token_secret': config('TWITTER_ACCESS_TOKEN_SECRET', default=''),
}

# Contribute numbers
# TODO: automate these
CONTRIBUTE_NUMBERS = {
    'num_mozillians': 10554,
    'num_languages': 87,
}

BASKET_URL = config('BASKET_URL', default='https://basket.mozilla.org')
BASKET_API_KEY = config('BASKET_API_KEY', default='')
BASKET_TIMEOUT = config('BASKET_TIMEOUT', cast=int, default=10)

BOUNCER_URL = config('BOUNCER_URL', default='https://download.mozilla.org/')

# This prefixes /b/ on all URLs generated by `reverse` so that links
# work on the dev site while we have a mix of Python/PHP
FORCE_SLASH_B = False

# reCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='')
RECAPTCHA_USE_SSL = config('RECAPTCHA_USE_SSL', cast=bool, default=True)

# Use a message storage mechanism that doesn't need a database.
# This can be changed to use session once we do add a database.
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'


def lazy_email_backend():
    'Needed in case DEBUG is enabled in local.py instead of environment variable'
    from django.conf import settings
    return ('django.core.mail.backends.console.EmailBackend' if settings.DEBUG else
            'django.core.mail.backends.smtp.EmailBackend')


EMAIL_BACKEND = config('EMAIL_BACKEND', default=lazy(lazy_email_backend, str)())
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX', default='[bedrock] ')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Google Analytics
GA_ACCOUNT_CODE = ''

EXTERNAL_FILES_PATH = config('EXTERNAL_FILES_PATH', default=path('community_data'))
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

# Used on the newsletter preference center, included in the "interests" section.
OTHER_NEWSLETTERS = [
    'firefox-desktop',
    'mobile',
    'os',
    'firefox-ios',
    'mozilla-general',
    'firefox-os',
]

# Regional press blogs map to locales
PRESS_BLOG_ROOT = 'https://blog.mozilla.org/'
PRESS_BLOGS = {
    'de': 'press-de/',
    'en-GB': 'press-uk/',
    'en-US': 'press/',
    'es-AR': 'press-latam/',
    'es-CL': 'press-latam/',
    'es-ES': 'press-es/',
    'es-MX': 'press-latam/',
    'fr': 'press-fr/',
    'it': 'press-it/',
    'pl': 'press-pl/',
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
    'bn-BD': {
        'currency': 'bdt',
        'symbol': u'৳',
        'presets': '1600,800,400,240',
        'default': '800'
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
    'en-GB': {
        'currency': 'gbp',
        'symbol': u'£',
        'presets': '40,25,15,8',
        'default': '25'
    },
    'es-AR': {
        'currency': 'ars',
        'symbol': '$',
        'presets': '1600,800,400,200',
        'default': '800'
    },
    'es-CL': {
        'currency': 'clp',
        'symbol': '$',
        'presets': '68000,34000,17000,10200',
        'default': '34000'
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
        'presets': '240,120,60,35',
        'default': '120'
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
        'presets': '4000,2000,1000,600',
        'default': '2000'
    },
    'id': {
        'currency': 'idr',
        'symbol': 'Rp',
        'presets': '270000,140000,70000,40000',
        'default': '140000'
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
        'presets': '2180,1000,550,330',
        'default': '1000'
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
        'presets': '150,100,50,30',
        'default': '100'
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
        'presets': '1000,500,250,140',
        'default': '500'
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
        'presets': '160,80,40,20',
        'default': '80'
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

# Optimize.ly project code
OPTIMIZELY_PROJECT_ID = config('OPTIMIZELY_PROJECT_ID', default='')

# Fx Accounts iframe source
FXA_IFRAME_SRC = config('FXA_IFRAME_SRC',
                        default='https://accounts.firefox.com/')

# Bug 1264843: embed FxA server in China within Fx China repack
FXA_IFRAME_SRC_MOZILLAONLINE = config('FXA_IFRAME_SRC_MOZILLAONLINE',
                                      default='https://accounts.firefox.com.cn/')

# Google Play and Apple App Store settings
from .appstores import (GOOGLE_PLAY_FIREFOX_LINK,  # noqa
                        GOOGLE_PLAY_FIREFOX_LINK_MOZILLAONLINE,  # noqa
                        APPLE_APPSTORE_FIREFOX_LINK, APPLE_APPSTORE_COUNTRY_MAP,
                        APPLE_APPSTORE_FIREFOX_FOCUS_LINK, GOOGLE_PLAY_FIREFOX_FOCUS_LINK)

# Locales that should display the 'Send to Device' widget
SEND_TO_DEVICE_LOCALES = ['de', 'en-GB', 'en-US', 'en-ZA',
                          'es-AR', 'es-CL', 'es-ES', 'es-MX',
                          'fr', 'id', 'pl', 'pt-BR', 'ru', 'zh-TW']

# country code for /country-code.json to return in dev mode
DEV_GEO_COUNTRY_CODE = config('DEV_GEO_COUNTRY_CODE', default='US')
SEND_TO_DEVICE_MESSAGE_SETS = {
    'default': {
        'sms_countries': config('STD_SMS_COUNTRIES_DEFAULT', default='US', cast=Csv()),
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
        'sms_countries': config('STD_SMS_COUNTRIES_ANDROID', default='US', cast=Csv()),
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
        'sms_countries': config('STD_SMS_COUNTRIES_DESKTOP', default='US', cast=Csv()),
        'sms': {
            'all': 'mobile-heartbeat',
        },
        'email': {
            'all': 'download-firefox-mobile-reco',
        }
    },
    'fx-50-whatsnew': {
        'sms_countries': config('STD_SMS_COUNTRIES_WHATSNEW50', default='US', cast=Csv()),
        'sms': {
            'all': 'whatsnewfifty',
        },
        'email': {
            'all': 'download-firefox-mobile-whatsnew',
        }
    }
}

RELEASE_NOTES_PATH = config('RELEASE_NOTES_PATH', default=path('release_notes'))
RELEASE_NOTES_REPO = config('RELEASE_NOTES_REPO', default='https://github.com/mozilla/release-notes.git')
RELEASE_NOTES_BRANCH = config('RELEASE_NOTES_BRANCH', default='master')

MOFO_SECURITY_ADVISORIES_PATH = config('MOFO_SECURITY_ADVISORIES_PATH',
                                       default=path('mofo_security_advisories'))
MOFO_SECURITY_ADVISORIES_REPO = config('MOFO_SECURITY_ADVISORIES_REPO',
                                       default='https://github.com/mozilla/'
                                               'foundation-security-advisories.git')
MOFO_SECURITY_ADVISORIES_BRANCH = config('MOFO_SECURITY_ADVISORIES_BRANCH', default='master')

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/([a-zA-Z-]+/)?(shapeoftheweb|newsletter)/'

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

TABLEAU_DB_URL = config('TABLEAU_DB_URL', default=None)

ADMINS = MANAGERS = config('ADMINS', cast=json.loads,
                           default='[]')

GTM_CONTAINER_ID = config('GTM_CONTAINER_ID', default='')
GMAP_API_KEY = config('GMAP_API_KEY', default='')
STUB_ATTRIBUTION_HMAC_KEY = config('STUB_ATTRIBUTION_HMAC_KEY', default='')
STUB_ATTRIBUTION_RATE = config('STUB_ATTRIBUTION_RATE', default=1 if DEV else 0, cast=float)

STATSD_CLIENT = config('STATSD_CLIENT', default='django_statsd.clients.normal')
STATSD_HOST = config('STATSD_HOST', default='127.0.0.1')
STATSD_PORT = config('STATSD_PORT', cast=int, default=8125)
STATSD_PREFIX = config('STATSD_PREFIX', default='bedrock')

FIREFOX_MOBILE_SYSREQ_URL = 'https://support.mozilla.org/kb/will-firefox-work-my-mobile-device'

MOZILLA_LOCATION_SERVICES_KEY = 'a9b98c12-d9d5-4015-a2db-63536c26dc14'

DEAD_MANS_SNITCH_URL = config('DEAD_MANS_SNITCH_URL', default=None)

RAVEN_CONFIG = {
    'dsn': config('SENTRY_DSN', None),
    'site': '.'.join(x for x in [DEIS_APP, DEIS_DOMAIN] if x),
    'release': config('GIT_SHA', None),
}

# Django-CSP
CSP_DEFAULT_SRC = (
    "'self'",
    '*.mozilla.net',
    '*.mozilla.org',
    '*.mozilla.com',
)
CSP_IMG_SRC = CSP_DEFAULT_SRC + (
    'data:',
    '*.optimizely.com',
    'www.googletagmanager.com',
    'www.google-analytics.com',
    'creativecommons.org',
)
CSP_SCRIPT_SRC = CSP_DEFAULT_SRC + (
    # TODO fix things so that we don't need this
    "'unsafe-inline'",
    # TODO snap.svg.js passes a string to Function() which is
    # blocked without unsafe-eval. Find a way to remove that.
    "'unsafe-eval'",
    '*.optimizely.com',
    'optimizely.s3.amazonaws.com',
    'www.googletagmanager.com',
    'www.google-analytics.com',
    'tagmanager.google.com',
    'www.youtube.com',
    's.ytimg.com',
)
CSP_STYLE_SRC = CSP_DEFAULT_SRC + (
    # TODO fix things so that we don't need this
    "'unsafe-inline'",
)
CSP_CHILD_SRC = (
    '*.optimizely.com',
    'www.googletagmanager.com',
    'www.google-analytics.com',
    'www.youtube-nocookie.com',
    'trackertest.org',  # mozilla service for tracker detection
    'www.surveygizmo.com',
    'accounts.firefox.com',
    'accounts.firefox.com.cn',
    'www.youtube.com',
)
CSP_CONNECT_SRC = CSP_DEFAULT_SRC + (
    '*.optimizely.com',
    'www.googletagmanager.com',
    'www.google-analytics.com',
)
CSP_REPORT_ONLY = config('CSP_REPORT_ONLY', default=False, cast=bool)
CSP_REPORT_ENABLE = config('CSP_REPORT_ENABLE', default=False, cast=bool)
if CSP_REPORT_ENABLE:
    CSP_REPORT_URI = config('CSP_REPORT_URI', default='/csp-violation-capture')

CSP_EXTRA_FRAME_SRC = config('CSP_EXTRA_FRAME_SRC', default='', cast=Csv())
if CSP_EXTRA_FRAME_SRC:
    CSP_CHILD_SRC += tuple(CSP_EXTRA_FRAME_SRC)

# support older browsers (mainly Safari)
CSP_FRAME_SRC = CSP_CHILD_SRC

# Bug 1331069 - Double Click tracking pixel for download page.
AVAILABLE_TRACKING_PIXELS = {
    'doubleclick': ('https://ad.doubleclick.net/ddm/activity/src=6417015;type=deskt0;cat=mozil0;dc_lat=;dc_rdid=;'
                    'tag_for_child_directed_treatment=;ord=1;num=1?&_dc_ck=try'),
}
ENABLED_PIXELS = config('ENABLED_PIXELS', default='doubleclick', cast=Csv())
TRACKING_PIXELS = [AVAILABLE_TRACKING_PIXELS[x] for x in ENABLED_PIXELS if x in AVAILABLE_TRACKING_PIXELS]

if config('SWITCH_TRACKING_PIXEL', default=DEV, cast=bool):
    if 'doubleclick' in ENABLED_PIXELS:
        CSP_IMG_SRC += ('ad.doubleclick.net',)

# Bug 1345467: Funnelcakes are now explicitly configured in the environment.
# Set experiment specific variables like the following:
#
# FUNNELCAKE_103_PLATFORMS=win,win64
# FUNNELCAKE_103_LOCALES=de,fr,en-US
#
# where "103" in the variable name is the funnelcake ID.
