# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.test import override_settings

import pytest
from waffle.testutils import override_switch

from bedrock.base.waffle import switch

pytestmark = [
    pytest.mark.django_db,
]


@override_settings(DEV=True)
def test_switch_helper_dev_true():
    # When no switch exists, we return the value of `settings.DEV`.
    assert switch("dude-and-walter") is True
    # Then test explicityly set switch values.
    with override_switch("DUDE_AND_WALTER", active=True):
        assert switch("dude-and-walter") is True
    with override_switch("DUDE_AND_WALTER", active=False):
        assert switch("dude-and-walter") is False


@override_settings(DEV=False)
def test_switch_helper_dev_false():
    # When no switch exists, we return the value of `settings.DEV`.
    assert switch("dude-and-walter") is False
    # Then test explicityly set switch values.
    with override_switch("DUDE_AND_WALTER", active=True):
        assert switch("dude-and-walter") is True
    with override_switch("DUDE_AND_WALTER", active=False):
        assert switch("dude-and-walter") is False
