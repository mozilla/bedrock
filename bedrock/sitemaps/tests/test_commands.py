# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from io import StringIO
from unittest.mock import patch

from django.core.management import call_command

import pytest

from bedrock.sitemaps.models import SitemapURL


@pytest.fixture
def refresh():
    with patch.object(SitemapURL.objects, "refresh") as refresh_mock:
        yield refresh_mock


def test_update_sitemaps_data(refresh):
    out = StringIO()
    call_command("update_sitemaps_data", stdout=out)
    refresh.assert_called_once_with()
    assert out.getvalue() == "Updated sitemaps data\n"


def test_update_sitemaps_data__quiet(refresh):
    out = StringIO()
    call_command("update_sitemaps_data", quiet=True, stdout=out)
    refresh.assert_called_once_with()
    assert out.getvalue() == ""


@patch("bedrock.utils.management.decorators.capture_exception")
def test_update_sitemaps_data__error_goes_to_sentry(capture_exception, refresh):
    error = RuntimeError("URL discovery failed")
    refresh.side_effect = error
    with pytest.raises(RuntimeError):
        call_command("update_sitemaps_data")
    capture_exception.assert_called_once_with(error)
