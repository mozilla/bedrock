# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test import override_settings
from django.urls import URLResolver

import pytest

from bedrock.base.i18n import (
    LocalePrefixPattern,
    bedrock_i18n_patterns,
    check_for_bedrock_language,
    get_best_language,
    get_language_from_headers,
    normalize_language,
    path_needs_lang_code,
    split_path_and_normalize_language,
)
from lib.l10n_utils import translation


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
        # misses/no matches
        ("dude", None),
        ("the-DUDE", None),
        ("xx", None),
        ("dq", None),
    ),
)
def test_normalize_language_mozorg_mode(lang_code, expected):
    assert normalize_language(lang_code) == expected


@pytest.mark.parametrize(
    "path, expected",
    (
        ("media", False),
        ("static", False),
        ("images", False),
        ("credits", False),
        ("robots.txt", False),
        (".well-known", False),
        ("telemetry", False),
        ("webmaker", False),
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
        ("/all-urls-global.xml", False),
        ("/all-urls.xml", False),
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
def test_split_path_and_normalize_language(path, result):
    res = split_path_and_normalize_language(path)
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


@override_settings(LANGUAGE_CODE="en-GB")
def test_local_prefix_pattern_fallback_mode():
    pattern = LocalePrefixPattern(prefix_default_language=False)
    assert pattern.language_prefix == ""


@pytest.mark.parametrize(
    "lang_code, expected_result",
    (
        ("en-US", True),
        ("fr", True),
        ("sco", True),
        ("hsb", True),
        ("ach", False),
        ("de", False),
    ),
)
@override_settings(
    LANGUAGES=[
        ("en-US", "English"),
        ("fr", "French"),
        ("sco", "Scots"),
        ("hsb", "Hornjoserbsce"),
    ]
)
def test_check_for_bedrock_language(lang_code, expected_result):
    assert check_for_bedrock_language(lang_code) == expected_result


@pytest.mark.parametrize("use_i18n", (True, False))
def test_bedrock_i18n_patterns(use_i18n):
    from bedrock.careers import urls as career_urls

    with override_settings(USE_I18N=use_i18n):
        patterns = bedrock_i18n_patterns(career_urls)
    if use_i18n:
        assert isinstance(patterns[0], URLResolver)
    else:
        assert patterns[0] == career_urls


@pytest.mark.parametrize(
    "headers, expected",
    (
        ({"HTTP_ACCEPT_LANGUAGE": "sco,de-DE;q=0.8,fr;q=0.6,en-GB;q=0.4,en-US;q=0.2"}, "sco"),
        ({"HTTP_ACCEPT_LANGUAGE": "fr,de-DE;q=0.8,sco;q=0.6,en-GB;q=0.4,en-US;q=0.2"}, "fr"),
        ({"HTTP_ACCEPT_LANGUAGE": "es-mx,es-es;q=0.8"}, "es-MX"),
        ({"HTTP_ACCEPT_LANGUAGE": "de-AT,de;q=0.8,sco;q=0.6,en-GB;q=0.4,en-US;q=0.2"}, "de"),
        ({}, "en-US"),
    ),
)
def test_get_language_from_headers(rf, headers, expected):
    request = rf.get("/", **headers)
    assert get_language_from_headers(request) == expected


@override_settings(DEV=False)
@pytest.mark.parametrize(
    "header, expected",
    (
        ("sco,de-DE;q=0.8,fr;q=0.6,en-GB;q=0.4,en-US;q=0.2", "sco"),
        ("fr,de-DE;q=0.8,sco;q=0.6,en-GB;q=0.4,en-US;q=0.2", "fr"),
        ("es-at,es-es;q=0.8", "es-ES"),
        ("de-AT,de;q=0.8,sco;q=0.6,en-GB;q=0.4,en-US;q=0.2", "de"),
        ("am", None),
        ("", None),
    ),
)
def test_get_best_language(header, expected):
    assert get_best_language(header) == expected
