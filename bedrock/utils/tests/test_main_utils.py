# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test import override_settings

from bedrock.utils import expand_locale_groups


@override_settings(LANG_GROUPS={"en": ["en-US", "en-GB"]})
def test_expand_locale_groups():
    assert expand_locale_groups(["de", "fr", "en-GB"]) == ["de", "fr", "en-GB"]
    assert expand_locale_groups(["de", "fr", "en"]) == ["de", "fr", "en-US", "en-GB"]
    assert expand_locale_groups(["en"]) == ["en-US", "en-GB"]
