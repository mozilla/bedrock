# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from bedrock.base.i18n import split_path_and_polish_lang


def test_normalize_language():
    assert False, "WRITE ME, incl ja-JP-mac case"


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


def test_find_supported():
    assert False, "WRITE ME"


def test_path_needs_lang_code():
    assert False, "WRITE ME"


@pytest.mark.parametrize(
    "path, result",
    [
        # Basic
        ("en-US/some/action", ("en-US", "some/action")),
        # First slash doesn't matter
        ("/en-US/some/action", ("en-US", "some/action")),
        # Nor does capitalization
        ("En-uS/some/action", ("en-US", "some/action")),
        # Unsupported languages return a blank language
        ("unsupported/some/action", ("", "unsupported/some/action")),
        # Unicode handling
        ("fR-Ca/Françoi/test", ("fr-CA", "Fran%C3%A7oi/test")),
    ],
)
def test_split_path(path, result):
    res = split_path_and_polish_lang(path)
    assert res == result


def test_locale_prefix_pattern():
    assert False, "WRITE ME AND SEE HOW SUMO TESTS THIS."
    # Handle:
    # default/none-specified,
    # perfect fit
    # lang-code-only fallback fit
    # total miss

    # Old prefixer tests covered:
    # assert prefixer.get_best_language("en") == "en-US"
    # assert prefixer.get_best_language("en-CA") == "en-US"
    # assert prefixer.get_best_language("en-GB") == "en-GB"
    # assert prefixer.get_best_language("en-US") == "en-US"
    # assert prefixer.get_best_language("es") == "es-ES"
    # assert prefixer.get_best_language("es-AR") == "es-AR"
    # assert prefixer.get_best_language("es-CL") == "es-ES"
    # assert prefixer.get_best_language("es-MX") == "es-ES"
