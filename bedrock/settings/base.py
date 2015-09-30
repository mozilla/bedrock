# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import logging
from os.path import abspath

from django.utils.functional import lazy
from django.utils.http import urlquote

import dj_database_url
from decouple import Csv, config
from pathlib import Path

from .static_media import PIPELINE_CSS, PIPELINE_JS  # noqa


# ROOT path of the project. A pathlib.Path object.
ROOT_PATH = Path(__file__).resolve().parents[2]
ROOT = str(ROOT_PATH)


def path(*args):
    return abspath(str(ROOT_PATH.joinpath(*args)))


# Is this a dev instance?
DEV = config('DEV', cast=bool, default=False)

DEBUG = TEMPLATE_DEBUG = config('DEBUG', cast=bool, default=False)

# Production uses MySQL, but Sqlite should be sufficient for local development.
# Our CI server tests against MySQL.
DATABASES = config(
    'DATABASES',
    cast=json.loads,
    default=json.dumps(
        {'default': config('DATABASE_URL',
                           cast=dj_database_url.parse,
                           default='sqlite:///bedrock.db')}))

SLAVE_DATABASES = config('SLAVE_DATABASES', cast=Csv(), default=',')
DATABASE_ROUTERS = ('multidb.PinningMasterSlaveRouter',)

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

# Site ID is used by Django's Sites framework.
SITE_ID = 1

# Logging
LOG_LEVEL = config('LOG_LEVEL', cast=int, default=logging.INFO)
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

# Gettext text domain
TEXT_DOMAIN = 'messages'
STANDALONE_DOMAINS = [TEXT_DOMAIN, 'javascript']
TOWER_KEYWORDS = {'_lazy': None}
TOWER_ADD_HEADERS = True
TOWER_INSTALL_JINJA_TRANSLATIONS = False

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

# Tells the product_details module where to find our local JSON files.
# This ultimately controls how LANGUAGES are constructed.
PROD_DETAILS_DIR = path('lib', 'product_details_json')
PROD_DETAILS_CACHE_NAME = 'product-details'
PROD_DETAILS_CACHE_TIMEOUT = 60 * 15  # 15 min

# Accepted locales
PROD_LANGUAGES = ('ach', 'af', 'an', 'ar', 'as', 'ast', 'az', 'be', 'bg',
                  'bn-BD', 'bn-IN', 'br', 'brx', 'bs', 'ca', 'cs', 'cy',
                  'da', 'de', 'dsb', 'ee', 'el', 'en-GB', 'en-US', 'en-ZA',
                  'eo', 'es-AR', 'es-CL', 'es-ES', 'es-MX', 'et', 'eu',
                  'fa', 'ff', 'fi', 'fr', 'fy-NL', 'ga-IE', 'gd', 'gl',
                  'gu-IN', 'ha', 'he', 'hi-IN', 'hr', 'hsb', 'hu',
                  'hy-AM', 'id', 'ig', 'is', 'it', 'ja', 'ja-JP-mac',
                  'ka', 'kk', 'km', 'kn', 'ko', 'lij', 'ln', 'lt', 'lv',
                  'mai', 'mk', 'ml', 'mr', 'ms', 'my', 'nb-NO', 'nl',
                  'nn-NO', 'oc', 'or', 'pa-IN', 'pl', 'pt-BR', 'pt-PT',
                  'rm', 'ro', 'ru', 'sat', 'si', 'sk', 'sl', 'son', 'sq', 'sr',
                  'sv-SE', 'sw', 'ta', 'te', 'th', 'tr', 'uk', 'ur',
                  'uz', 'vi', 'wo', 'xh', 'yo', 'zh-CN', 'zh-TW', 'zu')

LOCALES_PATH = ROOT_PATH / 'locale'


def get_dev_languages():
    try:
        return [lang.name for lang in LOCALES_PATH.iterdir()
                if lang.is_dir() and lang.name != 'templates']
    except OSError:
        # no locale dir
        return []


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
}

# Unlocalized pages are usually redirected to the English (en-US) equivalent,
# but sometimes it would be better to offer another locale as fallback. This map
# specifies such cases.
FALLBACK_LOCALES = {
    'es-AR': 'es-ES',
    'es-CL': 'es-ES',
    'es-MX': 'es-ES',
}


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
    'admin',
    'contribute.json',
    'credits',
    'gameon',
    'rna',
    'robots.txt',
    'telemetry',
    'webmaker',
    'contributor-data',
]

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', cast=Csv(),
    default='www.mozilla.org,www.ipv6.mozilla.org,www.allizom.org')

# The canonical, production URL without a trailing slash
CANONICAL_URL = 'https://www.mozilla.org'

# Make this unique, and don't share it with anybody.
SECRET_KEY = config('SECRET_KEY', default='ssssshhhhh')

TEMPLATE_DIRS = (
    path('locale'),
)


# has to stay a callable because tower expects that.
def JINJA_CONFIG():
    return {
        'extensions': [
            'lib.l10n_utils.template.i18n', 'jinja2.ext.do', 'jinja2.ext.with_',
            'jinja2.ext.loopcontrols', 'lib.l10n_utils.template.l10n_blocks',
            'lib.l10n_utils.template.lang_blocks',
            'jingo_markdown.extensions.MarkdownExtension',
            'pipeline.templatetags.ext.PipelineExtension',
        ],
        # Make None in templates render as ''
        'finalize': lambda x: x if x is not None else '',
        'auto_reload': True,
    }


MEDIA_URL = config('MEDIA_URL', default='/user-media/')
MEDIA_ROOT = config('MEDIA_ROOT', default=path('media'))
STATIC_URL = config('STATIC_URL', default='/media/')
STATIC_ROOT = config('STATIC_ROOT', default=path('static'))
STATICFILES_STORAGE = 'bedrock.base.storage.ManifestPipelineStorage'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
)
STATICFILES_DIRS = (
    path('media'),
)

JINGO_EXCLUDE_APPS = (
    'admin',
    'registration',
    'rest_framework',
    'rna',
    'waffle',
)

PIPELINE_DISABLE_WRAPPER = True
PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)
PIPELINE_LESS_BINARY = config('PIPELINE_LESS_BINARY',
                              default=path('node_modules', 'less', 'bin', 'lessc'))
PIPELINE_LESS_ARGUMENTS = config('PIPELINE_LESS_ARGUMENTS', default='-s')
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'
PIPELINE_UGLIFYJS_BINARY = config('PIPELINE_UGLIFYJS_BINARY',
                                  default=path('node_modules', 'uglify-js', 'bin', 'uglifyjs'))
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
PIPELINE_CSSMIN_BINARY = config('PIPELINE_CSSMIN_BINARY',
                                default=path('node_modules', 'cssmin', 'bin', 'cssmin'))

WHITENOISE_ROOT = config('WHITENOISE_ROOT', default=path('root_files'))
WHITENOISE_MAX_AGE = 6 * 60 * 60  # 6 hours

PROJECT_MODULE = 'bedrock'

ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS = {
    'messages': [
        ('%s/**.py' % PROJECT_MODULE,
            'tower.extract_tower_python'),
        ('%s/**/templates/**.html' % PROJECT_MODULE,
            'tower.extract_tower_template'),
        ('%s/**/templates/**.js' % PROJECT_MODULE,
            'tower.extract_tower_template'),
        ('%s/**/templates/**.jsonp' % PROJECT_MODULE,
            'tower.extract_tower_template'),
    ],
}

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'bedrock.mozorg.middleware.MozorgRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    # must come before LocaleURLMiddleware
    'bedrock.redirects.middleware.RedirectsMiddleware',
    'bedrock.tabzilla.middleware.TabzillaLocaleURLMiddleware',
    'commonware.middleware.RobotsTagHeader',
    'bedrock.mozorg.middleware.ClacksOverheadMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'bedrock.mozorg.middleware.CacheMiddleware',
    'dnt.middleware.DoNotTrackMiddleware',
    'lib.l10n_utils.middleware.FixLangFileTranslationsMiddleware',
    'bedrock.mozorg.middleware.ConditionalAuthMiddleware',
    'bedrock.mozorg.middleware.CrossOriginResourceSharingMiddleware',
)

AUTHENTICATED_URL_PREFIXES = ('/admin/', '/rna/')

INSTALLED_APPS = (
    'cronjobs',  # for ./manage.py cron * cmd line tasks

    # Django contrib apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.messages',

    # Third-party apps, patches, fixes
    'commonware.response.cookies',
    'django_nose',

    # L10n
    'tower',  # for ./manage.py extract
    'product_details',

    # third-party apps
    'jingo_markdown',
    # 'jingo_minify',
    'django_statsd',
    'pagedown',
    'rest_framework',
    'waffle',
    'pipeline',
    'localflavor',

    # Local apps
    'bedrock.base',
    'bedrock.lightbeam',
    'bedrock.firefox',
    'bedrock.foundation',
    'bedrock.gigabit',
    'bedrock.grants',
    'bedrock.legal',
    'bedrock.mozorg',
    'bedrock.newsletter',
    'bedrock.persona',
    'bedrock.press',
    'bedrock.privacy',
    'bedrock.redirects',
    'bedrock.research',
    'bedrock.styleguide',
    'bedrock.tabzilla',
    'bedrock.facebookapps',
    'bedrock.externalfiles',
    'bedrock.security',
    'bedrock.events',
    'bedrock.releasenotes',
    'bedrock.thunderbird',
    'bedrock.shapeoftheweb',

    # libs
    'django_extensions',
    'lib.l10n_utils',
    'captcha',
    'rna',
)

# Sessions
#
# By default, be at least somewhat secure with our session cookies.
SESSION_COOKIE_HTTPONLY = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

LOCALE_PATHS = (
    str(LOCALES_PATH),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'jingo.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.csrf',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'bedrock.base.context_processors.i18n',
    'bedrock.base.context_processors.globals',
    'bedrock.mozorg.context_processors.canonical_path',
    'bedrock.mozorg.context_processors.contrib_numbers',
    'bedrock.mozorg.context_processors.current_year',
    'bedrock.mozorg.context_processors.funnelcake_param',
    'bedrock.mozorg.context_processors.facebook_locale',
    'bedrock.firefox.context_processors.latest_firefox_versions',
    'jingo_minify.helpers.build_ids',
)

FEEDS = {
    'mozilla': 'https://blog.mozilla.org/feed/'
}
EVENTS_ICAL_FEEDS = (
    'https://reps.mozilla.org/events/period/future/ical/',
    'https://www.google.com/calendar/ical/mozilla.com_l9g7ie050ngr3g4qv6bgiinoig%40group.calendar.google.com/public/basic.ics',
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
TWITTER_APP_KEYS = config('TWITTER_APP_KEYS', cast=json.loads, default='{}')

# Contribute numbers
# TODO: automate these
CONTRIBUTE_NUMBERS = {
    'num_mozillians': 10554,
    'num_languages': 87,
}

BASKET_URL = config('BASKET_URL', default='https://basket.mozilla.org')
BASKET_API_KEY = config('BASKET_API_KEY', default='')
BASKET_TIMEOUT = config('BASKET_TIMEOUT', cast=int, default=10)

# This prefixes /b/ on all URLs generated by `reverse` so that links
# work on the dev site while we have a mix of Python/PHP
FORCE_SLASH_B = False

# reCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY', default='')
RECAPTCHA_USE_SSL = config('RECAPTCHA_USE_SSL', cast=bool, default=True)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

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
EMAIL_SUBJECT_PREFIX = config('EMAIL_SUBJECT_PREFIX', default='[bedrock] ')


AURORA_STUB_INSTALLER = False

# special value that means all locales are enabled.
STUB_INSTALLER_ALL = '__ALL__'
# values should be a list of lower case locales per platform for which a
# stub installer is available. Hopefully this can all be moved to bouncer.
STUB_INSTALLER_LOCALES = {
    'win': STUB_INSTALLER_ALL,
    'osx': [],
    'linux': [],
}

# Google Analytics
GA_ACCOUNT_CODE = ''

# Files from The Web[tm]
EXTERNAL_FILES = {
    'credits': {
        'url': 'https://svn.mozilla.org/projects/mozilla.org/trunk/credits/names.csv',
        'type': 'bedrock.mozorg.credits.CreditsFile',
        'name': 'credits.csv',
    },
    'forums': {
        'url': 'https://svn.mozilla.org/projects/mozilla.org/trunk/about/forums/raw-ng-list.txt',
        'type': 'bedrock.mozorg.forums.ForumsFile',
        'name': 'forums.txt',
    },
}

FACEBOOK_LOCALES = ['en-US', 'es-ES', 'pt-BR', 'id', 'de']
FACEBOOK_PAGE_NAMESPACE = 'DUMMY_PAGE_NAMESPACE'
FACEBOOK_APP_ID = 'DUMMY_APP_ID'

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


# FACEBOOK_TAB_URL is lazily evaluated because it depends on the namespace
# and app ID settings in local settings.
def facebook_tab_url_lazy():
    from django.conf import settings
    return '//www.facebook.com/{page}/app_{id}'.format(
        page=settings.FACEBOOK_PAGE_NAMESPACE, id=settings.FACEBOOK_APP_ID)
FACEBOOK_TAB_URL = lazy(facebook_tab_url_lazy, str)()

# Prefix for media. No trailing slash.
# e.g. '//mozorg.cdn.mozilla.net'
CDN_BASE_URL = config('CDN_BASE_URL', default='')

CSRF_FAILURE_VIEW = 'bedrock.mozorg.views.csrf_failure'

from .newsletters import (DEFAULT_NEWSLETTERS, OTHER_NEWSLETTERS,  # noqa
                          MARKETPLACE_NEWSLETTERS)

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

FXOS_PRESS_BLOG_LINKS = {
    'en': 'https://blog.mozilla.org/press/category/firefox-os/',
    'de': 'https://blog.mozilla.org/press-de/category/firefox-os/',
    'es-ES': 'https://blog.mozilla.org/press-es/category/firefox-os/',
    'es': 'https://blog.mozilla.org/press-latam/category/firefox-os/',
    'fr': 'https://blog.mozilla.org/press-fr/category/firefox-os/',
    'it': 'https://blog.mozilla.org/press-it/category/firefox-os/',
    'pb-BR': 'https://blog.mozilla.org/press-br/category/firefox-os/',
    'pl': 'https://blog.mozilla.org/press-pl/category/firefox-os/',
}

MOBILIZER_LOCALE_LINK = {
    'en-US': 'https://wiki.mozilla.org/FirefoxOS/Community/Mobilizers',
    'hu': 'https://www.facebook.com/groups/mobilizerhungary/',
    'pt-BR': 'https://wiki.mozilla.org/Mobilizers/MobilizerBrasil/',
    'pl': 'https://wiki.mozilla.org/Mobilizers/MobilizerPolska/',
    'gr': 'https://wiki.mozilla.org/Mobilizer/MobilizerGreece/',
    'cs': 'https://wiki.mozilla.org/Mobilizer/MobilizerCzechRepublic/'
}

DONATE_SPANISH_LINK = ('https://sendto.mozilla.org/page/contribute/givenow-seq-es?'
    'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
    '&utm_source=mozilla.org&utm_medium=referral&utm_content=mozillaorg_ES')

DONATE_LOCALE_LINK = {
    'default': (
        'https://sendto.mozilla.org/page/contribute/Give-Now?source={source}'
    ),
    'en-US': (
        'https://sendto.mozilla.org/page/contribute/givenow-seq?'
        'preset=2&source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content={source}'
    ),
    'cs': (
        'https://sendto.mozilla.org/page/content/paypal-donate-czk/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_CZK'
    ),
    'da': (
        'https://sendto.mozilla.org/page/content/paypal-donate-dkk/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source={source}&utm_medium=referral&utm_content=PPcurrency_DKK'
    ),
    'de': (
        'https://sendto.mozilla.org/page/contribute/givenow-seq-de?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=mozillaorg_DE'
    ),
    'es-AR': DONATE_SPANISH_LINK,
    'es-CL': DONATE_SPANISH_LINK,
    'es-ES': DONATE_SPANISH_LINK,
    'es-MX': DONATE_SPANISH_LINK,
    'fr': (
        'https://sendto.mozilla.org/page/contribute/givenow-seq-fr?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=mozillaorg_FR'
    ),
    'he': (
        'https://sendto.mozilla.org/page/content/paypal-donate-ils/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_ILS'
    ),
    'hu': (
        'https://sendto.mozilla.org/page/content/paypal-donate-huf/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_HUF'
    ),
    'ja': (
        'https://sendto.mozilla.org/page/content/paypal-donate-jpy/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_JPY'
    ),
    'nb-NO': (
        'https://sendto.mozilla.org/page/content/paypal-donate-nok/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_NOK'
    ),
    'nn-NO': (
        'https://sendto.mozilla.org/page/content/paypal-donate-nok/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_NOK'
    ),
    'pl': (
        'https://sendto.mozilla.org/page/content/paypal-donate-pln/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_PLN'
    ),
    'pt-BR': (
        'https://sendto.mozilla.org/page/contribute/givenow-seq-pt-br?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=mozillaorg_PTBR'
    ),
    'ru': (
        'https://sendto.mozilla.org/page/content/paypal-donate-rub/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_RUB'
    ),
    'sv-SE': (
        'https://sendto.mozilla.org/page/content/paypal-donate-sek/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_SEK'
    ),
    'th': (
        'https://sendto.mozilla.org/page/content/paypal-donate-thb/?'
        'source={source}&ref=EOYFR2014&utm_campaign=EOYFR2014'
        '&utm_source=mozilla.org&utm_medium=referral&utm_content=PPcurrency_THB'
    ),
}

# Official Firefox Twitter accounts
FIREFOX_TWITTER_ACCOUNTS = {
    'en-US': 'https://twitter.com/firefox',
    'es-ES': 'https://twitter.com/firefox_es',
    'pt-BR': 'https://twitter.com/firefoxbrasil',
}

# Twitter accounts to display on homepage per locale
HOMEPAGE_TWITTER_ACCOUNTS = {
    'en-US': 'firefox',
    'es-AR': 'firefox_es',
    'es-CL': 'firefox_es',
    'es-ES': 'firefox_es',
    'es-MX': 'firefox_es',
    'pt-BR': 'firefoxbrasil',
}

# Mapbox token for spaces and communities pages
MAPBOX_TOKEN = config('MAPBOX_TOKEN', default='mozilla-webprod.ijaeac5j')
MAPBOX_ACCESS_TOKEN = config(
    'MAPBOX_ACCESS_TOKEN',
    default='pk.eyJ1IjoibW96aWxsYS13ZWJwcm9kIiwiYSI6Ii0xYVEtTW8ifQ.3ikA2IgKATeXStfC5wKDaQ')

# Tabzilla Information Bar default options
TABZILLA_INFOBAR_OPTIONS = 'update translation'

# Optimize.ly project code
OPTIMIZELY_PROJECT_ID = None

# Fx Accounts iframe source
# Prod, stage, dev, & demos have this set in their local.py files.
#
# For local testing:
#   - Point FXA_IFRAME_SRC to stomlinson's instance in your own local.py:
#     FXA_IFRAME_SRC = 'https://stomlinson.dev.lcip.org/'
#   - Run local server on 127.0.0.1:8111
#   - Configure Fx40+ as detailed here:
#     https://bugzilla.mozilla.org/show_bug.cgi?id=1150231#c4
#
# For demo server testing, configure Fx40+ as detailed here:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1150231#c28
FXA_IFRAME_SRC = config('FXA_IFRAME_SRC', default='')

# Link to Firefox for Android on the Google Play store with Google Analytics
# campaign parameters
GOOGLE_PLAY_FIREFOX_LINK = ('https://play.google.com/store/apps/details?' +
                            'id=org.mozilla.firefox&referrer=' +
                            urlquote('utm_source=mozilla&utm_medium=Referral&'
                                     'utm_campaign=mozilla-org'))

# Link to Firefox for iOS on the Apple App Store with Google Analytics
# campaign patameters. Each implementation should add a "ct" parameter
# for analytics.

# Note: this URL is likely to change for Fx42. See bug comment:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1196310#c18
APPLE_APPSTORE_FIREFOX_LINK = ('https://itunes.apple.com/app/apple-store/' +
                               'id989804926?pt=373246&mt=8')


# Locales that should display the 'Send to Device' widget
SEND_TO_DEVICE_LOCALES = ['de', 'en-GB', 'en-US', 'en-ZA',
                          'es-AR', 'es-CL', 'es-ES', 'es-MX',
                          'fr', 'hu', 'id', 'pl', 'pt-BR', 'ru']

# Use bedrock Gruntfile.js for live reload
USE_GRUNT_LIVERELOAD = config('USE_GRUNT_LIVERELOAD', cast=bool, default=False)

# Publishing system config
RNA = {
    'BASE_URL': config('RNA_BASE_URL', default='https://nucleus.mozilla.org/rna/'),

    # default False as temporary workaround for bug 973499
    'VERIFY_SSL_CERT': config('VERIFY_SSL_CERT', cast=bool, default=False),
}

MOFO_SECURITY_ADVISORIES_PATH = path('..', 'mofo_security_advisories')
MOFO_SECURITY_ADVISORIES_REPO = 'https://github.com/mozilla/foundation-security-advisories.git'

CORS_URLS = {
    r'^/([a-zA-Z-]+/)?shapeoftheweb': '*',
}

LOGGING = {
    'root': {
        'level': 'WARNING',
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
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

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rna.serializers.HyperlinkedModelSerializerWithPkField',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_FILTER_BACKENDS': ('rna.filters.TimestampedFilterBackend',)
}

FIREFOX_OS_FEEDS = (
    ('de', 'https://blog.mozilla.org/press-de/category/firefox-os/feed/'),
    ('en-US', 'https://blog.mozilla.org/blog/category/firefox-os/feed/'),
    ('es-ES', 'https://blog.mozilla.org/press-es/category/firefox-os/feed/'),
    ('es', 'https://blog.mozilla.org/press-latam/category/firefox-os/feed/'),
    ('fr', 'https://blog.mozilla.org/press-fr/category/firefox-os/feed/'),
    ('it', 'https://blog.mozilla.org/press-it/category/firefox-os/feed/'),
    ('pl', 'https://blog.mozilla.org/press-pl/category/firefox-os/feed/'),
    ('pt-BR', 'https://blog.mozilla.org/press-br/category/firefox-os/feed/'),
)
FIREFOX_OS_FEED_LOCALES = [feed[0] for feed in FIREFOX_OS_FEEDS]

# Bug 1133146
FIREFOX_OS_COUNTRY_VERSIONS = {
    'default': '2.0',
    'AR': '1.3',
    'AU': '1.3',
    'BE': '1.3',
    'BD': '1.4',
    'BR': '1.1',
    'CH': '1.3',
    'CL': '1.3',
    'CO': '1.3',
    'CR': '1.3',
    'CZ': '1.3',
    'DE': '1.3',
    'ES': '1.3',
    'FR': '1.3',
    'GB': '1.3',
    'GR': '1.3',
    'GT': '1.3',
    'HU': '1.3',
    'IN': '1.3T',
    'IT': '1.1',
    'LU': '1.3',
    'ME': '1.3',
    'MK': '1.3',
    'MM': '1.3T',
    'MX': '1.3',
    'NI': '1.3',
    'PA': '1.3',
    'PE': '1.3',
    'PH': '1.3T',
    'PL': '1.3',
    'RS': '1.3',
    'RU': '1.3',
    'SV': '1.3',
    'UY': '1.3',
    'VE': '1.3',
}

TABLEAU_DB_URL = config('TABLEAU_DB_URL', default=None)

MAXMIND_DB_URL = config('MAXMIND_DB_URL', default=None)
MAXMIND_DB_PATH = config('MAXMIND_DB_PATH',
                         default=path('..', 'GeoIP2-Country.mmdb'))
MAXMIND_DEFAULT_COUNTRY = config('MAXMIND_DEFAULT_COUNTRY', default='US')

ADMINS = MANAGERS = config('ADMINS', cast=json.loads,
                           default=json.dumps([['admin', 'admin@example.com']]))

GTM_CONTAINER_ID = config('GTM_CONTAINER_ID', default='')
GMAP_API_KEY = config('GMAP_API_KEY', default='')
HMAC_KEYS = config('HMAC_KEYS', cast=json.loads, default='{}')

STATSD_CLIENT = config('STATSD_CLIENT', default='django_statsd.clients.normal')
STATSD_HOST = config('STATSD_HOST', default='127.0.0.1')
STATSD_PORT = config('STATSD_PORT', cast=int, default=8125)
STATSD_PREFIX = config('STATSD_PREFIX', default='bedrock')

SSLIFY_DISABLE = config('DISABLE_SSL', default=True, cast=bool)
if not SSLIFY_DISABLE:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
