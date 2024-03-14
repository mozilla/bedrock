# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test import override_settings

import pytest

from bedrock.base.i18n import (
    LocalePrefixPattern,
    normalize_language,
    path_needs_lang_code,
    split_path_and_polish_lang,
)
from lib.l10n_utils import translation


@override_settings(IS_MOZORG_MODE=True, IS_POCKET_MODE=False)
@pytest.mark.parametrize(
    "lang_code, expected",
    (
        (None, None),
        ("", None),
        # General normalization
        ("EN-US", "en-US"),
        ("en-US", "en-US"),
        ("eN-gB", "en-GB"),
        ("ja-jp-mac", "ja"),
        ("JA-JP-MAC", "ja"),
        # from CANONICAL_LOCALES
        ("en", "en-US"),
        ("es", "es-ES"),
        ("ja-JP-mac", "ja"),
        ("no", "nb-NO"),
        ("pt", "pt-BR"),
        ("sv", "sv-SE"),
        # mixed/ideal case
        ("zh-Hant", "zh-TW"),
        ("zh-Hant-TW", "zh-TW"),
        ("zh-HK", "zh-TW"),
        ("zh-Hant-HK", "zh-TW"),
        # all lowercase
        ("zh-hant", "zh-TW"),
        ("zh-hant-tw", "zh-TW"),
        ("zh-hk", "zh-TW"),
        ("zh-hant-hk", "zh-TW"),
        # lowercase country
        ("zh-Hant", "zh-TW"),
        ("zh-Hant-tw", "zh-TW"),
        ("zh-hk", "zh-TW"),
        ("zh-Hant-hk", "zh-TW"),
        # lowercase middle part
        ("zh-Hant-TW", "zh-TW"),
        ("zh-hant-HK", "zh-TW"),
    ),
)
def test_normalize_language_mozorg_mode(lang_code, expected):
    assert normalize_language(lang_code) == expected


@override_settings(
    IS_MOZORG_MODE=False,
    IS_POCKET_MODE=True,
    LANGUAGE_URL_MAP_WITH_FALLBACKS={
        # patch in what we set in settings.__init__
        "de": "de",
        "en": "en",
        "es": "es",
        "es-la": "es-la",
        "fr-ca": "fr-ca",
        "fr": "fr",
        "it": "it",
        "ja": "ja",
        "ko": "ko",
        "nl": "nl",
        "pl": "pl",
        "pt-br": "pt-br",
        "pt": "pt",
        "ru": "ru",
        "zh-cn": "zh-cn",
        "zh-tw": "zh-tw",
    },
)
@pytest.mark.parametrize(
    "lang_code, expected",
    (
        (None, None),
        ("", None),  # General normalization
        ("de", "de"),
        ("de-DE", "de"),
        ("DE", "de"),
        ("en", "en"),
        ("en-US", "en"),
        ("EN", "en"),
        ("es", "es"),
        ("ES", "es"),
        ("es-la", "es-la"),
        ("es-LA", "es-la"),
        ("ES-LA", "es-la"),
        ("fr-ca", "fr-ca"),
        ("fr-CA", "fr-ca"),
        ("FR-CA", "fr-ca"),
        ("fr", "fr"),
        ("FR", "fr"),
        ("it", "it"),
        ("IT", "it"),
        ("ja", "ja"),
        ("JA", "ja"),
        ("ko", "ko"),
        ("KO", "ko"),
        ("nl", "nl"),
        ("NL", "nl"),
        ("pl", "pl"),
        ("PL", "pl"),
        ("pt-br", "pt-br"),
        ("pt-BR", "pt-br"),
        ("PT-BR", "pt-br"),
        ("pt", "pt"),
        ("PT", "pt"),
        ("pt-PT", "pt"),
        ("PT-PT", "pt"),
        ("ru", "ru"),
        ("RU", "ru"),
        ("zh-cn", "zh-cn"),
        ("zh-CN", "zh-cn"),
        ("ZH-CN", "zh-cn"),
        ("zh-tw", "zh-tw"),
        ("zh-TW", "zh-tw"),
        ("ZH-TW", "zh-tw"),
    ),
)
def test_normalize_language_pocket_mode(lang_code, expected):
    assert normalize_language(lang_code) == expected


# @override_settings(LANGUAGE_URL_MAP={"es-ar": "es-AR", "en-gb": "en-GB", "es-us": "es-US"}, CANONICAL_LOCALES={"es": "es-ES", "en": "en-US"})
# class TestFindSupported(TestCase):
#     def test_find_supported(self):
#         assert find_supported("en-CA") == "en-US"
#         assert find_supported("en-US") == "en-US"
#         assert find_supported("en-GB") == "en-GB"
#         assert find_supported("en") == "en-US"
#         assert find_supported("es-MX") == "es-ES"
#         assert find_supported("es-AR") == "es-AR"
#         assert find_supported("es") == "es-ES"

#     def test_find_supported_none(self):
#         """
#         Should return None if it can't find any supported locale.
#         """
#         assert find_supported("de") is None
#         assert find_supported("fr") is None
#         assert find_supported("dude") is None


@pytest.mark.parametrize(
    "path, expected",
    (
        ("media", False),
        ("static", False),
        ("certs", False),
        ("images", False),
        ("contribute.json", False),
        ("credits", False),
        ("gameon", False),
        ("robots.txt", False),
        (".well-known", False),
        ("telemetry", False),
        ("webmaker", False),
        ("contributor-data", False),
        ("healthz", False),
        ("readiness", False),
        ("healthz-cron", False),
        ("2004", False),
        ("2005", False),
        ("2006", False),
        ("keymaster", False),
        ("microsummaries", False),
        ("xbl", False),
        ("revision.txt", False),
        ("locales", False),
        ("/sitemap_none.xml", False),
        ("/sitemap.xml", False),
        # Some example paths that do need them
        ("/about/", True),
        ("about", True),
        ("/products/", True),
        ("products/", True),
        ("security/some/path/here", True),
        # Note that NOT needing a lang string is based on affirmation, so anything
        # that isn't affirmed (e.g. cos it already has a lang code) is a default True
        ("/en-US/products/", True),
    ),
)
def test_path_needs_lang_code(path, expected):
    assert path_needs_lang_code(path) == expected


@pytest.mark.parametrize(
    "path, result",
    [
        # Basic
        (
            "en-US/some/action",
            ("en-US", "some/action", False),
        ),
        # First slash doesn't matter
        ("/en-US/some/action", ("en-US", "some/action", False)),
        # Nor does capitalization, but it counts as a 'changed' code
        ("En-uS/some/action", ("en-US", "some/action", True)),
        # Unsupported languages return a blank language
        ("unsupported/sOmE/action", ("", "unsupported/sOmE/action", False)),
        # Fallback to a lang-only lang code, not a territory
        ("de-AT/test", ("de", "test", True)),
        # Unicode handling + polishing of locale
        ("fR-Ca/François/test", ("fr", "François/test", True)),
    ],
)
def test_split_path_and_polish_lang(path, result):
    res = split_path_and_polish_lang(path)
    assert res == result


@pytest.mark.parametrize(
    "language_to_activate, expected_prefix",
    (
        ("en-US", "en-US/"),  # perfect fit
        ("en-us", "en-US/"),  # case fixup
        ("de", "de/"),  # perfect fit
        ("de-AT", "de/"),  # lang-code-only fallback fit
        ("", "en-US/"),  # default/fallback
        (None, "en-US/"),  # default/fallback
        ("abc", "en-US/"),  # default/fallback
    ),
)
def test_locale_prefix_pattern_works(language_to_activate, expected_prefix):
    pattern = LocalePrefixPattern()

    if language_to_activate:
        translation.activate(language_to_activate)

    assert pattern.language_prefix == expected_prefix
    translation.deactivate()
