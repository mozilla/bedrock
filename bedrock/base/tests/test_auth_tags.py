# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test import override_settings

import pytest

from bedrock.base.templatetags.auth_tags import should_use_sso_auth


@pytest.mark.parametrize(
    "settings_val, expected",
    (
        (True, True),
        (False, False),
        (None, False),
    ),
)
def test_should_use_simple_auth(settings_val, expected):
    with override_settings(USE_SSO_AUTH=settings_val):
        assert should_use_sso_auth() == expected
