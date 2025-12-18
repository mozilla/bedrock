# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging.config
import sys
from copy import deepcopy

import csp.constants

from .base import *  # noqa: F403, F405

# This file:
# 1. Handles setting specific settings based on the site Bedrock is serving - currently Mozorg
# 2. Tweaks some settings if Django can detect we're running tests
# 3. django_csp settings
# 4. Sets a number of general settings applicable to all site modes


ROOT_URLCONF = "bedrock.urls"

# CSP settings, expanded upon later:
# NOTE: We are providing all settings to django-csp as sets, not lists.
# - This is for de-duping, and because django-csp will convert them to `sorted` lists for us.

# NOTE: For any URLs that contain a path, not just the origin, trailing slashes are important.
# - if no path is provided, all resources are allowed from the origin.
# - if path is provided with no trailing slash: an exact-match is required.
#   - e.g. `https://example.com/api` will only match `https://example.com/api`
# - if path is provided with trailing slash: the path is a prefix-match.
#   - e.g. `https://example.com/api/` will match anything that starts with `https://example.com/api/`

# Add the host for front-end assets which is needed during integration tests or when someone is
# accessing the origin directly instead of the CDN.
CSP_ASSETS_HOST = config("CSP_ASSETS_HOST", default="")

_csp_default_src = {
    # NOTE: Keep `default-src` minimal. Best to set resources in the specific directives.
    csp.constants.SELF,
}
_csp_connect_src = {
    csp.constants.SELF,
    # NOTE: Check if these need to be in the `_csp_form_action` list as well since we often
    # progressively enhance forms by using Javascript.
    "o1069899.ingest.sentry.io",
    "o1069899.sentry.io",
    "region1.google-analytics.com",
    "telemetry.transcend.io",  # Transcend Consent Management
    "telemetry.us.transcend.io",  # Transcend Consent Management
    "cdn.transcend.io",  # Transcend Consent Management
    "transcend-cdn.com",  # Transcend Consent Management
    "www.google-analytics.com",
    "www.googletagmanager.com",
    # This is for glean pings and deletion requests.
    "www.mozilla.org/submit/bedrock/",
    BASKET_URL,
    FXA_ENDPOINT,
    FOUNDATION_URL,
}
_csp_font_src = {
    csp.constants.SELF,
    CSP_ASSETS_HOST,
}
_csp_form_action = {
    csp.constants.SELF,
    # NOTE: Check if these need to be in the `_csp_connect_src` list as well since we often
    # progressively enhance forms by using Javascript.
    BASKET_URL,
    FXA_ENDPOINT,
    FOUNDATION_URL,
}
# On hosts with wagtail admin enabled, we need to allow the admin to frame itself for previews.
_csp_frame_ancestors = {
    csp.constants.SELF if WAGTAIL_ENABLE_ADMIN else csp.constants.NONE,
}
_csp_frame_src = {
    csp.constants.SELF,
    "accounts.firefox.com",
    "js.stripe.com",
    "www.google-analytics.com",
    "www.googletagmanager.com",
    "www.youtube.com",
}
_csp_img_src = {
    csp.constants.SELF,
    CSP_ASSETS_HOST,
    "data:",
    "blog.mozilla.org",  # For careers pages.
    "www.mozilla.org",  # For release notes.
    "www.googletagmanager.com",
    "www.google-analytics.com",
    "images.ctfassets.net",
}
_csp_media_src = {
    csp.constants.SELF,
    CSP_ASSETS_HOST,
    "assets.mozilla.net",
    "videos.cdn.mozilla.net",
}
_csp_script_src = {
    csp.constants.SELF,
    CSP_ASSETS_HOST,
    "cdn.transcend.io",  # Transcend Consent Management
    "js.stripe.com",
    "s.ytimg.com",
    "tagmanager.google.com",
    "transcend-cdn.com",  # Transcend Consent Management
    "www.google-analytics.com",
    "www.googletagmanager.com",
    "www.youtube.com",
    csp.constants.UNSAFE_EVAL,
    csp.constants.UNSAFE_INLINE,
}
_csp_style_src = {
    csp.constants.SELF,
    CSP_ASSETS_HOST,
    csp.constants.UNSAFE_INLINE,
    "cdn.transcend.io",  # Transcend Consent Management
    "transcend-cdn.com",  # Transcend Consent Management
}

# Transcend Consent Management UI uses CSS-in-JS which requires inline styles.
if TRANSCEND_AIRGAP_URL:  # noqa: F405
    _csp_style_src.add(csp.constants.UNSAFE_INLINE)

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

    # If we're using sqlite, run tests on an in-memory version, else use the configured default DB engine
    if DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3":
        DATABASES["default"] = {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}


# 3. DJANGO-CSP SETTINGS
if csp_extra_default_src := config("CSP_DEFAULT_SRC", default="", parser=ListOf(str, allow_empty=False)):
    _csp_default_src |= set(csp_extra_default_src)
if csp_extra_frame_src := config("CSP_EXTRA_FRAME_SRC", default="", parser=ListOf(str, allow_empty=False)):
    _csp_frame_src |= set(csp_extra_frame_src)
csp_report_uri = config("CSP_REPORT_URI", default="") or None
csp_ro_report_uri = config("CSP_RO_REPORT_URI", default="") or None

CONTENT_SECURITY_POLICY = {
    # Default report percentage to 1% just in case the env var isn't set, we don't want to bombard Sentry.
    "REPORT_PERCENTAGE": config("CSP_REPORT_PERCENTAGE", default="1.0", parser=float),
    "DIRECTIVES": {
        "default-src": _csp_default_src,
        "base-uri": {csp.constants.NONE},
        "connect-src": _csp_connect_src,
        "font-src": _csp_font_src,
        "form-action": _csp_form_action,
        "frame-ancestors": _csp_frame_ancestors,
        "frame-src": _csp_frame_src,
        "img-src": _csp_img_src,
        "media-src": _csp_media_src,
        "object-src": {csp.constants.NONE},
        "script-src": _csp_script_src,
        "style-src": _csp_style_src,
        "upgrade-insecure-requests": False if DEBUG else True,
        "report-uri": csp_report_uri,
    },
}

# Only set up report-only CSP if we have a report-uri set.
CONTENT_SECURITY_POLICY_REPORT_ONLY = None
if csp_ro_report_uri:
    # Copy CSP and override report-uri for report-only.
    CONTENT_SECURITY_POLICY_REPORT_ONLY = deepcopy(CONTENT_SECURITY_POLICY)
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["report-uri"] = csp_ro_report_uri


# `CSP_PATH_OVERRIDES` and `CSP_PATH_OVERRIDES_REPORT_ONLY` are mainly for overriding CSP settings
# for CMS admin, but can override other paths.  Works in conjunction with the
# `bedrock.base.middleware.CSPMiddlewareByPathPrefix` middleware.


def _override_csp(
    csp: dict[str, dict[str, set[str]]],
    append: dict[str, set[str]] = None,
    replace: dict[str, set[str]] = None,
) -> dict[str, dict[str, set[str]]]:
    # Don't modify the original CSP settings.
    csp = deepcopy(csp)

    if append is not None:
        for key, value in append.items():
            csp["DIRECTIVES"][key] = csp["DIRECTIVES"].get(key, set()) | value

    if replace is not None:
        for key, value in replace.items():
            csp["DIRECTIVES"][key] = value

    return csp


#
# Path based overrides.
#

# /cms-admin/images/ loads just-uploaded images as blobs.
CMS_ADMIN_IMAGES_CSP = _override_csp(CONTENT_SECURITY_POLICY, append={"img-src": {"blob:"}})
CMS_ADMIN_IMAGES_CSP_RO = csp_ro_report_uri and _override_csp(CONTENT_SECURITY_POLICY_REPORT_ONLY, append={"img-src": {"blob:"}})
# The CMS admin frames itself for page previews.
CMS_ADMIN_CSP = _override_csp(CONTENT_SECURITY_POLICY, replace={"frame-ancestors": {csp.constants.SELF}})
CMS_ADMIN_CSP_RO = csp_ro_report_uri and _override_csp(CONTENT_SECURITY_POLICY_REPORT_ONLY, replace={"frame-ancestors": {csp.constants.SELF}})

CSP_PATH_OVERRIDES = {
    # Order them from most specific to least.
    "/cms-admin/images/": CMS_ADMIN_IMAGES_CSP,
    "/cms-admin/": CMS_ADMIN_CSP,
}

# Path based overrides for report-only CSP.
if csp_ro_report_uri:
    CSP_PATH_OVERRIDES_REPORT_ONLY = {
        # Order them from most specific to least.
        "/cms-admin/images/": CMS_ADMIN_IMAGES_CSP_RO,
        "/cms-admin/": CMS_ADMIN_CSP_RO,
    }

# 4. SETTINGS WHICH APPLY REGARDLESS OF SITE MODE
if not DEV:
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
