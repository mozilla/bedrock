# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest import mock

from django.conf import settings

import pytest

from bedrock.cms.models import AbstractBedrockCMSPage, SimpleRichTextPage
from bedrock.cms.tests.factories import StructuralPageFactory

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.skipif(
    settings.WAGTAIL_ENABLE_PAGE_SERVING is False,
    reason="Disabled while Wagtail page serving is not in use",
)
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


@pytest.mark.skipif(
    settings.WAGTAIL_ENABLE_PAGE_SERVING is False,
    reason="Disabled while Wagtail page serving is not in use",
)
def test_StructuralPage_serve_methods(
    minimal_site,
    rf,
):
    "Show that structural pages redirect to their parent rather than serve anything"

    root_page = SimpleRichTextPage.objects.first()
    sp = StructuralPageFactory(parent=root_page, slug="folder-page")
    sp.save()

    _relative_url = sp.relative_url(minimal_site)
    assert _relative_url == "/en-US/folder-page/"

    request = rf.get(_relative_url)
    live_result = sp.serve(request)
    assert live_result.headers["location"] == root_page.url

    preview_result = sp.serve_preview(request)
    assert preview_result.headers["location"] == root_page.url
