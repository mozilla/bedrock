# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
from wagtail.rich_text import RichText

from bedrock.cms.tests.conftest import minimal_site  # noqa
from bedrock.products.tests import factories

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_vpn_resource_center_index_page(minimal_site, rf, serving_method):  # noqa
    root_page = minimal_site.root_page

    call_to_action_middle = factories.VPNCallToActionSnippetFactory(
        heading="Test Call To Action Middle Heading",
    )
    call_to_action_middle.save()

    call_to_action_bottom = factories.VPNCallToActionSnippetFactory(
        heading="Test Call To Action Bottom Heading",
    )
    call_to_action_bottom.save()

    test_index_page = factories.VPNResourceCenterIndexPageFactory(
        parent=root_page,
        sub_title="Test Subtitle",
        call_to_action_middle=call_to_action_middle,
        call_to_action_bottom=call_to_action_bottom,
    )

    test_index_page.save()

    test_detail_pages = {}

    for i in range(1, 13):
        test_detail_pages[f"test_detail_page_{i}"] = factories.VPNResourceCenterDetailPageFactory(
            parent=test_index_page,
            slug=f"test-detail-{i}",
            desc=f"Test Detail Page {i} Description",
            content=RichText(f"Test Detail Page {i} Content"),
        )
        test_detail_pages[f"test_detail_page_{i}"].save()

    _relative_url = test_index_page.relative_url(minimal_site)
    assert _relative_url == "/en-US/test/"
    request = rf.get(_relative_url)

    resp = getattr(test_index_page, serving_method)(request)
    page_content = str(resp.content)
    assert "Test VPN Resource Center Index Page Title" in page_content
    assert "Test Subtitle" in page_content
    assert "Test Detail Page 1 Description" in page_content
    assert "Test Detail Page 12 Description" in page_content
    assert "Test Call To Action Middle Heading" in page_content
    assert "Test Call To Action Bottom Heading" in page_content


@pytest.mark.parametrize("serving_method", ("serve", "serve_preview"))
def test_vpn_resource_center_detail_page(minimal_site, rf, serving_method):  # noqa
    root_page = minimal_site.root_page

    call_to_action_bottom = factories.VPNCallToActionSnippetFactory(
        heading="Test Call To Action Bottom Heading",
    )
    call_to_action_bottom.save()

    test_index_page = factories.VPNResourceCenterIndexPageFactory(
        parent=root_page,
        sub_title="Test Subtitle",
    )

    test_detail_page = factories.VPNResourceCenterDetailPageFactory(
        parent=test_index_page,
        slug="test-detail-1",
        desc="Test Detail Page Description",
        content=RichText("Test Detail Page Content"),
        call_to_action_bottom=call_to_action_bottom,
    )

    test_index_page.save()
    test_detail_page.save()

    _relative_url = test_detail_page.relative_url(minimal_site)
    assert _relative_url == "/en-US/test/test-detail-1/"
    request = rf.get(_relative_url)

    resp = getattr(test_detail_page, serving_method)(request)
    page_content = str(resp.content)
    assert "Test VPN Resource Center Detail Page Title" in page_content
    assert "Test Detail Page Content" in page_content
    assert "Test Call To Action Bottom Heading" in page_content
