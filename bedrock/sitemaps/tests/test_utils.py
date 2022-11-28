# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

import pytest

from bedrock.contentful.constants import (
    CONTENT_CLASSIFICATION_VPN,
    CONTENT_TYPE_PAGE_RESOURCE_CENTER,
)
from bedrock.contentful.models import ContentfulEntry
from bedrock.sitemaps.utils import _get_vrc_urls, get_contentful_urls, update_sitemaps

pytestmark = pytest.mark.django_db


@pytest.fixture
def dummy_vrc_pages():
    # No content, just the bare data we need
    for idx in range(5):
        ContentfulEntry.objects.create(
            contentful_id=f"DUMMY-{idx}",
            slug=f"test-slug-{idx}",
            # TODO: support different locales
            locale="en-US",
            localisation_complete=True,
            content_type=CONTENT_TYPE_PAGE_RESOURCE_CENTER,
            classification=CONTENT_CLASSIFICATION_VPN,
            data={},
            data_hash="dummy",
        )


def test__get_vrc_urls(dummy_vrc_pages):
    # TODO: support different locales
    output = _get_vrc_urls()
    assert output == {
        "/products/vpn/resource-center/test-slug-0/": ["en-US"],
        "/products/vpn/resource-center/test-slug-1/": ["en-US"],
        "/products/vpn/resource-center/test-slug-2/": ["en-US"],
        "/products/vpn/resource-center/test-slug-3/": ["en-US"],
        "/products/vpn/resource-center/test-slug-4/": ["en-US"],
    }


def test__get_vrc_urls__no_content():
    output = _get_vrc_urls()
    assert output == {}


@patch("bedrock.sitemaps.utils._get_vrc_urls")
def test_get_contentful_urls(mock__get_vrc_urls):
    mock__get_vrc_urls.return_value = {"vrc-urls": "dummy-here"}

    output = get_contentful_urls()
    assert output == {"vrc-urls": "dummy-here"}
    mock__get_vrc_urls.assert_called_once_with()


@patch("bedrock.sitemaps.utils.get_static_urls")
@patch("bedrock.sitemaps.utils.get_release_notes_urls")
@patch("bedrock.sitemaps.utils.get_security_urls")
@patch("bedrock.sitemaps.utils.get_contentful_urls")
@patch("bedrock.sitemaps.utils.output_json")
def test_update_sitemaps(
    mock_output_json,
    mock_get_contentful_urls,
    mock_get_security_urls,
    mock_get_release_notes_urls,
    mock_get_static_urls,
):
    "Light check to ensure we've not added _new_ things we haven't added tests for"

    mock_get_contentful_urls.return_value = {"contentful": "dummy"}
    mock_get_security_urls.return_value = {"security": "dummy"}
    mock_get_release_notes_urls.return_value = {"release_notes": "dummy"}
    mock_get_static_urls.return_value = {"static_urls": "dummy"}

    update_sitemaps()
    expected = {
        "contentful": "dummy",
        "security": "dummy",
        "release_notes": "dummy",
        "static_urls": "dummy",
    }

    mock_output_json.assert_called_once_with(expected)
