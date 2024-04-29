# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest import mock

import pytest

from bedrock.cms.models import AbstractBedrockCMSPage, SimpleRichTextPage

pytestmark = [
    pytest.mark.django_db,
]


@mock.patch("bedrock.cms.models.SimpleRichTextPage.get_view_restrictions")
@pytest.mark.parametrize(
    "fake_restrictions, expected_headers",
    (
        ([], "max-age=600"),
        ([mock.Mock()], "max-age=0, no-cache, no-store, must-revalidate, private"),
    ),
    ids=[
        "Default, unrestricted-page behaviour",
        "Restricted-page behaviour",
    ],
)
def test_cache_control_headers_on_pages_with_view_restrictions(
    mock_get_view_restrictions,
    fake_restrictions,
    expected_headers,
    client,
    minimal_site,
):
    mock_get_view_restrictions.return_value = fake_restrictions

    page = SimpleRichTextPage.objects.last()  # made by the minimal_site fixture

    # Confirm we're using the base page
    assert isinstance(page, AbstractBedrockCMSPage)

    _relative_url = page.relative_url(minimal_site)
    assert _relative_url == "/en-US/test-page/"

    response = client.get(_relative_url)

    assert response.get("Cache-Control") == expected_headers
