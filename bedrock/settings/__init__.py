# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging.config
import sys
from copy import deepcopy

import csp.constants

from .base import *  # noqa: F403, F405

# This file:
# 1. Handles setting specific settings based on the site Bedrock is serving - currently Mozorg or Pocket
# 2. Tweaks some settings if Django can detect we're running tests
# 3. django_csp settings
# 4. Sets a number of general settings applicable to all site modes

# 1. OPERATION MODE SELECTION and specific config
# Which site do we want Bedrock to serve?

# IS_POCKET_MODE and IS_MOZORG_MODE are set in settings.base

if IS_POCKET_MODE:
    ROOT_URLCONF = "bedrock.urls.pocket_mode"

    # DROP the redirects app and middleware, because they contain Mozorg-specific
    # rules that clash with some Pocket URL paths (eg /jobs/)
    INSTALLED_APPS.pop(INSTALLED_APPS.index("bedrock.redirects"))
    MIDDLEWARE.pop(MIDDLEWARE.index("bedrock.redirects.middleware.RedirectsMiddleware"))

    # Override the FLUENT_* config for Pocket mode

    FLUENT_DEFAULT_FILES = [
        "brands",
        "nav",
        "footer",
    ]

    # The following lines do two things, both related to L10N and Pocket.
    #
    # 1) For Pocket mode, we don't need an intermediary mozmeao repo to hold translations while
    # we calculate activation metadata via CI (which does happen for Mozorg). Why? All locales
    # in Pocket are translated by a vendor, so should be 100% ready to go. This means that both
    # FLUENT_REPO and FLUENT_L10N_TEAM_REPO can point to the same git repo.
    #
    # 2) Pocket-specific config has already been defined in settings/base.py (for other reasons),
    # so here we can use those existing POCKET_FLUENT_* values to override our regular FLUENT_*
    # defaults. This means the L10N mechanics don't need to include any Pocket-related code
    # branching and just work on whatever the configured repos and directories are.

    FLUENT_REPO = FLUENT_L10N_TEAM_REPO = POCKET_FLUENT_REPO
    FLUENT_REPO_URL = FLUENT_L10N_TEAM_REPO_URL = POCKET_FLUENT_REPO_URL
    FLUENT_REPO_BRANCH = FLUENT_L10N_TEAM_REPO_BRANCH = POCKET_FLUENT_REPO_BRANCH
    FLUENT_REPO_PATH = FLUENT_L10N_TEAM_REPO_PATH = POCKET_FLUENT_REPO_PATH

    # Note: No need to redefine FLUENT_REPO_AUTH - we'll use the same for Pocket mode as for Mozorg mode

    # Redefine the FLUENT_LOCAL_PATH for a Pocket-specific one and
    # ensure it is the first one we check, because order matters.
    FLUENT_LOCAL_PATH = ROOT_PATH / "l10n-pocket"
    FLUENT_PATHS = [
        # local FTL files
        FLUENT_LOCAL_PATH,
        # remote FTL files from l10n team
        FLUENT_REPO_PATH,
    ]

    CANONICAL_LOCALES = {
        # Pocket uses mostly region-less locales, but these will be automatically selected by Bedrock
        # e.g. /de-DE/ -> /de/ via a 302
    }

    FALLBACK_LOCALES = {
        # Not needed in Bedrock
    }

    PROD_LANGUAGES = [
        # Note that all of Pocket's locale strings are lowercase - and mixed case is HTTP 301ed
        # to lowercase versions. We are retaining this behaviour for legacy consistency and SEO
        "de",
        "en",
        "es",  # We map es-ES to this in `l10n-pocket/configs/smartling-config.json`
        "es-la",  # Not an ISO locale, but a locale-like convention; remapped in vendor config
        "fr-ca",
        "fr",
        "it",
        "ja",
        "ko",
        "nl",
        "pl",
        "pt-br",
        "pt",  # mapped from "pt-PT"
        "ru",
        "zh-cn",
        "zh-tw",
    ]

    # No reason to have separate Dev and Prod lang sets for Pocket mode
    DEV_LANGUAGES = PROD_LANGUAGES
    LANGUAGE_CODE = "en"  # Pocket uses `en` not `en-US`

    # Pocket mode doesn't need language names available for a lang picker, so we can just do this
    # rather than fish around in product_details.languages. This is extra-handy because Pocket Mode
    # uses language codes that don't all appear in product_details.languages
    LANGUAGES = [(lang, lang) for lang in PROD_LANGUAGES]

    # We don't want any fallback lang support for Pocket mode, so let's override the Bedrock base default
    LANGUAGE_URL_MAP_WITH_FALLBACKS = LANGUAGE_URL_MAP

    COOKIE_CONSENT_SCRIPT_SRC = "https://cdn.cookielaw.org/scripttemplates/otSDKStub.js"
    COOKIE_CONSENT_DATA_DOMAIN = "a7ff9c31-9f59-421f-9a8e-49b11a3eb24e-test" if DEV else "a7ff9c31-9f59-421f-9a8e-49b11a3eb24e"

    SNOWPLOW_APP_ID = "pocket-web-mktg-dev" if DEV else "pocket-web-mktg"
    SNOWPLOW_SCRIPT_SRC = "https://assets.getpocket.com/web-utilities/public/static/te-3.1.2.js"
    SNOWPLOW_CONNECT_URL = "com-getpocket-prod1.mini.snplow.net" if DEV else "getpocket.com"

    # CSP settings for POCKET, expanded upon later:
    _csp_default_src = [
        csp.constants.SELF,
        "*.getpocket.com",
    ]
    _csp_img_src = [
        "data:",
        "www.mozilla.org",
        "www.googletagmanager.com",
        "www.google-analytics.com",
        "cdn.cookielaw.org",  # See https://github.com/mozilla/bedrock/issues/14118
    ]
    _csp_script_src = [
        # TODO fix use of OptanonWrapper() so that we don't need this
        csp.constants.UNSAFE_INLINE,
        # TODO onetrust cookie consent breaks
        # blocked without unsafe-eval. Find a way to remove that.
        "www.mozilla.org",
        csp.constants.UNSAFE_EVAL,
        "www.googletagmanager.com",
        "www.google-analytics.com",
        "cdn.cookielaw.org",
        "assets.getpocket.com",  # allow Pocket Snowplow analytics
    ]
    _csp_style_src = [
        csp.constants.UNSAFE_INLINE,
        "www.mozilla.org",
    ]
    _csp_child_src = [
        "www.googletagmanager.com",
    ]
    _csp_connect_src = [
        "www.googletagmanager.com",
        "www.google-analytics.com",
        "region1.google-analytics.com",
        "o1069899.sentry.io",
        "o1069899.ingest.sentry.io",
        "cdn.cookielaw.org",
        "privacyportal.onetrust.com",
        "getpocket.com",  # Pocket Snowplow
        "geolocation.onetrust.com",
    ]
    _csp_connect_extra_for_dev = [
        "com-getpocket-prod1.mini.snplow.net",
    ]
    _csp_font_src = []

else:
    # Mozorg mode
    ROOT_URLCONF = "bedrock.urls.mozorg_mode"

    # CSP settings for MOZORG, expanded upon later:
    _csp_default_src = [
        csp.constants.SELF,
        "*.mozilla.net",
        "*.mozilla.org",
        "*.mozilla.com",
    ]
    _csp_img_src = [
        "data:",
        "mozilla.org",
        "www.googletagmanager.com",
        "www.google-analytics.com",
        "creativecommons.org",
        "images.ctfassets.net",
    ]
    _csp_script_src = [
        # TODO fix things so that we don't need this
        csp.constants.UNSAFE_INLINE,
        # TODO snap.svg.js passes a string to Function() which is
        # blocked without unsafe-eval. Find a way to remove that.
        csp.constants.UNSAFE_EVAL,
        "www.googletagmanager.com",
        "www.google-analytics.com",
        "tagmanager.google.com",
        "www.youtube.com",
        "s.ytimg.com",
        "js.stripe.com",
    ]
    _csp_style_src = [
        # TODO fix things so that we don't need this
        csp.constants.UNSAFE_INLINE,
    ]
    _csp_child_src = [
        "www.googletagmanager.com",
        "www.google-analytics.com",
        "accounts.firefox.com",
        "www.youtube.com",
        "js.stripe.com",
    ]
    _csp_connect_src = [
        "www.googletagmanager.com",
        "www.google-analytics.com",
        "region1.google-analytics.com",
        "sentry.prod.mozaws.net",  # DEPRECATED. TODO: remove this once all sites are talking to sentry.io instead
        "o1069899.sentry.io",
        "o1069899.ingest.sentry.io",
        FXA_ENDPOINT,
        "stage.cjms.nonprod.cloudops.mozgcp.net",
        "cjms.services.mozilla.com",
    ]
    _csp_connect_extra_for_dev = []
    _csp_font_src = []

sys.stdout.write(f"Using SITE_MODE of '{site_mode}'\n")

# 2. TEST-SPECIFIC SETTINGS
# TODO: make this selectable by an env var, like the other modes
if (len(sys.argv) > 1 and sys.argv[1] == "test") or "pytest" in sys.modules:
    # Using the CachedStaticFilesStorage for tests breaks all the things.
    STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.StaticFilesStorage"
    # TEMPLATE_DEBUG has to be True for Jinja to call the template_rendered
    # signal which Django's test client uses to save away the contexts for your
    # test to look at later.
    TEMPLATES[0]["OPTIONS"]["debug"] = True
    # use default product-details data
    PROD_DETAILS_STORAGE = "product_details.storage.PDFileStorage"

    DATABASES["default"] = {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}


# 3. DJANGO-CSP SETTINGS
extra_csp_default_src = config("CSP_DEFAULT_SRC", default="", parser=ListOf(str))
if extra_csp_default_src:
    _csp_default_src = list(set(_csp_default_src + extra_csp_default_src))
if DEV:
    if _csp_connect_extra_for_dev:
        _csp_connect_src = list(set(_csp_connect_src + _csp_connect_extra_for_dev))
_csp_child_src = list(set(_csp_default_src + _csp_child_src))
csp_extra_frame_src = config("CSP_EXTRA_FRAME_SRC", default="", parser=ListOf(str))
if csp_extra_frame_src:
    _csp_child_src = list(set(_csp_child_src + csp_extra_frame_src))

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": _csp_default_src,
        "img-src": list(set(_csp_default_src + _csp_img_src)),
        "script-src": list(set(_csp_default_src + _csp_script_src)),
        "style-src": list(set(_csp_default_src + _csp_style_src)),
        "font-src": list(set(_csp_default_src + _csp_font_src)),
        "child-src": _csp_child_src,
        "connect-src": list(set(_csp_default_src + _csp_connect_src)),
        # support older browsers (mainly Safari)
        "frame-src": _csp_child_src,
    },
}
# Only set up report-only CSP if we have a report-uri set.
if csp_report_uri := config("CSP_REPORT_URI", default="") or None:
    CONTENT_SECURITY_POLICY_REPORT_ONLY = deepcopy(CONTENT_SECURITY_POLICY)
    # Add reporting.
    CONTENT_SECURITY_POLICY_REPORT_ONLY["REPORT_PERCENTAGE"] = config("CSP_REPORT_PERCENTAGE", default="100", parser=int)
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["report-uri"] = csp_report_uri
    # CSP directive updates we're testing that we hope to move to the enforced policy.
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["frame-ancestors"] = [csp.constants.NONE]
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["style-src"].remove(csp.constants.UNSAFE_INLINE)


# `CSP_PATH_OVERRIDES` and `CSP_PATH_OVERRIDES_REPORT_ONLY` are mainly for overriding CSP settings
# for CMS admin, but can override other paths.  Works in conjunction with the
# `bedrock.base.middleware.CSPMiddlewareByPathPrefix` middleware.


def _override_csp(csp, append: dict[str, list[str]] = None, replace: dict[str, list[str]] = None):
    csp = deepcopy(csp)

    if append is not None:
        for key, value in append.items():
            if key in csp["DIRECTIVES"]:
                value = csp["DIRECTIVES"][key] + value
            csp["DIRECTIVES"][key] = value

    if replace is not None:
        for key, value in replace.items():
            csp["DIRECTIVES"][key] = value

    return csp


# Path based overrides.
# /cms-admin/images/ loads just-uploaded images as blobs.
CMS_ADMIN_IMAGES_CSP = _override_csp(CONTENT_SECURITY_POLICY, append={"img-src": ["blob:"]})

CSP_PATH_OVERRIDES = {
    # Order them from most specific to least.
    "/cms-admin/images/": CMS_ADMIN_IMAGES_CSP,
}

if csp_report_uri:
    # Path based overrides for report-only CSP.
    CMS_ADMIN_CSP_RO = _override_csp(CONTENT_SECURITY_POLICY_REPORT_ONLY, replace={"frame-ancestors": [csp.constants.SELF]})
    CMS_ADMIN_IMAGES_CSP_RO = _override_csp(CONTENT_SECURITY_POLICY_REPORT_ONLY, append={"img-src": ["blob:"]})

    CSP_PATH_OVERRIDES_REPORT_ONLY = {
        # Order them from most specific to least.
        "/cms-admin/images/": CMS_ADMIN_IMAGES_CSP_RO,
        "/cms-admin/": CMS_ADMIN_CSP_RO,
    }

# 4. SETTINGS WHICH APPLY REGARDLESS OF SITE MODE
if DEV:
    ALLOWED_HOSTS = ["*"]
else:
    MIDDLEWARE += ["bedrock.base.middleware.FrameOptionsHeader"]


if CACHES["default"]["BACKEND"] == "django_pylibmc.memcached.PyLibMCCache":
    CACHES["default"]["BINARY"] = True
    CACHES["default"]["OPTIONS"] = {  # Maps to pylibmc "behaviors"
        "tcp_nodelay": True,
        "ketama": True,
    }

# cache for Fluent files
CACHES["fluent"] = {
    "BACKEND": "bedrock.base.cache.SimpleDictCache",
    "LOCATION": "fluent",
    "TIMEOUT": FLUENT_CACHE_TIMEOUT,
    "OPTIONS": {
        "MAX_ENTRIES": 5000,
        "CULL_FREQUENCY": 4,  # 1/4 entries deleted if max reached
    },
}

# cache for product details
CACHES["product-details"] = {
    "BACKEND": "bedrock.base.cache.SimpleDictCache",
    "LOCATION": "product-details",
    "OPTIONS": {
        "MAX_ENTRIES": 200,  # currently 104 json files
        "CULL_FREQUENCY": 4,  # 1/4 entries deleted if max reached
    },
}

# cache for release notes
CACHES["release-notes"] = {
    "BACKEND": "bedrock.base.cache.SimpleDictCache",
    "LOCATION": "release-notes",
    "TIMEOUT": 5,
    "OPTIONS": {
        "MAX_ENTRIES": 300,  # currently 564 json files but most are rarely accessed
        "CULL_FREQUENCY": 4,  # 1/4 entries deleted if max reached
    },
}

# cache for externalfiles
CACHES["externalfiles"] = {
    "BACKEND": "bedrock.base.cache.SimpleDictCache",
    "LOCATION": "externalfiles",
    "OPTIONS": {
        "MAX_ENTRIES": 10,  # currently 2 files
        "CULL_FREQUENCY": 4,  # 1/4 entries deleted if max reached
    },
}

# cache for generated QR codes
CACHES["qrcode"] = {
    "BACKEND": "bedrock.base.cache.SimpleDictCache",
    "LOCATION": "qrcode",
    "TIMEOUT": None,
    "OPTIONS": {
        "MAX_ENTRIES": 20,
        "CULL_FREQUENCY": 4,  # 1/4 entries deleted if max reached
    },
}

MEDIA_URL = CDN_BASE_URL + MEDIA_URL
STATIC_URL = CDN_BASE_URL + STATIC_URL
logging.config.dictConfig(LOGGING)
