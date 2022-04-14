# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging.config
import sys

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa

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

# cache for lang files
CACHES["l10n"] = {
    "BACKEND": "bedrock.base.cache.SimpleDictCache",
    "LOCATION": "l10n",
    "TIMEOUT": DOTLANG_CACHE,
    "OPTIONS": {
        "MAX_ENTRIES": 5000,
        "CULL_FREQUENCY": 4,  # 1/4 entries deleted if max reached
    },
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

# OPERATION MODE SELECTION
# Which site do we want Bedrock to serve?
DEFAULT_SITE_MODE = "Default"
POCKET_SITE_MODE = "Pocket"
MOZORG_SITE_MODE = "Mozorg"

site_mode = config("SITE_MODE", default=DEFAULT_SITE_MODE)

if site_mode == MOZORG_SITE_MODE:
    ROOT_URLCONF = "bedrock.urls_mozorg_mode"
elif site_mode == POCKET_SITE_MODE:
    ROOT_URLCONF = "bedrock.urls_pocket_mode"
    # TODO: from settings.pocket import *
    # to switch in Pocket-appropriate versions of
    # DEV_LANGUAGES, PROD_LANGUAGES, CANONICAL_LOCALES,
    # FLUENT_* overrides for Pocket L10N, etc
    # (The import from settings.pocket is just one option)
elif site_mode == DEFAULT_SITE_MODE:
    # For now, the default behaviour should not be changed
    # TODO: remove this option once Pocket mode is in production AND
    # we've made Mozorg mode an explicit mode for production, too
    ROOT_URLCONF = "bedrock.urls"
else:
    raise ImproperlyConfigured(f"SITE_MODE of '{site_mode}' not recognised, so cannot run")

# TEST-SPECIFIC SETTINGS
# TODO: make this selectable by an env var, like the other modes
if (len(sys.argv) > 1 and sys.argv[1] == "test") or "pytest" in sys.modules:

    # Ensure we have all URLs available for tests
    ROOT_URLCONF = "bedrock.urls"

    # Using the CachedStaticFilesStorage for tests breaks all the things.
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    # TEMPLATE_DEBUG has to be True for Jinja to call the template_rendered
    # signal which Django's test client uses to save away the contexts for your
    # test to look at later.
    TEMPLATES[0]["OPTIONS"]["debug"] = True
    # use default product-details data
    PROD_DETAILS_STORAGE = "product_details.storage.PDFileStorage"

    DATABASES["default"] = {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}

sys.stdout.write(f"Using SITE_MODE of '{site_mode}' and ROOT_URLCONF of '{ROOT_URLCONF}'\n")
