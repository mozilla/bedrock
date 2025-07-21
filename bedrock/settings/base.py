# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import platform
import socket
import struct
import sys
from os.path import abspath
from pathlib import Path
from urllib.parse import urlparse

from django.conf.locale import LANG_INFO  # we patch this in bedrock.base.apps.BaseAppConfig  # noqa: F401
from django.utils.functional import lazy

import dj_database_url
import markus
import sentry_sdk
from everett.manager import ChoiceOf, ListOf
from sentry_processor import DesensitizationProcessor
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.rq import RqIntegration

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


db_connection_max_age_secs = config("DB_CONN_MAX_AGE", default="0", parser=int)
db_conn_health_checks = config("DB_CONN_HEALTH_CHECKS", default="false", parser=bool)
db_default_url = config(
    "DATABASE_URL",
    default=f"sqlite:////{data_path('bedrock.db')}",
)

DATABASES = {
    "default": dj_database_url.parse(
        db_default_url,
        conn_max_age=db_connection_max_age_secs,
        conn_health_checks=db_conn_health_checks,
    )
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

TASK_QUEUE_AVAILABLE = False
RQ_QUEUES = {}

REDIS_URL = config("REDIS_URL", default="")
if REDIS_URL:
    TASK_QUEUE_AVAILABLE = True
    REDIS_URL = REDIS_URL.rstrip("/0")
    RQ_QUEUES = {
        # Same Redis DBs/connections
        "default": {"URL": f"{REDIS_URL}/0"},
        "image_renditions": {"URL": f"{REDIS_URL}/0"},
    }

CACHE_TIME_SHORT = config("CACHE_TIME_SHORT", parser=int, default=f"{60 * 10}")  # 10 mins
CACHE_TIME_MED = 60 * 60  # 1 hour
CACHE_TIME_LONG = 60 * 60 * 6  # 6 hours


CACHES = {
    "default": {
        "BACKEND": "bedrock.base.cache.SimpleDictCache",
        "LOCATION": "default",
        "TIMEOUT": CACHE_TIME_SHORT,
        "OPTIONS": {
            "MAX_ENTRIES": 5000,
            "CULL_FREQUENCY": 4,  # 1/4 entries deleted if max reached
        },
    },
}

# Logging
LOG_LEVEL = config(
    "LOG_LEVEL",
    default="INFO",
    parser=ChoiceOf(
        str,
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    ),
)
HAS_SYSLOG = True
SYSLOG_TAG = "http_app_bedrock"
LOGGING_CONFIG = None

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

# Use the "X-Forwarded-Host" header from the CDN to set the Hostname
# https://mozilla-hub.atlassian.net/browse/SE-4263
USE_X_FORWARDED_HOST = config("USE_X_FORWARDED_HOST", default="False", parser=bool)

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
        "gu-IN",
        "hi-IN",
        "id",
        "ja",
        "kk",
        "km",
        "kn",
        "ko",
        "lo",
        "ml",
        "mr",
        "ms",
        "my",
        "ne-NP",
        "pa-IN",
        "si",
        "ta",
        "te",
        "tg",
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
    "Middle East and Africa": ["ach", "af", "ar", "az", "fa", "ff", "he", "kab", "skr", "son", "xh"],
}


def _put_default_lang_first(langs, default_lang=LANGUAGE_CODE):
    if langs.index(default_lang):
        langs.pop(langs.index(default_lang))
    langs.insert(0, default_lang)
    return langs


# Our accepted production locales are the values from the above, plus an exception.
PROD_LANGUAGES = _put_default_lang_first(sorted(sum(LOCALES_BY_REGION.values(), [])) + ["ja-JP-mac"])

GITHUB_REPO = "https://github.com/mozilla/bedrock"

# Global L10n files.
FLUENT_DEFAULT_FILES = [
    "banners/consent-banner",
    "banners/firefox-app-store",
    "brands",
    "download_button",
    "footer",
    "footer-refresh",
    "fxa_form",
    "mozorg/about/shared",
    "navigation",
    "navigation_v2",
    "navigation_refresh",
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
# Also allow entire directories to be skipped
EXCLUDE_EDIT_TEMPLATES_DIRECTORIES = [
    "cms",
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
    "credits",
    "robots.txt",
    ".well-known",
    "telemetry",  # redirect only
    "webmaker",  # redirect only
    "healthz",  # Needed for k8s
    "readiness",  # Needed for k8s
    "healthz-cron",  # status dash
    "2004",
    "2005",
    "2006",
    "keymaster",
    "microsummaries",
    "xbl",
    "revision.txt",  # from root_files
    "locales",
    "csrf_403",
]

# Paths that can exist either with or without a locale code in the URL.
# Matches the whole URL path
SUPPORTED_LOCALE_IGNORE = [
    "/all-urls-global.xml",  # in sitemap urls
    "/all-urls.xml",  # in sitemap urls
]
# Pages that we don't want to be indexed by search engines.
# Only impacts sitemap generator. If you need to disallow indexing of
# specific URLs, add them to mozorg/templates/mozorg/robots.txt.
NOINDEX_URLS = [
    r"^(404|500)/",
    r"^firefox/welcome/",
    r"^contribute/(embed|event)/",
    r"^cms-admin/",
    r"^django-admin/",
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
    r"^firefox/landing/",
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

# Pages that have different URLs for different locales, e.g.
#   'firefox/private-browsing/': {
#       'en-US': '/firefox/features/private-browsing/',
#   },
ALT_CANONICAL_PATHS = {}

# NOTE:
# - In the infra config a pod IP is prepended with a trailing comma
# - In some environments, there might be no additional content after this comma
# - The `allow_empty=True` ensures the split operation works even when nothing follows the comma
# - We then use `filter()` to remove any resulting empty strings from the list
ALLOWED_HOSTS = list(
    filter(
        None,
        config(
            "ALLOWED_HOSTS",
            parser=ListOf(
                str,
                allow_empty=True,
            ),
            default="",
        ),
    )
)

# The canonical, production URL without a trailing slash
CANONICAL_URL = "https://www.mozilla.org"

# Make this unique, and don't share it with anybody.
SECRET_KEY = config("SECRET_KEY", default="ssssshhhhh")

# If config is available, we use Google Cloud Storage, else (for local dev)
# fall back to filesytem storage

GS_BUCKET_NAME = config("GS_BUCKET_NAME", default="")
GS_PROJECT_ID = config("GS_PROJECT_ID", default="")

STORAGES = {
    # In production only the CMS/Editing deployment has write access
    # to the cloud storage bucket. As such, be careful if you introduce
    # file uploads to other parts of Bedrock that use "default" storage -
    # it will not allow uploads for the Web deployment. You will have to
    # specify a different, dedicated storage backend for the file-upload process.
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage"
        if GS_BUCKET_NAME and GS_PROJECT_ID
        else "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        if DEBUG
        else "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

MEDIA_URL = config("MEDIA_URL", default="/custom-media/")
MEDIA_ROOT = config("MEDIA_ROOT", default=path("custom-media"))
STATIC_URL = config("STATIC_URL", default="/media/")
STATIC_ROOT = config("STATIC_ROOT", default=path("static"))
STATICFILES_DIRS = (path("assets"),)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
if DEBUG:
    STATICFILES_DIRS += (path("media"),)

GS_OBJECT_PARAMETERS = {
    "cache_control": "max-age=2592000, public, immutable"  # 2592000 == 30 days / 1 month
}


def _get_media_cdn_hostname_for_storage_backend(media_url):
    # settings.MEDIA_URL (passed in here as media_url) is a custom route on our CDN
    # that points to a cloud bucket, which we use for uploaded media from the CMS.
    #
    # Specifically, due to infra constraints, it has to point to a _sub-path_ in the bucket,
    # not the top/root of it. It also needs to be distinct from the CDN route that points to our
    # collected static assets (which are at https://<CDN_HOSTNAME>/media/ - that is STATIC_URL)
    #
    # With all this in mind, MEDIA_URL, when set, points to https://<CDN_HOSTNAME>/media/cms/
    #
    # When django-storages computes the URL for a object in that CMS bucket, it wants
    # just the hostname of the bucket, not the full CDN/proxy path to the subdir in the bucket,
    # because it opinionatedly concatenates it with GS_LOCATION (defined below, which ensures
    # the files are uploaded to the sub-path mentioned above).
    #
    # TLDR: We just need the root of the CDN, from MEDIA_URL.

    if media_url.startswith("http"):
        media_url_parsed = urlparse(media_url)
        media_cdn_hostname = f"{media_url_parsed.scheme}://{media_url_parsed.hostname}"
    else:
        media_cdn_hostname = media_url

    return media_cdn_hostname


if GS_BUCKET_NAME and GS_PROJECT_ID:
    GS_CUSTOM_ENDPOINT = _get_media_cdn_hostname_for_storage_backend(MEDIA_URL)  # hostname that proxies the storage bucket
    GS_FILE_OVERWRITE = False
    GS_LOCATION = "media/cms"  # path within the bucket to upload to

    # The GCS bucket has a uniform policy (public read, authenticated write) so we don't want
    # to try to sign URLs with querystrings here, as that will cause GCS to respond with
    # 400 Bad Request because signed URLs are not compatible with uniform access control.
    # See the notes for https://django-storages.readthedocs.io/en/latest/backends/gcloud.html#gs-default-acl
    GS_QUERYSTRING_AUTH = False
else:
    SUPPORTED_NONLOCALES += [
        "custom-media",  # using local filesystem storage (for dev)
    ]


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
    # IMPORTANT: this may be extended later in this file or via settings/__init__.py
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
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "bedrock.mozorg.middleware.CacheMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "bedrock.cms.middleware.CMSLocaleFallbackMiddleware",
]

ENABLE_CSP_MIDDLEWARE = config("ENABLE_CSP_MIDDLEWARE", default="true", parser=bool)
if ENABLE_CSP_MIDDLEWARE:
    MIDDLEWARE.append("bedrock.base.middleware.CSPMiddlewareByPathPrefix")

INSTALLED_APPS = [
    # Django contrib apps
    "django.contrib.sessions",
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
    "waffle",
    "watchman",
    # Wagtail CMS and related, necessary apps
    "wagtail.contrib.redirects",
    "wagtail.documents",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.images",
    "wagtail_localize_smartling",  # Has to come before wagtail_localize
    "wagtail_localize",
    "wagtail_localize.locales",  # This replaces "wagtail.locales"
    "wagtail.search",
    "wagtaildraftsharing",  # has to come before wagtail.admin due to template overriding; also needs wagtail.snippets
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "csp",
    # Local apps
    "bedrock.base",
    "bedrock.cms",  # Wagtail-based CMS bases
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
    "bedrock.security",
    "bedrock.releasenotes",
    "bedrock.contentcards",
    "bedrock.contentful",
    "bedrock.utils",
    "bedrock.wordpress",
    "bedrock.sitemaps",
    "bedrock.careers",
    # last so that redirects here will be last
    "bedrock.redirects",
    # libs
    "django_extensions",
    "lib.l10n_utils",
    "django_rq",
    "django_rq_email_backend",
    "mozilla_django_oidc",  # needs to be loaded after django.contrib.auth
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


def _is_bedrock_custom_app(app_name):
    return app_name.startswith("bedrock.")


TEMPLATES = [
    {
        "BACKEND": "django_jinja.jinja2.Jinja2",
        "APP_DIRS": False,
        "DIRS": [f"bedrock/{name.split('.')[1]}/templates" for name in INSTALLED_APPS if _is_bedrock_custom_app(name)],
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
                "bedrock.mozorg.context_processors.current_year",
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
                "wagtail.jinja2tags.core",
                "wagtail.images.jinja2tags.images",
            ],
        },
    },
    {
        # Wagtail needs the standard Django template backend
        # https://docs.wagtail.org/en/stable/reference/jinja2.html#configuring-django
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": [
            "bedrock/admin/templates",
        ],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
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

BASKET_URL = config("BASKET_URL", default="https://basket.mozilla.org")
BASKET_API_KEY = config("BASKET_API_KEY", default="")
BASKET_TIMEOUT = config("BASKET_TIMEOUT", parser=int, default="10")
BASKET_SUBSCRIBE_URL = f"{BASKET_URL}/news/subscribe/"

BOUNCER_URL = config("BOUNCER_URL", default="https://download.mozilla.org/")

# Use a message storage mechanism that doesn't need a database.
# This can be changed to use session once we do add a database.
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

default_email_backend = "django.core.mail.backends.smtp.EmailBackend"
if DEBUG:
    default_email_backend = "django.core.mail.backends.console.EmailBackend"
elif TASK_QUEUE_AVAILABLE is True:
    default_email_backend = "django_rq_email_backend.backends.RQEmailBackend"

DEFAULT_FROM_EMAIL = "Mozilla.com <noreply@mozilla.com>"

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

DONATE_LINK = "https://foundation.mozilla.org/{location}"

# Official Firefox Instagram accounts
MOZILLA_INSTAGRAM_ACCOUNTS = {
    "en-US": "https://www.instagram.com/mozilla/",
    "de": "https://www.instagram.com/mozilla_deutschland/",
}

# Mozilla accounts product links
# ***This URL *MUST* end in a traling slash!***
FXA_ENDPOINT = config("FXA_ENDPOINT", default="https://accounts.stage.mozaws.net/" if DEV else "https://accounts.firefox.com/")

# Google Play and Apple App Store settings
from .appstores import (  # noqa: E402, F401
    AMAZON_FIREFOX_FIRE_TV_LINK,
    APPLE_APPSTORE_COUNTRY_MAP,
    APPLE_APPSTORE_FIREFOX_LINK,
    APPLE_APPSTORE_FOCUS_LINK,
    APPLE_APPSTORE_KLAR_LINK,
    APPLE_APPSTORE_VPN_LINK,
    GOOGLE_PLAY_FIREFOX_BETA_LINK,
    GOOGLE_PLAY_FIREFOX_LINK,
    GOOGLE_PLAY_FIREFOX_LINK_UTMS,
    GOOGLE_PLAY_FIREFOX_NIGHTLY_LINK,
    GOOGLE_PLAY_FIREFOX_SEND_LINK,
    GOOGLE_PLAY_FOCUS_LINK,
    GOOGLE_PLAY_KLAR_LINK,
    GOOGLE_PLAY_VPN_LINK,
    MICROSOFT_WINDOWS_STORE_FIREFOX_BETA_DIRECT_LINK,
    MICROSOFT_WINDOWS_STORE_FIREFOX_BETA_WEB_LINK,
    MICROSOFT_WINDOWS_STORE_FIREFOX_DIRECT_LINK,
    MICROSOFT_WINDOWS_STORE_FIREFOX_WEB_LINK,
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
    default="1" if DEV is True else "10",
    parser=float,
)

RELEASE_NOTES_PATH = config("RELEASE_NOTES_PATH", default=data_path("release_notes"))
RELEASE_NOTES_REPO = config("RELEASE_NOTES_REPO", default="https://github.com/mozilla/release-notes.git")
RELEASE_NOTES_BRANCH = config("RELEASE_NOTES_BRANCH", default="master")

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
        "mozilla_django_oidc": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

# DisallowedHost gets a lot of action thanks to scans/bots/scripts,
# but we need not take any action because it's already HTTP 400-ed.
# Note that we ignore at the Sentry client level
ignore_logger("django.security.DisallowedHost")

PASSWORD_HASHERS = ["django.contrib.auth.hashers.PBKDF2PasswordHasher"]
ADMINS = MANAGERS = config("ADMINS", parser=json.loads, default="[]")

GTM_CONTAINER_ID = config("GTM_CONTAINER_ID", default="")

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
        integrations=[DjangoIntegration(), RedisIntegration(), RqIntegration()],
        before_send=before_send,
    )

# Frontend uses the same DSN as backend by default, but we'll
# specify a separate one for FE use in Production only
SENTRY_FRONTEND_DSN = config("SENTRY_FRONTEND_DSN", default=SENTRY_DSN)

# Statsd metrics via markus
if DEBUG or config("DISABLE_LOCAL_MARKUS", default="false", parser=bool):
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

# Countries that need to see cookie banner
# See https://www.gov.uk/eu-eea

DATA_CONSENT_COUNTRIES = [
    "AT",  # Austria
    "BE",  # Belgium
    "BG",  # Bulgaria
    "HR",  # Croatia
    "CY",  # Republic of Cyprus
    "CZ",  # Czech Republic
    "DK",  # Denmark
    "EE",  # Estonia
    "FI",  # Finland
    "FR",  # France
    "DE",  # Germany
    "GR",  # Greece
    "HU",  # Hungary
    "IE",  # Ireland
    "IS",  # Iceland
    "IT",  # Italy
    "LV",  # Latvia
    "LI",  # Liechtenstein
    "LT",  # Lithuania
    "LU",  # Luxembourg
    "MT",  # Malta
    "NL",  # Netherlands
    "NO",  # Norway
    "PL",  # Poland
    "PT",  # Portugal
    "RO",  # Romania
    "SK",  # Slovakia
    "SI",  # Slovenia
    "ES",  # Spain
    "SE",  # Sweden
    "CH",  # Switzerland
    "GB",  # United Kingdom
]

# VPN ==========================================================================================

# URL for Mozilla VPN sign-in links
# ***This URL *MUST* end in a traling slash!***
VPN_ENDPOINT = config("VPN_ENDPOINT", default="https://stage.guardian.nonprod.cloudops.mozgcp.net/" if DEV else "https://vpn.mozilla.org/")

# URL for Mozilla VPN subscription links
# ***This URL *MUST* end in a traling slash!***
VPN_SUBSCRIPTION_URL = config("VPN_SUBSCRIPTION_URL", default="https://accounts.stage.mozaws.net/" if DEV else "https://accounts.firefox.com/")

# New URL for VPN subscription links
# ***This URL *MUST* end in a trailing slash!***
VPN_SUBSCRIPTION_URL_NEXT = config(
    "VPN_SUBSCRIPTION_URL_NEXT", default="https://payments-next.stage.fxa.nonprod.webservices.mozgcp.net/" if DEV else "https://payments.firefox.com/"
)

# For testing/QA we support a test 'daily' API endpoint on the staging API only
VPN_SUBSCRIPTION_USE_DAILY_MODE__QA_ONLY = config("VPN_SUBSCRIPTION_USE_DAILY_MODE__QA_ONLY", default="False", parser=bool)

# Product ID for VPN subscriptions
VPN_PRODUCT_ID = config("VPN_PRODUCT_ID", default="prod_FiJ42WCzZNRSbS" if DEV else "prod_FvnsFHIfezy3ZI")
VPN_PRODUCT_ID_NEXT = "mozillavpnstage" if DEV else "vpn"

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

# Simplified pricing matrix for countries that can
# only purchase a subscription through the app store.
VPN_MOBILE_SUB_PRICING = {
    "AU": {  # Australia
        "12-month": {
            "price": "7.5",
            "total": "89.99",
            "currency": "AUD",
        },
        "monthly": {
            "price": "14.99",
            "currency": "AUD",
        },
    },
    "BD": {  # Bangladesh
        "12-month": {
            "price": "583.33",
            "total": "7000",
            "currency": "BDT",
        },
        "monthly": {
            "price": "1200",
            "currency": "BDT",
        },
    },
    "BR": {  # Brazil
        "12-month": {
            "price": "27.50",
            "total": "330",
            "currency": "BRL",
        },
        "monthly": {
            "price": "56",
            "currency": "BRL",
        },
    },
    "CL": {  # Chile
        "12-month": {
            "price": "4582.50",
            "total": "54990",
            "currency": "CLP",
        },
        "monthly": {
            "price": "9300",
            "currency": "CLP",
        },
    },
    "CO": {  # Colombia
        "12-month": {
            "price": "20825",
            "total": "249900",
            "currency": "COP",
        },
        "monthly": {
            "price": "41900",
            "currency": "COP",
        },
    },
    "EG": {  # Egypt
        "12-month": {
            "price": "241.67",
            "total": "2899.99",
            "currency": "EGP",
        },
        "monthly": {
            "price": "479.99",
            "currency": "EGP",
        },
    },
    "GR": {  # Greece
        "12-month": {
            "price": "4.99",
            "total": "59.88",
            "currency": "EUR",
        },
        "monthly": {
            "price": "9.99",
            "currency": "EUR",
        },
    },
    "ID": {  # Indonesia
        "12-month": {
            "price": "75000",
            "total": "900000",
            "currency": "IDR",
        },
        "monthly": {
            "price": "155000",
            "currency": "IDR",
        },
    },
    "IN": {  # India
        "12-month": {
            "price": "416.58",
            "total": "4999",
            "currency": "INR",
        },
        "monthly": {
            "price": "839",
            "currency": "INR",
        },
    },
    "KE": {  # Kenya
        "12-month": {
            "price": "5.00",
            "total": "59.99",
            "currency": "USD",
        },
        "monthly": {
            "price": "9.99",
            "currency": "USD",
        },
    },
    "KR": {  # South Korea
        "12-month": {
            "price": "6658.33",
            "total": "79900",
            "currency": "KRW",
        },
        "monthly": {
            "price": "13500",
            "currency": "KRW",
        },
    },
    "MA": {  # Morocco
        "12-month": {
            "price": "50",
            "total": "600",
            "currency": "MAD",
        },
        "monthly": {
            "price": "99",
            "currency": "MAD",
        },
    },
    "MX": {  # Mexico
        "12-month": {
            "price": "95.75",
            "total": "1149",
            "currency": "MXN",
        },
        "monthly": {
            "price": "189",
            "currency": "MXN",
        },
    },
    "NG": {  # Nigeria
        "12-month": {
            "price": "8325",
            "total": "99900",
            "currency": "NGN",
        },
        "monthly": {
            "price": "15900",
            "currency": "NGN",
        },
    },
    "NO": {  # Norway
        "12-month": {
            "price": "54.17",
            "total": "650",
            "currency": "NOK",
        },
        "monthly": {
            "price": "110",
            "currency": "NOK",
        },
    },
    "SA": {  # Saudi Arabia
        "12-month": {
            "price": "18.75",
            "total": "224.99",
            "currency": "SAR",
        },
        "monthly": {
            "price": "36.99",
            "currency": "SAR",
        },
    },
    "SN": {  # Senegal
        "12-month": {
            "price": "4.99",
            "total": "59.88",
            "currency": "USD",
        },
        "monthly": {
            "price": "9.99",
            "currency": "USD",
        },
    },
    "TH": {  # Thailand
        "12-month": {
            "price": "165.83",
            "total": "1990",
            "currency": "THB",
        },
        "monthly": {
            "price": "330",
            "currency": "THB",
        },
    },
    "TR": {  # Turkey
        "12-month": {
            "price": "166.67",
            "total": "1999.99",
            "currency": "TRY",
        },
        "monthly": {
            "price": "339.99",
            "currency": "TRY",
        },
    },
    "TW": {  # Taiwan
        "12-month": {
            "price": "158.33",
            "total": "1900",
            "currency": "TWD",
        },
        "monthly": {
            "price": "320",
            "currency": "TWD",
        },
    },
    "UA": {  # Ukraine
        "12-month": {
            "price": "5.00",
            "total": "59.99",
            "currency": "USD",
        },
        "monthly": {
            "price": "9.99",
            "currency": "USD",
        },
    },
    "UG": {  # Uganda
        "12-month": {
            "price": "4.99",
            "total": "59.88",
            "currency": "USD",
        },
        "monthly": {
            "price": "9.99",
            "currency": "USD",
        },
    },
    "US": {  # United States (only used as a fallback should a country match not be found).
        "12-month": {
            "price": "4.99",
            "total": "59.88",
            "currency": "USD",
        },
        "monthly": {
            "price": "9.99",
            "currency": "USD",
        },
    },
    "VN": {  # Vietnam
        "12-month": {
            "price": "124917",
            "total": "1499000",
            "currency": "VND",
        },
        "monthly": {
            "price": "249000",
            "currency": "VND",
        },
    },
    "ZA": {  # South Africa
        "12-month": {
            "price": "83.33",
            "total": "999.99",
            "currency": "ZAR",
        },
        "monthly": {
            "price": "169.99",
            "currency": "ZAR",
        },
    },
}

# Mozilla VPN Geo restrictions
# https://github.com/mozilla-services/guardian-website/blob/master/server/constants.ts

# Countries where VPN is available for subscription via desktop (FxA) or mobile app stores.
VPN_COUNTRY_CODES = [
    "CA",  # Canada
    "MY",  # Malaysia
    "NZ",  # New Zealand
    "SG",  # Singapore
    # United Kingdom + "Territories"
    "GB",  # United Kingdom of Great Britain and Northern Ireland
    "GG",  # Guernsey (a British Crown dependency)
    "IM",  # Isle of Man (a British Crown dependency)
    "IO",  # British Indian Ocean Territory
    "JE",  # Jersey (a British Crown dependency)
    "VG",  # Virgin Islands (British)
    # USA + "Territories"
    "AS",  # American Samoa
    "MP",  # Northern Mariana Islands
    "PR",  # Puerto Rico
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

# Countries where VPN is available but subscriptions are only available through mobile app stores.
VPN_MOBILE_SUB_COUNTRY_CODES = [
    "AU",  # Australia
    "BD",  # Bangladesh
    "BR",  # Brazil
    "CL",  # Chile
    "CO",  # Colombia
    "EG",  # Egypt
    "GR",  # Greece
    "ID",  # Indonesia
    "IN",  # India
    "KE",  # Kenya
    "KR",  # South Korea
    "MA",  # Morocco
    "MX",  # Mexico
    "NG",  # Nigeria
    "NO",  # Norway
    "SA",  # Saudi Arabia
    "SN",  # Senegal
    "TH",  # Thailand
    "TR",  # Turkey
    "TW",  # Taiwan
    "UA",  # Ukraine
    "UG",  # Uganda
    "VN",  # Viet Nam
    "ZA",  # South Africa
]

# Countries where VPN is available for subscription only via Google Play Store.
VPN_MOBILE_SUB_ANDROID_ONLY_COUNTRY_CODES = [
    "BD",  # Bangladesh
    "BR",  # Brazil
    "MA",  # Morocco
    "SN",  # Senegal
]

VPN_AVAILABLE_COUNTRIES = 57
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

# List of locales that are supported in the Mozilla VPN client application.
VPN_SUPPORTED_LOCALES = [
    "co",
    "cs",
    "cy",
    "da",
    "de",
    "dsb",
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
    "ko",
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
    "vi",
    "zh",
]

# RELAY =========================================================================================

RELAY_PRODUCT_URL = config(
    "RELAY_PRODUCT_URL", default="https://stage.fxprivaterelay.nonprod.cloudops.mozgcp.net/" if DEV else "https://relay.firefox.com/"
)

# VPN, Monitor, and Relay bundle ====================================================================

# Product ID for VPN, Monitor, and Relay bundle subscriptions.
VPN_MONITOR_RELAY_BUNDLE_PRODUCT_ID = config("VPN_MONITOR_RELAY_BUNDLE_PRODUCT_ID", default="prod_SFb8iVuZIOPREe" if DEV else "prod_SOYBYCOWallcgz")

# VPN, Monitor, and Relay bundle plan IDs by currency/language.
VPN_MONITOR_RELAY_BUNDLE_PLAN_ID_MATRIX = {
    "usd": {
        "en": {
            "12-month": {
                "id": "price_1RMAopKb9q6OnNsLSGe1vLtt" if DEV else "price_1RTl5CJNcmPzuWtRVETtMFUX",
                "price": "8.25",
                "total": "99",
                "currency": "USD",
                "saving": 40,
                "analytics": {
                    "brand": "vpn",
                    "plan": "vpn + monitor + relay",
                    "currency": "USD",
                    "discount": "80.88",
                    "price": "99",
                    "period": "yearly",
                },
            },
        }
    },
}

# Map of country codes to allocated VPN Monitor, and Relay bundle currency/language plan IDs.
VPN_MONITOR_RELAY_BUNDLE_PRICING = {
    "US": {
        "default": VPN_MONITOR_RELAY_BUNDLE_PLAN_ID_MATRIX["usd"]["en"],
    },
}

# Countries where VPN Monitor, and Relay bundle is available.
VPN_MONITOR_RELAY_BUNDLE_COUNTRY_CODES = [
    "US",  # United States of America
]

# Authentication with Mozilla OpenID Connect / Auth0 ============================================

LOGIN_ERROR_URL = "/cms-admin/"
LOGIN_REDIRECT_URL_FAILURE = "/cms-admin/"
LOGIN_REDIRECT_URL = "/cms-admin/"
LOGOUT_REDIRECT_URL = "/cms-admin/"

OIDC_RP_SIGN_ALGO = "RS256"

# How frequently do we check with the provider that the user still exists and is authorised?
OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = config(
    "OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS",
    default="64800",  # 18 hours
    parser=int,
)

OIDC_CREATE_USER = False  # We don't want drive-by signups

OIDC_RP_CLIENT_ID = config("OIDC_RP_CLIENT_ID", default="")
OIDC_RP_CLIENT_SECRET = config("OIDC_RP_CLIENT_SECRET", default="")

OIDC_OP_AUTHORIZATION_ENDPOINT = "https://auth.mozilla.auth0.com/authorize"
OIDC_OP_TOKEN_ENDPOINT = "https://auth.mozilla.auth0.com/oauth/token"
OIDC_OP_USER_ENDPOINT = "https://auth.mozilla.auth0.com/userinfo"
OIDC_OP_DOMAIN = "auth.mozilla.auth0.com"
OIDC_OP_JWKS_ENDPOINT = "https://auth.mozilla.auth0.com/.well-known/jwks.json"

# If True (which should only be for local work in your .env), then show
# username and password fields when signing up, not the SSO button
USE_SSO_AUTH = config("USE_SSO_AUTH", default="true", parser=bool)

if USE_SSO_AUTH:
    AUTHENTICATION_BACKENDS = (
        # Deliberately OIDC only, else no entry by any other means
        "mozilla_django_oidc.auth.OIDCAuthenticationBackend",
    )
else:
    AUTHENTICATION_BACKENDS = (
        # Regular username + password auth
        "django.contrib.auth.backends.ModelBackend",
    )

# Note that AUTHENTICATION_BACKENDS is overridden in tests, so take care
# to check/amend those if you add additional auth backends

# Extra Wagtail config to disable password usage (SSO should be the only route)
# https://docs.wagtail.org/en/v4.2.4/reference/settings.html#wagtail-password-management-enabled
# Don't let users change or reset their password
if USE_SSO_AUTH:
    WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = False
    WAGTAIL_PASSWORD_RESET_ENABLED = False

    # Don't require a password when creating a user,
    # and blank password means cannot log in unless via SSO
    WAGTAILUSERS_PASSWORD_ENABLED = False

# Custom CSRF failure view to show custom CSRF messaging, which is
# more likely to appear with SSO auth enabled, when sessions expire
CSRF_FAILURE_VIEW = "bedrock.base.views.csrf_failure"

# WAGTAIL =======================================================================================

WAGTAIL_SITE_NAME = config("WAGTAIL_SITE_NAME", default="Mozilla.org")

# Disable use of Gravatar URLs.
# Important: if this is enabled in the future, make sure you redact the
# `wagtailusers_profile.avatar` column when exporting the DB to sqlite
WAGTAIL_GRAVATAR_PROVIDER_URL = None

WAGTAILADMIN_BASE_URL = config("WAGTAILADMIN_BASE_URL", default="")

# We're sticking to LTS releases of Wagtail, so we don't want to be told there's a new version if that's not LTS
WAGTAIL_ENABLE_UPDATE_CHECK = False

# Custom setting (not a Wagtail core one) that we use to plug in/unplug the admin UI entirely
WAGTAIL_ENABLE_ADMIN = config("WAGTAIL_ENABLE_ADMIN", default="false", parser=bool)

if WAGTAIL_ENABLE_ADMIN:
    # Enable Middleware essential for admin

    INSTALLED_APPS += [
        # django.contrib.admin needs SessionMiddleware and AuthenticationMiddleware to be specced, and fails
        # hard if it's in INSTALLED_APPS when they are not, so we have to defer adding it till here
        "django.contrib.admin",
        # wagtail_localize_smartling > 0.10 needs django.contrib.humanize
        "django.contrib.humanize",
    ]

    for midddleware_spec in [
        "mozilla_django_oidc.middleware.SessionRefresh",  # In case someone has their Auth0 revoked while logged in, revalidate it
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
    ]:
        MIDDLEWARE.insert(3, midddleware_spec)

    SUPPORTED_NONLOCALES.extend(
        [
            "cms-admin",
            "django-admin",
            "django-rq",
            "oidc",
            "_internal_draft_preview",
        ]
    )

    # Increase the number of form fields allowed to be submitted in one GET/POST,
    # but only for deployments where the CMS is enabled. This is needed to support
    # complex pages with lots of (small, but) nested fields.
    # Resolves https://mozilla.sentry.io/issues/5800147294
    DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000


def lazy_wagtail_langs():
    enabled_wagtail_langs = [
        # Notes:
        # 1) The labels are only used internally so can be in English
        # 2) These are the Bedrock-side lang codes. They are mapped to
        # Smartling-specific ones in the WAGTAIL_LOCALIZE_SMARTLING settings, below
        ("en-US", "English (US)"),
        ("de", "German"),
        ("fr", "French"),
        ("es-ES", "Spanish (Spain)"),
        ("it", "Italian"),
        ("ja", "Japanese"),
        ("nl", "Dutch (Netherlands)"),
        ("pl", "Polish"),
        ("pt-BR", "Portuguese (Brazil)"),
        ("ru", "Russian"),
        ("zh-CN", "Chinese (China-Simplified)"),
    ]
    enabled_language_codes = [x[0] for x in LANGUAGES]
    retval = [wagtail_lang for wagtail_lang in enabled_wagtail_langs if wagtail_lang[0] in enabled_language_codes]
    return retval


WAGTAIL_I18N_ENABLED = True
WAGTAIL_CONTENT_LANGUAGES = lazy(lazy_wagtail_langs, list)()

# Don't automatically make a page for a non-default locale availble in the default locale
WAGTAILLOCALIZE_SYNC_LIVE_STATUS_ON_TRANSLATE = False  # note that WAGTAILLOCALIZE is correct without the _

# Settings for https://github.com/mozilla/wagtail-localize-smartling
WAGTAIL_LOCALIZE_SMARTLING = {
    # Required settings (get these from "Account settings" > "API" in the Smartling dashboard)
    "PROJECT_ID": config("WAGTAIL_LOCALIZE_SMARTLING_PROJECT_ID", default="setme"),
    "USER_IDENTIFIER": config("WAGTAIL_LOCALIZE_SMARTLING_USER_IDENTIFIER", default="setme"),
    "USER_SECRET": config("WAGTAIL_LOCALIZE_SMARTLING_USER_SECRET", default="setme"),
    # Optional settings and their default values
    "REQUIRED": config(
        "WAGTAIL_LOCALIZE_SMARTLING_ALWAYS_SEND",
        default="false",
        parser=bool,
    ),  # Set this to True to always send translations to Smartling
    "ENVIRONMENT": config(
        "WAGTAIL_LOCALIZE_SMARTLING_ENVIRONMENT",
        default="production",
        parser=ChoiceOf(str, ["production", "staging"]),
    ),  # Set this to "staging" to use Smartling's staging API
    "API_TIMEOUT_SECONDS": config(
        "WAGTAIL_LOCALIZE_SMARTLING_API_TIMEOUT_SECONDS",
        default="5",
        parser=float,
    ),  # Timeout in seconds for requests to the Smartling API
    "LOCALE_TO_SMARTLING_LOCALE": {
        "de": "de-DE",
        "fr": "fr-FR",
        "it": "it-IT",
        "ja": "ja-JP",
        "nl": "nl-NL",
        "pl": "pl-PL",
        "ru": "ru-RU",
    },
    "JOB_NAME_PREFIX": config(
        "WAGTAIL_LOCALIZE_JOB_NAME_PREFIX",
        default="www.mozilla.org",
    ),
    "REFORMAT_LANGUAGE_CODES": False,  # don't force language codes into Django's all-lowercase pattern
    "VISUAL_CONTEXT_CALLBACK": "bedrock.cms.wagtail_localize_smartling.callbacks.visual_context",
}

WAGTAILDRAFTSHARING = {
    "ADMIN_MENU_POSITION": 9000,
    # MAX_TTL: 14 * 24 * 60 * 60
    # VERBOSE_NAME: "Internal Share"
    # VERBOSE_NAME_PLURAL: "Internal Shares"
    # MENU_ITEM_LABEL: "Create internal sharing link"
}


# Custom settings, not a core Wagtail ones, to scope out RichText options
WAGTAIL_RICHTEXT_FEATURES_FULL = [
    # https://docs.wagtail.org/en/stable/advanced_topics/customisation/page_editing_interface.html#limiting-features-in-a-rich-text-field
    # Order here is the order used in the editor UI
    "h2",
    "h3",
    "hr",
    "bold",
    "italic",
    "code",
    "blockquote",
    "superscript",
    "link",
    "ol",
    "ul",
    "image",
]

WAGTAIL_RICHTEXT_FEATURES_MINIMAL = [
    # https://docs.wagtail.org/en/stable/advanced_topics/customisation/page_editing_interface.html#limiting-features-in-a-rich-text-field
    # Order here is the order used in the editor UI
    "bold",
    "italic",
    "link",
    "ol",
    "ul",
]

WAGTAILIMAGES_IMAGE_MODEL = "cms.BedrockImage"

WAGTAILIMAGES_EXTENSIONS = [
    "gif",
    "jpg",
    "jpeg",
    "png",
    "webp",
    "svg",
]

# Custom code in bedrock.cms.models.base.AbstractBedrockCMSPage limits what page
# models can be added as a child page.
#
# This means we can control when a page is available for use in the CMS, versus
# simply being in the codebase. Also, note that removing a particular page class
# from this allowlist will not break existing pages that are of that class, but
# will stop anyone adding a _new_ one.
#
# NB: EVERY TIME you add a new Wagtail Page subclass to the CMS, you must enable
# it here if you want it to be selectable as a new child page in Production
#
# You must ALSO consider if they need to be added to the DB export script. If
# they are not, they will not be fully exported to the sqlite DB, which
# may break things like demos and integration tests. See bin/export-db-to-sqlite.sh

_allowed_page_models = [
    "cms.SimpleRichTextPage",
    "cms.StructuralPage",
    "mozorg.LeadershipPage",
    "products.VPNResourceCenterDetailPage",
    "products.VPNResourceCenterIndexPage",
    "products.MonitorArticleIndexPage",
    "products.MonitorArticlePage",
]

if DEV is True:
    CMS_ALLOWED_PAGE_MODELS = ["__all__"]
else:
    CMS_ALLOWED_PAGE_MODELS = _allowed_page_models


# Our use of django-waffle relies on the following 2 settings to be set this way so that if a switch
# doesn't exist, we get `None` back from `switch_is_active`.
WAFFLE_SWITCH_DEFAULT = None
WAFFLE_CREATE_MISSING_SWITCHES = False

if config("ENABLE_WAGTAIL_STYLEGUIDE", parser=bool, default="False"):
    # Useful when customising the Wagtail admin
    # when enabled, will be visible on cms-admin/styleguide
    INSTALLED_APPS.append("wagtail.contrib.styleguide")

# Django-silk for performance profiling
if ENABLE_DJANGO_SILK := config("ENABLE_DJANGO_SILK", default="False", parser=bool):
    print("Django-Silk profiling enabled - go to http://localhost:8000/silk/ to view metrics")
    INSTALLED_APPS.append("silk")
    MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")
    SUPPORTED_NONLOCALES.append("silk")
    SILKY_PYTHON_PROFILER = config("SILKY_PYTHON_PROFILER", default="False", parser=bool)

# Config for redirection of certain pages over to www.firefox.com - if you override this,
# be sure NOT to include `locale` - we add that in the redirects as and when needed
# NOTE THE LACK OF TRAILING SLASH, too - this is deliberate and should be followed
FXC_BASE_URL = config("FXC_BASE_URL", default="https://www.firefox.com")

ENABLE_FIREFOX_COM_REDIRECTS = config(
    "ENABLE_FIREFOX_COM_REDIRECTS",
    default="True",
    parser=bool,
)

MAKE_FIREFOX_COM_REDIRECTS_PERMANENT = ENABLE_FIREFOX_COM_REDIRECTS and config(
    "MAKE_FIREFOX_COM_REDIRECTS_PERMANENT",
    default="True",
    parser=bool,
)
