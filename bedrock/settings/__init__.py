# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging.config
import sys

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
POCKET_SITE_MODE = "Pocket"
MOZORG_SITE_MODE = "Mozorg"

site_mode = config("SITE_MODE", default=MOZORG_SITE_MODE)

IS_POCKET_MODE = site_mode == POCKET_SITE_MODE
IS_MOZORG_MODE = not IS_POCKET_MODE

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
        # TODO: check whether redundant when we have real translations flowing in to Bedrock
        "en-US": "en",
        "en-GB": "en",
        "en-CA": "en",
        "es-ES": "es-ES",
        "es-la": "es",  # NB: es-LA isn't a real locale, but it is what getpocket.com has used and we need to deal with it
    }

    FALLBACK_LOCALES = {
        # TODO: double-check for correctness when we have real translations flowing in to Bedrock
        # "es" is the fallback for non-Spain Spanish, not for "es-ES"
        "es-CL": "es",
        "es-MX": "es",
        "es-AR": "es",
    }

    PROD_LANGUAGES = [
        # TODO: double-check for correctness and completeness
        # when we have real translations from the vendor
        "de",
        "en",
        "es",
        "es-ES",
        "fr-CA",
        "fr",
        "it",
        "ja",
        "ko",
        "nl",
        "pl",
        "pt-BR",
        "pt-PT",
        "ru",
        "zh-CN",
        "zh-TW",
    ]

    # No reason to have separate Dev and Prod lang sets for Pocket mode
    DEV_LANGUAGES = PROD_LANGUAGES
    LANGUAGE_CODE = "en"  # Pocket uses `en` not `en-US`

else:
    ROOT_URLCONF = "bedrock.urls.mozorg_mode"

# TEST-SPECIFIC SETTINGS
# TODO: make this selectable by an env var, like the other modes
if (len(sys.argv) > 1 and sys.argv[1] == "test") or "pytest" in sys.modules:

    # Using the CachedStaticFilesStorage for tests breaks all the things.
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    # TEMPLATE_DEBUG has to be True for Jinja to call the template_rendered
    # signal which Django's test client uses to save away the contexts for your
    # test to look at later.
    TEMPLATES[0]["OPTIONS"]["debug"] = True
    # use default product-details data
    PROD_DETAILS_STORAGE = "product_details.storage.PDFileStorage"

    DATABASES["default"] = {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}

sys.stdout.write(f"Using SITE_MODE of '{site_mode}'\n")
