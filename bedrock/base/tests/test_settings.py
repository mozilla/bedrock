# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Tests for settings"""

from django.conf import settings
from django.test import override_settings

import pytest

from bedrock.settings.base import _get_media_cdn_hostname_for_storage_backend


@override_settings(DEV=False, PROD_LANGUAGES=("de", "fr", "nb-NO", "ja", "ja-JP-mac", "en-US", "en-GB"))
def test_lang_groups():
    # should not contain 'nb' and 'ja' group should contain 'ja'
    assert dict(settings.LANG_GROUPS) == {
        "ja": ["ja-JP-mac", "ja"],
        "en": ["en-US", "en-GB"],
    }


@pytest.mark.parametrize(
    "media_url, expected_hostname",
    (
        ("https://www-dev.allizom.org/media/cms/", "https://www-dev.allizom.org"),
        ("https://www-dev.allizom.org/some/future/assets/path/", "https://www-dev.allizom.org"),
        ("https://www.allizom.org/media/cms/", "https://www.allizom.org"),
        ("https://www.mozilla.org/media/cms/", "https://www.mozilla.org"),
        ("/custom-media/", "/custom-media/"),  # this one is the default, used in local dev
    ),
)
def test_get_media_cdn_hostname(media_url, expected_hostname):
    assert _get_media_cdn_hostname_for_storage_backend(media_url) == expected_hostname
