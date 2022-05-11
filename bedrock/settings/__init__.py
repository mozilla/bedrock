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

    # Note that for Pocket mode, we don't need an intermediary mozmeao/* repo to hold the translations
    # while we calculate activation metadata via a CI task (which does happen for Mozorg). Why? All
    # locales in Pocket should be 100% ready to go, because they are translated by a vendor, whereas
    # Mozorg has community translation contributions as well, which aren't always exhaustive.
    #
    # As a result, both FLUENT_REPO and FLUENT_L10N_TEAM_REPO point to the same git repo

    FLUENT_REPO = config("POCKET_FLUENT_REPO", default="mozilla-l10n/pocket-www-l10n")
    FLUENT_REPO_URL = f"https://github.com/{FLUENT_REPO}"
    FLUENT_REPO_BRANCH = config("POCKET_FLUENT_REPO_BRANCH", default="main")
    FLUENT_REPO_PATH = DATA_PATH / "pocket-www-l10n"

    FLUENT_L10N_TEAM_REPO = config("POCKET_FLUENT_L10N_TEAM_REPO", default="mozilla-l10n/pocket-www-l10n")
    FLUENT_L10N_TEAM_REPO_URL = f"https://github.com/{FLUENT_L10N_TEAM_REPO}"
    FLUENT_L10N_TEAM_REPO_BRANCH = config("POCKET_FLUENT_L10N_TEAM_REPO_BRANCH", default="main")
    FLUENT_L10N_TEAM_REPO_PATH = DATA_PATH / "l10n-pocket-team"

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

    DEV_LANGUAGES = get_dev_languages(
        fluent_repo_path=FLUENT_REPO_PATH,
        ignore_lang_dirs=IGNORE_LANG_DIRS,
        prod_languages=PROD_LANGUAGES,
    )
    DEV_LANGUAGES.append("en")

    CANONICAL_LOCALES = {
        # TODO: check whether redundant
        "en-US": "en",
        "en-GB": "en",
        "en-CA": "en",
        "es-ES": "es-ES",  # TODO: check whether redundant
        "es-CL": "es",
        "es-MX": "es",
    }

    FALLBACK_LOCALES = {
        "es-AR": "es",
        "es-CL": "es",
        "es-MX": "es",
    }

    PROD_LANGUAGES = [
        "de",
        "en",
        "es-AR",
        "es-CL",
        "es-ES",
        "es-MX",
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
