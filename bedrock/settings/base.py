# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""IMPORTANT: bedrock/settings/__init__.py contains important logic that determines
which site will be served.
"""

import json
import platform
import socket
import struct
import sys
from os.path import abspath
from pathlib import Path

from django.conf.locale import LANG_INFO  # we patch this in bedrock.base.apps.BaseAppConfig  # noqa: F401
from django.utils.functional import lazy

import markus
import sentry_sdk
from everett.manager import ListOf
from greenlet import GreenletExit
from sentry_processor import DesensitizationProcessor
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger

from bedrock.base.config_manager import config
from bedrock.contentful.constants import (
    DEFAULT_CONTENT_TYPES as CONTENTFUL_DEFAULT_CONTENT_TYPES,
)

# ROOT path of the project. A pathlib.Path object.
DATA_PATH = config("DATA_PATH", default="data")
ROOT_PATH = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT_PATH / DATA_PATH
ROOT = str(ROOT_PATH)


def path(*args):
    return abspath(str(ROOT_PATH.joinpath(*args)))


def data_path(*args):
    return abspath(str(DATA_PATH.joinpath(*args)))


# Is this a development-mode deployment where we might have
# extra behaviour/helpers/URLs enabled? (eg, local dev or demo)
# (Don't infer that this specifically means our Dev _deployment_
# - it doesn't. You can use APP_NAME, below, to get that)
DEV = config("DEV", parser=bool, default="false")

# Is this particular deployment running in _production-like_ mode?
# (This will include the Dev and Staging deployments, for instance)
PROD = config("PROD", parser=bool, default="false")

DEBUG = config("DEBUG", parser=bool, default="false")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": data_path("bedrock.db"),
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CACHES = {
    "default": {
        "BACKEND": "bedrock.base.cache.SimpleDictCache",
        "LOCATION": "default",
        "TIMEOUT": 600,
        "OPTIONS": {
            "MAX_ENTRIES": 5000,
            "CULL_FREQUENCY": 4,  # 1/4 entries deleted if max reached
        },
    },
}

# in case django-pylibmc is in use
PYLIBMC_MIN_COMPRESS_LEN = 150 * 1024
PYLIBMC_COMPRESS_LEVEL = 1  # zlib.Z_BEST_SPEED

# Logging
LOG_LEVEL = config("LOG_LEVEL", default="INFO")
HAS_SYSLOG = True
SYSLOG_TAG = "http_app_bedrock"
LOGGING_CONFIG = None

# CEF Logging - TODO: remove these if def redundant
CEF_PRODUCT = "Bedrock"
CEF_VENDOR = "Mozilla"
CEF_VERSION = "0"
CEF_DEVICE_VERSION = "0"


# Internationalization.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = config("TIME_ZONE", default="America/Los_Angeles")

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

USE_TZ = True

USE_ETAGS = config("USE_ETAGS", default=str(not DEBUG), parser=bool)

# just here so Django doesn't complain
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-US"

# Languages using BiDi (right-to-left) layout. Overrides/extends Django default.
LANGUAGES_BIDI = ["ar", "ar-dz", "fa", "he", "skr", "ur"]

# Tells the product_details module where to find our local JSON files.
# This ultimately controls how LANGUAGES are constructed.
PROD_DETAILS_CACHE_NAME = "product-details"
PROD_DETAILS_CACHE_TIMEOUT = 60 * 15  # 15 min
PROD_DETAILS_STORAGE = config("PROD_DETAILS_STORAGE", default="product_details.storage.PDDatabaseStorage")
# path into which to clone the p-d json repo
PROD_DETAILS_JSON_REPO_PATH = config("PROD_DETAILS_JSON_REPO_PATH", default=data_path("product_details_json"))
PROD_DETAILS_JSON_REPO_URI = config("PROD_DETAILS_JSON_REPO_URI", default="https://github.com/mozilla-releng/product-details.git")
PROD_DETAILS_JSON_REPO_BRANCH = config("PROD_DETAILS_JSON_REPO_BRANCH", default="production")
# path to updated p-d data for testing before loading into DB
PROD_DETAILS_TEST_DIR = str(Path(PROD_DETAILS_JSON_REPO_PATH).joinpath("public", "1.0"))

# Regions defined on the `/locales/` page.
LOCALES_BY_REGION = {
    "Americas": ["azz", "cak", "en-CA", "en-US", "es-AR", "es-CL", "es-MX", "gn", "is", "pt-BR", "trs"],
    "Asia Pacific": [
        "bn",
        "hi-IN",
        "id",
        "ja",
        "kk",
        "km",
        "ko",
        "ml",
        "mr",
        "ms",
        "my",
        "ne-NP",
        "pa-IN",
        "si",
        "ta",
        "te",
        "th",
        "tl",
        "ur",
        "vi",
        "zh-CN",
        "zh-TW",
    ],
    "Europe": [
        "an",
        "ast",
        "be",
        "bg",
        "br",
        "bs",
        "ca",
        "cs",
        "cy",
        "da",
        "de",
        "dsb",
        "el",
        "en-GB",
        "eo",
        "es-ES",
        "et",
        "eu",
        "fi",
        "fr",
        "fy-NL",
        "ga-IE",
        "gd",
        "gl",
        "hr",
        "hsb",
        "hu",
        "hy-AM",
        "ia",
        "it",
        "ka",
        "lij",
        "lt",
        "ltg",
        "lv",
        "mk",
        "nb-NO",
        "nl",
        "nn-NO",
        "oc",
        "pl",
        "pt-PT",
        "rm",
        "ro",
        "ru",
        "sco",
        "sk",
        "sl",
        "sq",
        "sr",
        "sv-SE",
        "tr",
        "uk",
        "uz",
    ],
    "Middle East and Africa": ["ach", "af", "ar", "az", "fa", "ff", "gu-IN", "he", "kab", "kn", "skr", "son", "xh"],
}


def _put_default_lang_first(langs, default_lang=LANGUAGE_CODE):
    if langs.index(default_lang):
        langs.pop(langs.index(default_lang))
    langs.insert(0, default_lang)
    return langs


# Our accepted production locales are the values from the above, plus an exception.
PROD_LANGUAGES = _put_default_lang_first(sorted(sum(LOCALES_BY_REGION.values(), [])) + ["ja-JP-mac"])

GITHUB_REPO = "https://github.com/mozilla/bedrock"

# NOTE: This default l10n config is for mozorg.
# In settings/__init__.py we plug in an alternative Pocket-appropriate l10n setup.

# Global L10n files.
FLUENT_DEFAULT_FILES = [
    "affiliate",
    "banners/firefox-app-store",
    "brands",
    "download_button",
    "footer",
    "fxa_form",
    "mozorg/about/shared",
    "navigation",
    "navigation_v2",
    "newsletter_form",
    "send_to_device",
    "sub_navigation",
    "ui",
    "mozilla-account-promo",
]

FLUENT_DEFAULT_PERCENT_REQUIRED = config("FLUENT_DEFAULT_PERCENT_REQUIRED", default="80", parser=int)
FLUENT_REPO = config("FLUENT_REPO", default="mozmeao/www-l10n")
FLUENT_REPO_URL = f"https://github.com/{FLUENT_REPO}"
FLUENT_REPO_BRANCH = config("FLUENT_REPO_BRANCH", default="master")
FLUENT_REPO_PATH = DATA_PATH / "www-l10n"
# will be something like "<github username>:<github token>"
FLUENT_REPO_AUTH = config("FLUENT_REPO_AUTH", default="")
FLUENT_LOCAL_PATH = ROOT_PATH / "l10n"
FLUENT_L10N_TEAM_REPO = config("FLUENT_L10N_TEAM_REPO", default="mozilla-l10n/www-l10n")
FLUENT_L10N_TEAM_REPO_URL = f"https://github.com/{FLUENT_L10N_TEAM_REPO}"
FLUENT_L10N_TEAM_REPO_BRANCH = config("FLUENT_L10N_TEAM_REPO_BRANCH", default="master")
FLUENT_L10N_TEAM_REPO_PATH = DATA_PATH / "l10n-team"
# 10 seconds during dev and 10 min in prod
FLUENT_CACHE_TIMEOUT = config("FLUENT_CACHE_TIMEOUT", default="10" if DEBUG else "600", parser=int)
# Order matters. first string found wins.
FLUENT_PATHS = [
    # local FTL files
    FLUENT_LOCAL_PATH,
    # remote FTL files from l10n team
    FLUENT_REPO_PATH,
]

# These are defined up front, because we need them for more than just Pocket mode, but
# note that they are also swapped in as the Fluent defaults in settings/__init__.py
POCKET_FLUENT_REPO = config(
    "POCKET_FLUENT_REPO",
    default="mozilla-l10n/pocket-www-l10n",
)
POCKET_FLUENT_REPO_URL = f"https://github.com/{POCKET_FLUENT_REPO}"
POCKET_FLUENT_REPO_PATH = DATA_PATH / "pocket-www-l10n"
POCKET_FLUENT_REPO_BRANCH = config("POCKET_FLUENT_REPO_BRANCH", default="main")

# Templates to exclude from having an "edit this page" link in the footer
# these are typically ones for which most of the content is in the DB
EXCLUDE_EDIT_TEMPLATES = [
    "firefox/releases/nightly-notes.html",
    "firefox/releases/dev-browser-notes.html",
    "firefox/releases/esr-notes.html",
    "firefox/releases/beta-notes.html",
    "firefox/releases/aurora-notes.html",
    "firefox/releases/release-notes.html",
    "firefox/releases/notes.html",
    "firefox/releases/system_requirements.html",
    "mozorg/credits.html",
    "mozorg/about/forums.html",
    "security/advisory.html",
    "security/advisories.html",
    "security/product-advisories.html",
    "security/known-vulnerabilities.html",
]
IGNORE_LANG_DIRS = [
    ".git",
    "configs",
    "metadata",
]


def get_dev_languages():
    try:
        return [lang.name for lang in FLUENT_REPO_PATH.iterdir() if lang.is_dir() and lang.name not in IGNORE_LANG_DIRS]
    except OSError:
        # no locale dir
        return list(PROD_LANGUAGES)


DEV_LANGUAGES = _put_default_lang_first(get_dev_languages())


# Map short locale names to long, preferred locale names. This
# will be used in urlresolvers to determine the
# best-matching locale from the user's Accept-Language header.
CANONICAL_LOCALES = {
    "en": "en-US",
    "es": "es-ES",
    "ja-JP-mac": "ja",
    "no": "nb-NO",
    "pt": "pt-BR",
    "sv": "sv-SE",
    "zh-Hant": "zh-TW",  # Bug 1263193
    "zh-Hant-TW": "zh-TW",  # Bug 1263193
    "zh-HK": "zh-TW",  # Bug 1338072
    "zh-Hant-HK": "zh-TW",  # Bug 1338072
}

# Unlocalized pages are usually redirected to the English (en-US) equivalent,
# but sometimes it would be better to offer another locale as fallback. This map
# specifies such cases.
FALLBACK_LOCALES = {
    "es-AR": "es-ES",
    "es-CL": "es-ES",
    "es-MX": "es-ES",
}


def lazy_lang_group():
    """Groups languages with a common prefix into a map keyed on said prefix"""
    from django.conf import settings

    groups = {}
    langs = settings.DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    for lang in langs:
        if "-" in lang:
            prefix, _ = lang.split("-", 1)
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
    return {i: i for i in langs}


def lazy_langs():
    """
    Override Django's built-in with our native names

    Note: Unlike the above lazy methods, this one returns a list of tuples to
    match Django's expectations, BUT it has mixed-case lang codes, rather
    than core Django's all-lowercase codes. This is because we work with
    mixed-case codes and we'll need them in LANGUAGES when we use
    Wagtail-Localize, as that has to be configured with a subset of LANGUAGES

    :return: list of tuples

    """
    from django.conf import settings

    from product_details import product_details

    langs = DEV_LANGUAGES if settings.DEV else settings.PROD_LANGUAGES
    return [(lang, product_details.languages[lang]["native"]) for lang in langs if lang in product_details.languages]


def language_url_map_with_fallbacks():
    """
    Return a complete dict of language -> URL mappings, including the canonical
    short locale maps (e.g. es -> es-ES and en -> en-US), as well as fallback
    mappings for language variations we don't support directly but via a nearest
    match

    :return: dict
    """
    lum = lazy_lang_url_map()
    langs = dict(list(lum.items()) + list(CANONICAL_LOCALES.items()))
    # Add missing short locales to the list. By default, this will automatically
    # map en to en-GB (not en-US), etc. in alphabetical order.
    # To override this behavior, explicitly define a preferred locale
    # map with the CANONICAL_LOCALES setting.
    langs.update((k.split("-")[0], v) for k, v in lum.items() if k.split("-")[0] not in langs)

    return langs


LANG_GROUPS = lazy(lazy_lang_group, dict)()
LANGUAGE_URL_MAP = lazy(lazy_lang_url_map, dict)()
LANGUAGE_URL_MAP_WITH_FALLBACKS = lazy(language_url_map_with_fallbacks, dict)()  # used in normalize_language
LANGUAGES = lazy(lazy_langs, list)()

FEED_CACHE = 3900
# 30 min during dev and 10 min in prod
DOTLANG_CACHE = config("DOTLANG_CACHE", default="1800" if DEBUG else "600", parser=int)

# country code for GEO-IP lookup to return in dev mode
DEV_GEO_COUNTRY_CODE = config("DEV_GEO_COUNTRY_CODE", default="US")

# Paths that don't require a locale code in the URL.
# matches the first url component (e.g. mozilla.org/credits)
SUPPORTED_NONLOCALES = [
    # from redirects.urls
    "media",
    "static",
    "certs",
    "images",  # root_files
    "credits",  # in mozorg urls
    "robots.txt",  # in mozorg urls
    ".well-known",  # in mozorg urls
    "telemetry",  # redirect only
    "webmaker",  # redirect only
    "healthz",  # Needed for k8s
    "readiness",  # Needed for k8s
    "healthz-cron",  # status dash, in urls/mozorg_mode.py
    "2004",  # in mozorg urls
    "2005",  # in mozorg urls
    "2006",  # in mozorg urls
    "keymaster",  # in mozorg urls
    "microsummaries",  # in mozorg urls
    "xbl",  # in mozorg urls
    "revision.txt",  # from root_files
    "locales",  # in mozorg urls
]
# Paths that can exist either with or without a locale code in the URL.
# Matches the whole URL path
SUPPORTED_LOCALE_IGNORE = [
    "/sitemap_none.xml",  # in sitemap urls
    "/sitemap.xml",  # in sitemap urls
]
# Pages that we don't want to be indexed by search engines.
# Only impacts sitemap generator. If you need to disallow indexing of
# specific URLs, add them to mozorg/templates/mozorg/robots.txt.
NOINDEX_URLS = [
    r"^(404|500)/",
    r"^firefox/welcome/",
    r"^contribute/(embed|event)/",
    r"^firefox/set-as-default/thanks/",
    r"^firefox/unsupported/",
    r"^firefox/(sms-)?send-to-device-post",
    r"^firefox/feedback",
    r"^firefox/stub_attribution_code/",
    r"^firefox/dedicated-profiles/",
    r"^firefox/installer-help/",
    r"^firefox/this-browser-comes-highly-recommended/",
    r"^firefox/nightly/notes/feed/$",
    r"^firefox.*/all/$",
    r"^.+/(firstrun|whatsnew)/$",
    r"^m/",
    r"^newsletter/(confirm|existing|hacks\.mozilla\.org|recovery|updated|fxa-error)/",
    r"^newsletter/opt-out-confirmation/",
    r"^newsletter/country/success/",
    r"^newsletter/newsletter-strings\.json",
    r"^products/vpn/invite/waitlist/",
    r"^products/monitor/waitlist-plus/",
    r"^products/monitor/waitlist-scan/",
    r"/system-requirements/$",
    r".*/(firstrun|thanks)/$",
    r"^readiness/$",
    r"^healthz(-cron)?/$",
    r"^country-code\.json$",
    r"^firefox/browsers/mobile/get-ios/",
    # exclude redirects
    r"^foundation/annualreport/$",
    r"^firefox/notes/$",
    r"^teach/$",
    r"^about/legal/impressum/$",
    r"^security/announce/",
]

# Pages we do want indexed but don't show up in automated URL discovery
# or are only available in a non-default locale
EXTRA_INDEX_URLS = {
    "/privacy/firefox-klar/": ["de"],
    "/about/legal/impressum/": ["de"],
}

SITEMAPS_REPO = config("SITEMAPS_REPO", default="https://github.com/mozmeao/www-sitemap-generator.git")
SITEMAPS_REPO_BRANCH = config("SITEMAPS_REPO_BRANCH", default="master")
SITEMAPS_PATH = DATA_PATH / "sitemaps"

# Pages that have different URLs for different locales, e.g.
#   'firefox/private-browsing/': {
#       'en-US': '/firefox/features/private-browsing/',
#   },
ALT_CANONICAL_PATHS = {}

ALLOWED_HOSTS = config("ALLOWED_HOSTS", parser=ListOf(str), default="www.mozilla.org,www.ipv6.mozilla.org,www.allizom.org")
ALLOWED_CIDR_NETS = config("ALLOWED_CIDR_NETS", default="", parser=ListOf(str))

# The canonical, production URL without a trailing slash
CANONICAL_URL = "https://www.mozilla.org"

# Make this unique, and don't share it with anybody.
SECRET_KEY = config("SECRET_KEY", default="ssssshhhhh")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        if DEBUG
        else "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

MEDIA_URL = config("MEDIA_URL", default="/user-media/")
MEDIA_ROOT = config("MEDIA_ROOT", default=path("media"))
STATIC_URL = config("STATIC_URL", default="/media/")
STATIC_ROOT = config("STATIC_ROOT", default=path("static"))
STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.FileSystemFinder",)
STATICFILES_DIRS = (path("assets"),)
if DEBUG:
    STATICFILES_DIRS += (path("media"),)


def set_whitenoise_headers(headers, path, url):
    if "/fonts/" in url:
        headers["Cache-Control"] = "public, max-age=604800"  # one week

    if url.startswith("/.well-known/matrix/"):
        headers["Content-Type"] = "application/json"

    if url == "/.well-known/apple-app-site-association":
        headers["Content-Type"] = "application/json"


WHITENOISE_ADD_HEADERS_FUNCTION = set_whitenoise_headers
WHITENOISE_ROOT = config("WHITENOISE_ROOT", default=path("root_files"))
WHITENOISE_MAX_AGE = 6 * 60 * 60  # 6 hours

PROJECT_MODULE = "bedrock"


def get_app_name(hostname):
    """
    Get the app name from the host name.

    The hostname in our deployments will be in the form `bedrock-{version}-{type}-{random-ID}`
    where {version} is "dev", "stage", or "prod", and {type} is the process type
    (e.g. "web" or "clock"). Everywhere else the hostname won't be in this form and
    this helper will just return a default string.
    """
    if hostname.startswith("bedrock-"):
        app_mode = hostname.split("-")[1]
        return "bedrock-" + app_mode

    return "bedrock"


HOSTNAME = platform.node()
# Prefer APP_NAME from env, but fall back to hostname parsing. TODO: remove get_app_name() usage once fully redundant
APP_NAME = config("APP_NAME", default=get_app_name(HOSTNAME))
CLUSTER_NAME = config("CLUSTER_NAME", default="")
ENABLE_HOSTNAME_MIDDLEWARE = config("ENABLE_HOSTNAME_MIDDLEWARE", default=str(bool(APP_NAME)), parser=bool)
ENABLE_VARY_NOCACHE_MIDDLEWARE = config("ENABLE_VARY_NOCACHE_MIDDLEWARE", default="false", parser=bool)
# set this to enable basic auth for the entire site
# e.g. BASIC_AUTH_CREDS="thedude:thewalrus"
BASIC_AUTH_CREDS = config("BASIC_AUTH_CREDS", default="")
ENABLE_METRICS_VIEW_TIMING_MIDDLEWARE = config("ENABLE_METRICS_VIEW_TIMING_MIDDLEWARE", default="false", parser=bool)

MIDDLEWARE = [
    "allow_cidr.middleware.AllowCIDRMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "bedrock.mozorg.middleware.HostnameMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # VaryNoCacheMiddleware must be above LocaleMiddleware"
    # so that it can see the response has a vary on accept-language.
    "bedrock.mozorg.middleware.VaryNoCacheMiddleware",
    "bedrock.base.middleware.BasicAuthMiddleware",
    "bedrock.redirects.middleware.RedirectsMiddleware",  # must come before BedrockLocaleMiddleware
    "bedrock.base.middleware.BedrockLangCodeFixupMiddleware",  # must come after RedirectsMiddleware
    "bedrock.base.middleware.BedrockLocaleMiddleware",  # wraps django.middleware.locale.LocaleMiddleware
    "bedrock.mozorg.middleware.ClacksOverheadMiddleware",
    "bedrock.base.middleware.MetricsStatusMiddleware",
    "bedrock.base.middleware.MetricsViewTimingMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "bedrock.mozorg.middleware.CacheMiddleware",
]

ENABLE_CSP_MIDDLEWARE = config("ENABLE_CSP_MIDDLEWARE", default="true", parser=bool)
if ENABLE_CSP_MIDDLEWARE:
    MIDDLEWARE.append("csp.middleware.CSPMiddleware")

INSTALLED_APPS = [
    # Django contrib apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    # Third-party apps, patches, fixes
    "commonware.response.cookies",
    # L10n
    "product_details",
    # third-party apps
    "django_jinja_markdown",
    "django_jinja",
    "watchman",
    # Local apps
    "bedrock.base",
    "bedrock.firefox",
    "bedrock.foundation",
    "bedrock.legal",
    "bedrock.legal_docs",
    "bedrock.mozorg",
    "bedrock.newsletter",
    "bedrock.press",
    "bedrock.privacy",
    "bedrock.products",
    "bedrock.externalfiles",
    "bedrock.pocket",
    "bedrock.security",
    "bedrock.releasenotes",
    "bedrock.contentcards",
    "bedrock.contentful",
    "bedrock.utils",
    "bedrock.wordpress",
    "bedrock.sitemaps",
    "bedrock.pocketfeed",
    "bedrock.careers",
    # last so that redirects here will be last
    "bedrock.redirects",
    # libs
    "django_extensions",
    "lib.l10n_utils",
]

# Must match the list at CloudFlare if the
# VaryNoCacheMiddleware is enabled. The home
# page is exempt by default.
VARY_NOCACHE_EXEMPT_URL_PREFIXES = (
    "/firefox/",
    "/contribute/",
    "/about/",
    "/contact/",
    "/newsletter/",
    "/privacy/",
    "/foundation/",
)

# Sessions
#
# NB: There are no sessions in Bedrock - it's currently stateless.
# Django's messages framework is configured to use cookie storage,
# not session storage - see MESSAGE_STORAGE below

# legacy setting. backward compat.
DISABLE_SSL = config("DISABLE_SSL", default="true", parser=bool)
# SecurityMiddleware settings
SECURE_REFERRER_POLICY = config("SECURE_REFERRER_POLICY", default="strict-origin-when-cross-origin")
SECURE_HSTS_SECONDS = config("SECURE_HSTS_SECONDS", default="0", parser=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_CONTENT_TYPE_NOSNIFF = config("SECURE_CONTENT_TYPE_NOSNIFF", default="true", parser=bool)
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=str(not DISABLE_SSL), parser=bool)
SECURE_REDIRECT_EXEMPT = [
    r"^readiness/$",
    r"^healthz(-cron)?/$",
]
if config("USE_SECURE_PROXY_HEADER", default=str(SECURE_SSL_REDIRECT), parser=bool):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

STRFTIME_FORMAT_INTERNAL_USE = "%Y-%m-%d %H:%M:%S"

# watchman
WATCHMAN_DISABLE_APM = True
WATCHMAN_CHECKS = (
    "watchman.checks.caches",
    "watchman.checks.databases",
)

TEMPLATES = [
    {
        "BACKEND": "django_jinja.jinja2.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": None,
            "finalize": lambda x: x if x is not None else "",
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "bedrock.base.context_processors.i18n",
                "bedrock.base.context_processors.globals",
                "bedrock.base.context_processors.geo",
                "bedrock.mozorg.context_processors.canonical_path",
                "bedrock.mozorg.context_processors.contrib_numbers",
                "bedrock.mozorg.context_processors.current_year",
                "bedrock.mozorg.context_processors.funnelcake_param",
                "bedrock.firefox.context_processors.latest_firefox_versions",
            ],
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.i18n",
                "jinja2.ext.loopcontrols",
                "django_jinja.builtins.extensions.CsrfExtension",
                "django_jinja.builtins.extensions.StaticFilesExtension",
                "django_jinja.builtins.extensions.DjangoFiltersExtension",
                "django_jinja_markdown.extensions.MarkdownExtension",
            ],
        },
    },
]

# use the Wordpress JSON REST API to get blog data
WP_BLOGS = {
    # 'firefox': {
    #     'url': 'https://blog.mozilla.org/firefox/',
    #     'name': 'The Firefox Frontier',
    #     default num_posts is 20
    #     uncomment and change this to get more
    #     'num_posts': 20,
    # },
    "careers": {
        "url": "https://blog.mozilla.org/careers/",
        "name": "Life@Mozilla",
        "num_posts": 20,
    },
}

GREENHOUSE_BOARD = config("GREENHOUSE_BOARD", default="mozilla")

# used to connect to @MozillaHQ Pocket account
POCKET_API_URL = config("POCKET_API_URL", default="https://getpocket.com/v3/firefox/profile-recs")
POCKET_CONSUMER_KEY = config("POCKET_CONSUMER_KEY", default="")
POCKET_ACCESS_TOKEN = config("POCKET_ACCESS_TOKEN", default="")

# Todo: move this into Pocket-only settings in a way that can also be accessed in tests
BRAZE_API_URL_BASE = config("BRAZE_API_URL_BASE", default="https://rest.iad-05.braze.com")
BRAZE_API_KEY = config("BRAZE_API_KEY", default="")
BRAZE_API_NEWSLETTERS = {
    "news": config("BRAZE_API_NEWSLETTER_ID_NEWS", default=""),
    "hits": config("BRAZE_API_NEWSLETTER_ID_HITS", default=""),
}
BRAZE_POCKET_COOKIE_NAME = config("BRAZE_POCKET_COOKIE_NAME", default="a95b4b6")

# Contribute numbers
# TODO: automate these
CONTRIBUTE_NUMBERS = {
    "num_mozillians": 10554,
    "num_languages": 87,
}

BASKET_URL = config("BASKET_URL", default="https://basket.mozilla.org")
BASKET_API_KEY = config("BASKET_API_KEY", default="")
BASKET_TIMEOUT = config("BASKET_TIMEOUT", parser=int, default="10")
BASKET_SUBSCRIBE_URL = BASKET_URL + "/news/subscribe/"

BOUNCER_URL = config("BOUNCER_URL", default="https://download.mozilla.org/")

# reCAPTCHA keys
RECAPTCHA_PUBLIC_KEY = config("RECAPTCHA_PUBLIC_KEY", default="")
RECAPTCHA_PRIVATE_KEY = config("RECAPTCHA_PRIVATE_KEY", default="")
RECAPTCHA_USE_SSL = config("RECAPTCHA_USE_SSL", parser=bool, default="true")

# Use a message storage mechanism that doesn't need a database.
# This can be changed to use session once we do add a database.
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"


default_email_backend = "django.core.mail.backends.console.EmailBackend" if DEBUG else "django.core.mail.backends.smtp.EmailBackend"

EMAIL_BACKEND = config("EMAIL_BACKEND", default=default_email_backend)
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", default="25", parser=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default="false", parser=bool)
EMAIL_SUBJECT_PREFIX = config("EMAIL_SUBJECT_PREFIX", default="[bedrock] ")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")


EXTERNAL_FILES_PATH = config("EXTERNAL_FILES_PATH", default=data_path("community_data"))
EXTERNAL_FILES_BRANCH = config("EXTERNAL_FILES_BRANCH", default="master")
EXTERNAL_FILES_REPO = config("EXTERNAL_FILES_REPO", default="https://github.com/mozilla/community-data.git")
EXTERNAL_FILES = {
    "credits": {
        "type": "bedrock.mozorg.credits.CreditsFile",
        "name": "credits/names.csv",
    },
}

# Prefix for media. No trailing slash.
# e.g. '//mozorg.cdn.mozilla.net'
CDN_BASE_URL = config("CDN_BASE_URL", default="")

# newsletters that always show for FxA holders
FXA_NEWSLETTERS = [
    "firefox-accounts-journey",
    "test-pilot",
    "take-action-for-the-internet",
    "knowledge-is-power",
]
FXA_NEWSLETTERS_LOCALES = ["en", "de", "fr"]

# Regional press blogs map to locales
PRESS_BLOG_ROOT = "https://blog.mozilla.org/"
PRESS_BLOGS = {
    "de": "press-de/",
    "en-GB": "press-uk/",
    "en-US": "press/",
    "es-AR": "press-es/",
    "es-CL": "press-es/",
    "es-ES": "press-es/",
    "es-MX": "press-es/",
    "fr": "press-fr/",
    "it": "press-it/",
    "pl": "press-pl/",
    "pt-BR": "press-br/",
}

DONATE_LINK = "https://foundation.mozilla.org/{location}"

# Official Firefox Twitter accounts
FIREFOX_TWITTER_ACCOUNTS = {
    "en-US": "https://twitter.com/firefox",
    "es-ES": "https://twitter.com/firefox_es",
    "pt-BR": "https://twitter.com/firefoxbrasil",
}

# Official Mozilla Twitter accounts
MOZILLA_TWITTER_ACCOUNTS = {
    "en-US": "https://twitter.com/mozilla",
    "de": "https://twitter.com/mozilla_germany",
    "fr": "https://twitter.com/mozilla_france",
}

# Official Firefox Instagram accounts
MOZILLA_INSTAGRAM_ACCOUNTS = {
    "en-US": "https://www.instagram.com/mozilla/",
    "de": "https://www.instagram.com/mozilla_deutschland/",
}

# Mozilla accounts product links
# ***This URL *MUST* end in a traling slash!***
FXA_ENDPOINT = config("FXA_ENDPOINT", default="https://accounts.stage.mozaws.net/" if DEV else "https://accounts.firefox.com/")

# Affiliate micro service (CJMS) endpoint (issue 11212)
CJMS_AFFILIATE_ENDPOINT = "https://stage.cjms.nonprod.cloudops.mozgcp.net/aic" if DEV else "https://cjms.services.mozilla.com/aic"

# Google Play and Apple App Store settings
from .appstores import (  # noqa: E402, F401
    AMAZON_FIREFOX_FIRE_TV_LINK,
    APPLE_APPSTORE_COUNTRY_MAP,
    APPLE_APPSTORE_FIREFOX_LINK,
    APPLE_APPSTORE_FOCUS_LINK,
    APPLE_APPSTORE_KLAR_LINK,
    APPLE_APPSTORE_POCKET_LINK,
    GOOGLE_PLAY_FIREFOX_BETA_LINK,
    GOOGLE_PLAY_FIREFOX_LINK,
    GOOGLE_PLAY_FIREFOX_LINK_UTMS,
    GOOGLE_PLAY_FIREFOX_NIGHTLY_LINK,
    GOOGLE_PLAY_FIREFOX_SEND_LINK,
    GOOGLE_PLAY_FOCUS_LINK,
    GOOGLE_PLAY_KLAR_LINK,
    GOOGLE_PLAY_POCKET_LINK,
)

# Locales that should display the 'Send to Device' widget
SEND_TO_DEVICE_LOCALES = ["de", "en-GB", "en-US", "es-AR", "es-CL", "es-ES", "es-MX", "fr", "id", "pl", "pt-BR", "ru", "zh-TW"]

SEND_TO_DEVICE_MESSAGE_SETS = {
    "default": {
        "email": {
            "all": "download-firefox-mobile",
        }
    },
    "fx-mobile-download-desktop": {
        "email": {
            "all": "download-firefox-mobile-reco",
        }
    },
    "fx-whatsnew": {
        "email": {
            "all": "download-firefox-mobile",
        }
    },
    "firefox-mobile-welcome": {
        "email": {
            "all": "firefox-mobile-welcome",
        }
    },
}

if DEV:
    content_cards_default_branch = "dev-processed"
else:
    content_cards_default_branch = "prod-processed"

CONTENT_CARDS_PATH = config("CONTENT_CARDS_PATH", default=data_path("content_cards"))
CONTENT_CARDS_REPO = config("CONTENT_CARDS_REPO", default="https://github.com/mozmeao/www-admin.git")
CONTENT_CARDS_BRANCH = config("CONTENT_CARDS_BRANCH", default=content_cards_default_branch)
CONTENT_CARDS_URL = config("CONTENT_CARDS_URL", default=STATIC_URL)

CONTENTFUL_SPACE_ID = config("CONTENTFUL_SPACE_ID", raise_error=False)
CONTENTFUL_SPACE_KEY = config("CONTENTFUL_SPACE_KEY", raise_error=False)
CONTENTFUL_ENVIRONMENT = config("CONTENTFUL_ENVIRONMENT", default="master")
CONTENTFUL_SPACE_API = ("preview" if DEV else "cdn") + ".contentful.com"
CONTENTFUL_API_TIMEOUT = config("CONTENTFUL_API_TIMEOUT", default="5", parser=int)
CONTENTFUL_CONTENT_TYPES_TO_SYNC = config(
    "CONTENTFUL_CONTENT_TYPES_TO_SYNC",
    default=CONTENTFUL_DEFAULT_CONTENT_TYPES,
    parser=ListOf(str),
)

CONTENTFUL_NOTIFICATION_QUEUE_URL = config("CONTENTFUL_NOTIFICATION_QUEUE_URL", default="", raise_error=False)
CONTENTFUL_NOTIFICATION_QUEUE_REGION = config("CONTENTFUL_NOTIFICATION_QUEUE_REGION", default="", raise_error=False)
CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID = config("CONTENTFUL_NOTIFICATION_QUEUE_ACCESS_KEY_ID", default="", raise_error=False)
CONTENTFUL_NOTIFICATION_QUEUE_SECRET_ACCESS_KEY = config("CONTENTFUL_NOTIFICATION_QUEUE_SECRET_ACCESS_KEY", default="", raise_error=False)
CONTENTFUL_NOTIFICATION_QUEUE_WAIT_TIME = config("CONTENTFUL_NOTIFICATION_QUEUE_WAIT_TIME", default="10", parser=int, raise_error=False)

CONTENTFUL_HOMEPAGE_LOOKUP = {
    # TEMPORARY lookup table for which Contentful `connectHomepage` page ID to get for which locale
    "en-US": "58YIvwDmzSDjtvpSqstDcL",
    "de": "4k3CxqZGjxXOjR1I0dhyto",
}

CONTENTFUL_LOCALE_SUFFICIENT_CONTENT_PERCENTAGE = config(
    "CONTENTFUL_LOCALE_SUFFICIENT_CONTENT_PERCENTAGE",
    default="1" if DEV is True else "60",
    parser=float,
)

RELEASE_NOTES_PATH = config("RELEASE_NOTES_PATH", default=data_path("release_notes"))
RELEASE_NOTES_REPO = config("RELEASE_NOTES_REPO", default="https://github.com/mozilla/release-notes.git")
RELEASE_NOTES_BRANCH = config("RELEASE_NOTES_BRANCH", default="master")

WWW_CONFIG_PATH = config("WWW_CONFIG_PATH", default=data_path("www_config"))
WWW_CONFIG_REPO = config("WWW_CONFIG_REPO", default="https://github.com/mozmeao/www-config.git")
WWW_CONFIG_BRANCH = config("WWW_CONFIG_BRANCH", default="main")

MONITOR_SWITCH_WAITLIST = "SWITCH_MONITOR_WAITLIST"
MONITOR_SWITCH_WAITLIST_DEFAULT = "off"
MONITOR_ENDPOINT = config("MONITOR_ENDPOINT", default="https://monitor.mozilla.org/api/v1/stats")
MONITOR_TOKEN = config("MONITOR_TOKEN", default="")

LEGAL_DOCS_PATH = DATA_PATH / "legal_docs"
LEGAL_DOCS_REPO = config("LEGAL_DOCS_REPO", default="https://github.com/mozilla/legal-docs.git")
LEGAL_DOCS_BRANCH = config("LEGAL_DOCS_BRANCH", default="main" if DEV else "prod")
LEGAL_DOCS_DMS_URL = config("LEGAL_DOCS_DMS_URL", default="")

WEBVISION_DOCS_PATH = DATA_PATH / "webvisions"
WEBVISION_DOCS_REPO = config("WEBVISION_DOCS_REPO", default="https://github.com/mozilla/webvision.git")
WEBVISION_DOCS_BRANCH = config("WEBVISION_DOCS_BRANCH", default="main")

MOFO_SECURITY_ADVISORIES_PATH = config("MOFO_SECURITY_ADVISORIES_PATH", default=data_path("mofo_security_advisories"))
MOFO_SECURITY_ADVISORIES_REPO = config("MOFO_SECURITY_ADVISORIES_REPO", default="https://github.com/mozilla/foundation-security-advisories.git")
MOFO_SECURITY_ADVISORIES_BRANCH = config("MOFO_SECURITY_ADVISORIES_BRANCH", default="master")

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r"^/([a-zA-Z-]+/)?(newsletter)/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["console"],
    },
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(message)s"},
    },
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# DisallowedHost gets a lot of action thanks to scans/bots/scripts,
# but we need not take any action because it's already HTTP 400-ed.
# Note that we ignore at the Sentry client level
ignore_logger("django.security.DisallowedHost")

PASSWORD_HASHERS = ["django.contrib.auth.hashers.PBKDF2PasswordHasher"]
ADMINS = MANAGERS = config("ADMINS", parser=json.loads, default="[]")

GA_ACCOUNT_CODE = ""  # DELETE ME: Deprecated?
GTM_CONTAINER_ID = config("GTM_CONTAINER_ID", default="")  # NB: Will be used in both modes (bedrock and pocket).
# Pocket mode will be running both GA UA and GA4 for a while going forward
GOOGLE_ANALYTICS_ID = config("GOOGLE_ANALYTICS_ID", default="")  # NB: Not used in all Bedrock modes (Pocket only).

GMAP_API_KEY = config("GMAP_API_KEY", default="")
STUB_ATTRIBUTION_HMAC_KEY = config("STUB_ATTRIBUTION_HMAC_KEY", default="")
STUB_ATTRIBUTION_RATE = config("STUB_ATTRIBUTION_RATE", default=str(1 if DEV else 0), parser=float)
STUB_ATTRIBUTION_MAX_LEN = config("STUB_ATTRIBUTION_MAX_LEN", default="600", parser=int)


# via http://stackoverflow.com/a/6556951/107114
def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    try:
        with open("/proc/net/route") as fh:
            for line in fh:
                fields = line.strip().split()
                if fields[1] != "00000000" or not int(fields[3], 16) & 2:
                    continue

                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
        return "localhost"
    except OSError:
        return "localhost"


FIREFOX_MOBILE_SYSREQ_URL = "https://support.mozilla.org/kb/will-firefox-work-my-mobile-device"

MOZILLA_LOCATION_SERVICES_KEY = "a9b98c12-d9d5-4015-a2db-63536c26dc14"

DEAD_MANS_SNITCH_URL = config("DEAD_MANS_SNITCH_URL", default="")  # see cron.py
# There is also a DB_UPDATE_SCRIPT_DMS_URL defined in env vars, which is called directly from
# the bash script bin/run-db-update.sh

# SENTRY CONFIG
SENTRY_DSN = config("SENTRY_DSN", default="")
# Data scrubbing before Sentry
# https://github.com/laiyongtao/sentry-processor
SENSITIVE_FIELDS_TO_MASK_ENTIRELY = [
    "email",
    # "token",  # token is on the default blocklist, which we also use via `with_default_keys`
]
SENTRY_IGNORE_ERRORS = (
    BrokenPipeError,
    ConnectionResetError,
    GreenletExit,
)


def before_send(event, hint):
    if hint and "exc_info" in hint:
        exc_type, exc_value, tb = hint["exc_info"]
        if isinstance(exc_value, SENTRY_IGNORE_ERRORS):
            return None

    processor = DesensitizationProcessor(
        with_default_keys=True,
        sensitive_keys=SENSITIVE_FIELDS_TO_MASK_ENTIRELY,
    )
    event = processor.process(event, hint)
    return event


if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        release=config("GIT_SHA", default=""),
        server_name=".".join(x for x in [APP_NAME, CLUSTER_NAME] if x),
        integrations=[DjangoIntegration()],
        before_send=before_send,
    )

# Frontend uses the same DSN as backend by default, but we'll
# specify a separate one for FE use in Production only
SENTRY_FRONTEND_DSN = config(
    "SENTRY_FRONTEND_DSN",
    default=SENTRY_DSN,
)

# Statsd metrics via markus
if DEBUG:
    MARKUS_BACKENDS = [
        {"class": "markus.backends.logging.LoggingMetrics", "options": {"logger_name": "metrics"}},
    ]
else:
    STATSD_HOST = config("STATSD_HOST", default=get_default_gateway_linux())
    STATSD_PORT = config("STATSD_PORT", default="8125", parser=int)
    STATSD_NAMESPACE = config("APP_NAME", default="bedrock-local")

    MARKUS_BACKENDS = [
        {
            "class": "markus.backends.datadog.DatadogMetrics",
            "options": {
                "statsd_host": STATSD_HOST,
                "statsd_port": STATSD_PORT,
                "statsd_namespace": STATSD_NAMESPACE,
            },
        },
    ]

markus.configure(backends=MARKUS_BACKENDS)

# Django-CSP settings are in settings/__init__.py, where they are
# set according to site mode

# Bug 1345467: Funnelcakes are now explicitly configured in the environment.
# Set experiment specific variables like the following:
#
# FUNNELCAKE_103_PLATFORMS=win,win64
# FUNNELCAKE_103_LOCALES=de,fr,en-US
#
# where "103" in the variable name is the funnelcake ID.

# VPN ==========================================================================================

# URL for Mozilla VPN sign-in links
# ***This URL *MUST* end in a traling slash!***
VPN_ENDPOINT = config("VPN_ENDPOINT", default="https://stage.guardian.nonprod.cloudops.mozgcp.net/" if DEV else "https://vpn.mozilla.org/")

# URL for Mozilla VPN subscription links
# ***This URL *MUST* end in a traling slash!***
VPN_SUBSCRIPTION_URL = config("VPN_SUBSCRIPTION_URL", default="https://accounts.stage.mozaws.net/" if DEV else "https://accounts.firefox.com/")

# Product ID for VPN subscriptions
VPN_PRODUCT_ID = config("VPN_PRODUCT_ID", default="prod_FiJ42WCzZNRSbS" if DEV else "prod_FvnsFHIfezy3ZI")

# VPN variable subscription plan IDs by currency/language.
VPN_PLAN_ID_MATRIX = {
    "chf": {  # Swiss franc
        "de": {  # German
            "12-month": {
                "id": "price_1J4sAUKb9q6OnNsLfYDKbpdY" if DEV else "price_1J5JssJNcmPzuWtR616BH4aU",
                "price": "5.99",
                "total": "71.88",
                "currency": "CHF",
                "saving": 45,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "60.00", "price": "71.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J4sC2Kb9q6OnNsLIgz3DDu8" if DEV else "price_1J5Ju3JNcmPzuWtR3GpNYSWj",
                "price": "10.99",
                "total": None,
                "currency": "CHF",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "0", "price": "10.99", "period": "monthly"},
            },
        },
        "fr": {  # French
            "12-month": {
                "id": "price_1J4sM2Kb9q6OnNsLsGLZwTP9" if DEV else "price_1J5JunJNcmPzuWtRo9dLxn6M",
                "price": "5.99",
                "total": "71.88",
                "currency": "CHF",
                "saving": 45,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "60.00", "price": "71.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J4sNGKb9q6OnNsLl3OEuKqT" if DEV else "price_1J5JvjJNcmPzuWtR3wwy1dcR",
                "price": "10.99",
                "currency": "CHF",
                "total": None,
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "0", "price": "10.99", "period": "monthly"},
            },
        },
        "it": {  # Italian
            "12-month": {
                "id": "price_1J4sWMKb9q6OnNsLkrTo2uUW" if DEV else "price_1J5JwWJNcmPzuWtRgrx5fjOc",
                "price": "5.99",
                "total": "71.88",
                "currency": "CHF",
                "saving": 45,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "60.00", "price": "71.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J4sXWKb9q6OnNsLVoGiXcW5" if DEV else "price_1J5JxGJNcmPzuWtRrp5e1SUB",
                "price": "10.99",
                "total": None,
                "currency": "CHF",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CHF", "discount": "0", "price": "10.99", "period": "monthly"},
            },
        },
    },
    "czk": {  # Czech koruna
        "cs": {  # Czech
            "12-month": {
                "id": "price_1N7ObPKb9q6OnNsLf9okHbUl" if DEV else "price_1N7PDwJNcmPzuWtR1IxSkZ0c",
                "price": "119",
                "total": "1428",
                "currency": "CZK",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CZK", "discount": "1416", "price": "1428", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7Oc2Kb9q6OnNsLkYPFVHtx" if DEV else "price_1N7PESJNcmPzuWtRTgmv8Ve4",
                "price": "237",
                "total": None,
                "currency": "CZK",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "CZK", "discount": "0", "price": "237", "period": "monthly"},
            },
        },
    },
    "dkk": {  # Danish krone
        "da": {  # Dansk
            "12-month": {
                "id": "price_1N7Oa1Kb9q6OnNsLh9F1hDhi" if DEV else "price_1N7PCQJNcmPzuWtRNqtksScA",
                "price": "37",
                "total": "444",
                "currency": "DKK",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "DKK", "discount": "456", "price": "444", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7OapKb9q6OnNsLTvIbY6DY" if DEV else "price_1N7PCsJNcmPzuWtRXIMBFQbq",
                "price": "75",
                "total": None,
                "currency": "DKK",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "DKK", "discount": "0", "price": "75", "period": "monthly"},
            },
        },
    },
    "euro": {  # Euro
        "bg": {  # Bulgarian
            "12-month": {
                "id": "price_1N7OdmKb9q6OnNsLO0Rf6LUt" if DEV else "price_1N7PGEJNcmPzuWtRzTe85nzw",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7OeJKb9q6OnNsLvGDxhcaj" if DEV else "price_1N7PHRJNcmPzuWtRjZ8D8kwx",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "de": {  # German
            "12-month": {
                "id": "price_1IXw5oKb9q6OnNsLPMkWOid7" if DEV else "price_1IgwblJNcmPzuWtRynC7dqQa",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N9CInKb9q6OnNsLQYotCVpd" if DEV else "price_1IgwZVJNcmPzuWtRg9Wssh2y",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "el": {  # Greek
            "12-month": {
                "id": "price_1N7Or1Kb9q6OnNsLhHrEcbwd" if DEV else "price_1N7PPyJNcmPzuWtRkUbirJmB",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7OrgKb9q6OnNsLk5xS9DYr" if DEV else "price_1N7PQIJNcmPzuWtR2BQdQbtL",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "en": {  # English
            "12-month": {
                "id": "price_1JcuArKb9q6OnNsLXAnkCSUE" if DEV else "price_1JcdvBJNcmPzuWtROLbEH9d2",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1Jcu7uKb9q6OnNsLG4JAAXuw" if DEV else "price_1JcdsSJNcmPzuWtRGF9Y5TMJ",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "es": {  # Spanish
            "12-month": {
                "id": "price_1J4pE7Kb9q6OnNsLnvvyRClI" if DEV else "price_1J5JCdJNcmPzuWtRrvQMFLlP",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J4pFSKb9q6OnNsLEyiFLbvB" if DEV else "price_1J5JDgJNcmPzuWtRqQtIbktk",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "fr": {  # French
            "12-month": {
                "id": "price_1N9CFcKb9q6OnNsL1r7W4EiX" if DEV else "price_1IgnlcJNcmPzuWtRjrNa39W4",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N9CHBKb9q6OnNsLlYDTJ3px" if DEV else "price_1IgowHJNcmPzuWtRzD7SgAYb",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "hu": {  # Hungarian
            "12-month": {
                "id": "price_1N7OcfKb9q6OnNsLuXLBVp8T" if DEV else "price_1N7PF1JNcmPzuWtRujxNI9yh",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7OdBKb9q6OnNsLJENr3u8W" if DEV else "price_1N7PFbJNcmPzuWtRlVNtHvgG",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "it": {  # Italian
            "12-month": {
                "id": "price_1J4p3CKb9q6OnNsLK2oBxgsV" if DEV else "price_1J4owvJNcmPzuWtRomVhWQFq",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J4p6wKb9q6OnNsLTb6kCDsC" if DEV else "price_1J5J6iJNcmPzuWtRK5zfoguV",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "nl": {  # Dutch
            "12-month": {
                "id": "price_1J4ryxKb9q6OnNsL3fPF8mxI" if DEV else "price_1J5JRGJNcmPzuWtRXwXA84cm",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J4s0MKb9q6OnNsLS19LMKBb" if DEV else "price_1J5JSkJNcmPzuWtR54LPH2zi",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "pt": {  # Portuguese
            "12-month": {
                "id": "price_1N7OSoKb9q6OnNsLdJDSaCBW" if DEV else "price_1N7PBOJNcmPzuWtRykt8Uyzm",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7OUEKb9q6OnNsLXlaW6Ovc" if DEV else "price_1N7PBsJNcmPzuWtRzS5kTc5B",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "ro": {  # Romanian
            "12-month": {
                "id": "price_1N7ORMKb9q6OnNsLVMHfYXQq" if DEV else "price_1N7PADJNcmPzuWtRxHjlrDiy",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7OS5Kb9q6OnNsLA2BVYqTG" if DEV else "price_1N7PAmJNcmPzuWtR1zOoPIao",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "sk": {  # Slovak
            "12-month": {
                "id": "price_1N7OjyKb9q6OnNsLRnctp7yW" if DEV else "price_1N7PKUJNcmPzuWtRrnyAM0wd",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7OkVKb9q6OnNsL5Vzz6X9D" if DEV else "price_1N7PKyJNcmPzuWtROTKgdgW0",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
        "sl": {  # Slovenian
            "12-month": {
                "id": "price_1N7OmEKb9q6OnNsLI2fRSJX3" if DEV else "price_1N7PMcJNcmPzuWtR8TWsjoHe",
                "price": "4.99",
                "total": "59.88",
                "currency": "EUR",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7OmiKb9q6OnNsLvXqreUUk" if DEV else "price_1N7PN6JNcmPzuWtRpN8HAr7L",
                "price": "9.99",
                "total": None,
                "currency": "EUR",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "EUR", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        },
    },
    "pln": {  # Polish złoty
        "en": {  # English
            "12-month": {
                "id": "price_1N7OOaKb9q6OnNsLSUzW83h9" if DEV else "price_1N7P8TJNcmPzuWtRI7pI29bO",
                "price": "22",
                "total": "264",
                "currency": "PLN",
                "saving": 48,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "PLN", "discount": "276", "price": "264", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1N7OQWKb9q6OnNsLMLHUFggO" if DEV else "price_1N7P98JNcmPzuWtRbUaI24OH",
                "price": "45",
                "total": None,
                "currency": "PLN",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "PLN", "discount": "0", "price": "45", "period": "monthly"},
            },
        },
    },
    "usd": {  # US dollar
        "en": {  # English
            "12-month": {
                "id": "price_1J0Y1iKb9q6OnNsLXwdOFgDr" if DEV else "price_1Iw85dJNcmPzuWtRyhMDdtM7",
                "price": "4.99",
                "total": "59.88",
                "currency": "USD",
                "saving": 50,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "USD", "discount": "60.00", "price": "59.88", "period": "yearly"},
            },
            "monthly": {
                "id": "price_1J0owvKb9q6OnNsLExNhEDXm" if DEV else "price_1Iw7qSJNcmPzuWtRMUZpOwLm",
                "price": "9.99",
                "total": None,
                "currency": "USD",
                "saving": None,
                "analytics": {"brand": "vpn", "plan": "vpn", "currency": "USD", "discount": "0", "price": "9.99", "period": "monthly"},
            },
        }
    },
}

# Map of country codes to allocated VPN currency/language plan IDs.
# Each country can support both a default language and (optionally)
# a set of one or more alternative languages.
VPN_VARIABLE_PRICING = {
    "AT": {  # Austria
        "default": VPN_PLAN_ID_MATRIX["euro"]["de"],
    },
    "BE": {  # Belgium
        "default": VPN_PLAN_ID_MATRIX["euro"]["nl"],
        "de": VPN_PLAN_ID_MATRIX["euro"]["de"],
        "fr": VPN_PLAN_ID_MATRIX["euro"]["fr"],
    },
    "BG": {  # Bulgaria
        "default": VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "CH": {  # Switzerland
        "default": VPN_PLAN_ID_MATRIX["chf"]["de"],
        "fr": VPN_PLAN_ID_MATRIX["chf"]["fr"],
        "it": VPN_PLAN_ID_MATRIX["chf"]["it"],
    },
    "CY": {  # Cyprus
        "default": VPN_PLAN_ID_MATRIX["euro"]["en"],
        "el": VPN_PLAN_ID_MATRIX["euro"]["el"],
    },
    "CZ": {  # Czech Republic
        "default": VPN_PLAN_ID_MATRIX["czk"]["cs"],
    },
    "DE": {  # Germany
        "default": VPN_PLAN_ID_MATRIX["euro"]["de"],
    },
    "DK": {  # Denmark
        "default": VPN_PLAN_ID_MATRIX["dkk"]["da"],
    },
    "EE": {  # Estonia
        "default": VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "ES": {  # Spain
        "default": VPN_PLAN_ID_MATRIX["euro"]["es"],
    },
    "FI": {  # Finland
        "default": VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "FR": {  # France
        "default": VPN_PLAN_ID_MATRIX["euro"]["fr"],
    },
    "HR": {  # Croatia
        "default": VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "HU": {  # Hungary
        "default": VPN_PLAN_ID_MATRIX["euro"]["hu"],
    },
    "IE": {  # Ireland
        "default": VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "IT": {  # Italy
        "default": VPN_PLAN_ID_MATRIX["euro"]["it"],
    },
    "LT": {  # Lithuania
        "default": VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "LU": {  # Luxembourg
        "default": VPN_PLAN_ID_MATRIX["euro"]["fr"],
        "de": VPN_PLAN_ID_MATRIX["euro"]["de"],
    },
    "LV": {  # Latvia
        "default": VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "MT": {  # Malta
        "default": VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "NL": {  # The Netherlands
        "default": VPN_PLAN_ID_MATRIX["euro"]["nl"],
    },
    "PL": {  # Poland
        "default": VPN_PLAN_ID_MATRIX["pln"]["en"],
    },
    "PT": {  # Portugal
        "default": VPN_PLAN_ID_MATRIX["euro"]["pt"],
    },
    "RO": {  # Romania
        "default": VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "SE": {  # Sweden
        "default": VPN_PLAN_ID_MATRIX["euro"]["en"],
    },
    "SI": {  # Slovenia
        "default": VPN_PLAN_ID_MATRIX["euro"]["sl"],
    },
    "SK": {  # Slovakia
        "default": VPN_PLAN_ID_MATRIX["euro"]["sk"],
    },
    "US": {  # USA
        "default": VPN_PLAN_ID_MATRIX["usd"]["en"],
    },
}

# Mozilla VPN Geo restrictions
# https://github.com/mozilla-services/guardian-website/blob/master/server/constants.ts

# Countries where VPN is available.
VPN_COUNTRY_CODES = [
    "CA",  # Canada
    "MY",  # Malaysia
    "NZ",  # New Zealand
    "SG",  # Singapore
    # United Kingdom + "Territories"
    "GB",  # United Kingdom of Great Britain and Northern Island
    "GG",  # Guernsey (a British Crown dependency)
    "IM",  # Isle of Man (a British Crown dependency)
    "IO",  # British Indian Ocean Territory
    "JE",  # Jersey (a British Crown dependency)
    "UK",  # United Kingdom
    "VG",  # Virgin Islands (British)
    # USA + "Territories"
    "AS",  # American Samoa
    "MP",  # Northern Mariana Islands
    "PR",  # Puerto Rico
    "UM",  # United States Minor Outlying Islands
    "US",  # United States of America
    "VI",  # Virgin Islands (U.S.)
    # EU Countries
    "DE",  # Germany
    "FR",  # France
    "AT",  # Austria
    "BE",  # Belgium
    "CH",  # Switzerland
    "ES",  # Spain
    "IT",  # Italy
    "IE",  # Ireland
    "NL",  # Netherlands
    "SE",  # Sweden
    "FI",  # Finland
    "BG",  # Bulgaria
    "CY",  # Cyprus
    "CZ",  # Czech Republic
    "DK",  # Denmark
    "EE",  # Estonia
    "HR",  # Croatia
    "HU",  # Hungary
    "LT",  # Lithuania
    "LU",  # Luxembourg
    "LV",  # Latvia
    "MT",  # Malta
    "PL",  # Poland
    "PT",  # Portugal
    "RO",  # Romania
    "SI",  # Slovenia
    "SK",  # Slovakia
]

VPN_AFFILIATE_COUNTRIES = ["CA", "DE", "FR", "GB", "IE", "US"]
VPN_AVAILABLE_COUNTRIES = 33
VPN_CONNECT_SERVERS = 500
VPN_CONNECT_COUNTRIES = 30
VPN_CONNECT_DEVICES = 5

# VPN client ID for referral parameter tracking (issue 10811)
VPN_CLIENT_ID = "e6eb0d1e856335fc"

# Countries where we can't legally sell or advertise Mozilla VPN (e.g via /whatsnew)
# See: https://github.com/mozilla/bedrock/issues/11572
VPN_EXCLUDED_COUNTRY_CODES = [
    "AE",  # United Arab Emirates
    "BY",  # Belarus
    "CN",  # China
    "CU",  # Cuba
    "IQ",  # Iraq
    "IR",  # Iran
    "KP",  # North Korea
    "OM",  # Oman
    "RU",  # Russia
    "SD",  # Sudan
    "SY",  # Syria
    "TM",  # Turkmenistan
    "TR",  # Turkey
]

# Countries where we block Mozilla VPN downloads
# See: https://github.com/mozilla/bedrock/issues/11659
VPN_BLOCK_DOWNLOAD_COUNTRY_CODES = [
    "CN",  # China
    "CU",  # Cuba
    "IR",  # Iran
    "KP",  # North Korea
    "SD",  # Sudan
    "SY",  # Syria
]

# VPN / RELAY BUNDLE ============================================================================

# Product ID for VPN & Relay bundle subscriptions.
VPN_RELAY_BUNDLE_PRODUCT_ID = config("VPN_RELAY_BUNDLE_PRODUCT_ID", default="prod_MQ9Zf1cyI81XS2" if DEV else "prod_MIex7Q079igFZJ")

# VPN & Relay bundle plan IDs by currency/language.
VPN_RELAY_BUNDLE_PLAN_ID_MATRIX = {
    "usd": {
        "en": {
            "12-month": {
                "id": "price_1Lwp7uKb9q6OnNsLQYzpzUs5" if DEV else "price_1LwoSDJNcmPzuWtR6wPJZeoh",
                "price": "6.99",
                "total": "83.88",
                "currency": "USD",
                "saving": 40,
                "analytics": {
                    "brand": "vpn",
                    "plan": "vpn + relay",
                    "currency": "USD",
                    "discount": "83.88",
                    "price": "83.88",
                    "period": "yearly",
                },
            },
        }
    },
}

# Map of country codes to allocated VPN & Relay bundle currency/language plan IDs.
# Each country can support both a default language and (optionally) a set of one
# or more alternative languages.
VPN_RELAY_BUNDLE_PRICING = {
    "US": {
        "default": VPN_RELAY_BUNDLE_PLAN_ID_MATRIX["usd"]["en"],
    },
}

# Countries where VPN & Relay bundle is available.
# Phone masking is only supported in these countries.
VPN_RELAY_BUNDLE_COUNTRY_CODES = [
    "CA",  # Canada
    "US",  # United States of America
]

# List of locales that are supported in the Mozilla VPN client application.
VPN_SUPPORTED_LOCALES = [
    "co",
    "cs",
    "cy",
    "de",
    "el",
    "en",
    "es",
    "fi",
    "fr",
    "fy",
    "hsb",
    "hu",
    "ia",
    "id",
    "is",
    "it",
    "ja",
    "lo",
    "nl",
    "pa",
    "pl",
    "pt",
    "ru",
    "sk",
    "sl",
    "sq",
    "sv",
    "tr",
    "uk",
    "zh",
]

# RELAY =========================================================================================

RELAY_PRODUCT_URL = config(
    "RELAY_PRODUCT_URL", default="https://stage.fxprivaterelay.nonprod.cloudops.mozgcp.net/" if DEV else "https://relay.firefox.com/"
)
