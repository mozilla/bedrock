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

# CSP settings for MOZORG, expanded upon later:
_csp_default_src = [
    csp.constants.SELF,
    "*.mozilla.net",
    "*.mozilla.org",
    "*.mozilla.com",
]
_csp_img_src = [
    "data:",
    "www.googletagmanager.com",
    "www.google-analytics.com",
    "images.ctfassets.net",
]
_csp_script_src = [
    # TODO change settings so we don't need unsafes even in dev
    csp.constants.UNSAFE_INLINE,
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
extra_csp_default_src = config("CSP_DEFAULT_SRC", default="", parser=ListOf(str, allow_empty=False))
if extra_csp_default_src:
    _csp_default_src = list(set(_csp_default_src + extra_csp_default_src))
if DEV:
    if _csp_connect_extra_for_dev:
        _csp_connect_src = list(set(_csp_connect_src + _csp_connect_extra_for_dev))
_csp_child_src = list(set(_csp_default_src + _csp_child_src))
csp_extra_frame_src = config("CSP_EXTRA_FRAME_SRC", default="", parser=ListOf(str, allow_empty=False))
if csp_extra_frame_src:
    _csp_child_src = list(set(_csp_child_src + csp_extra_frame_src))
csp_report_uri = config("CSP_REPORT_URI", default="") or None
csp_ro_report_uri = config("CSP_RO_REPORT_URI", default="") or None

CONTENT_SECURITY_POLICY = {
    # Default report percentage to 1% just in case the env var isn't set, we don't want to bombard Sentry.
    "REPORT_PERCENTAGE": config("CSP_REPORT_PERCENTAGE", default="1.0", parser=float),
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
        "report-uri": csp_report_uri,
    },
}

# Only set up report-only CSP if we have a report-uri set.
CONTENT_SECURITY_POLICY_REPORT_ONLY = None
if csp_ro_report_uri:
    # Copy CSP and override report-uri for report-only.
    CONTENT_SECURITY_POLICY_REPORT_ONLY = deepcopy(CONTENT_SECURITY_POLICY)
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["report-uri"] = csp_ro_report_uri

    # CSP directive updates we're testing that we hope to move to the enforced policy.
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["default-src"] = [csp.constants.SELF]
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["media-src"] = [csp.constants.SELF, "assets.mozilla.net", "videos.cdn.mozilla.net"]
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["object-src"] = [csp.constants.NONE]
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["frame-ancestors"] = [csp.constants.NONE]
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["style-src"].remove(csp.constants.UNSAFE_INLINE)
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["upgrade-insecure-requests"] = True
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["base-uri"] = [csp.constants.NONE]
    # For `form-action`, include a trailing slash to avoid CSP's "exact match" path-part rules, unless exact matching is intended.
    CONTENT_SECURITY_POLICY_REPORT_ONLY["DIRECTIVES"]["form-action"] = [csp.constants.SELF, f"{BASKET_URL}/news/", FXA_ENDPOINT]


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

if csp_ro_report_uri:
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
