# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.products.vpn.resource_center import VPNResourceCenterHomePage


@pytest.mark.nondestructive
@pytest.mark.parametrize(
    "locale",
    [
        ("en-US"),
    ],
)
def test_vpn_available_in_country(locale, base_url, selenium):
    page = VPNResourceCenterHomePage(
        selenium,
        base_url,
    ).open()

    # Light test that the VRC page renders at all
    assert page.is_resource_center_header_displayed

    # ...and that it has at least one article
    assert page.is_article_card_with_link_displayed
