# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.products.vpn.invite import VPNInvitePage


@pytest.mark.nondestructive
def test_sign_up_success(base_url, selenium):
    page = VPNInvitePage(selenium, base_url).open()
    page.type_email('success@example.com')
    page.select_country('United Kingdom')
    page.select_language('English')
    page.click_sign_me_up()
    assert page.is_form_success_displayed


@pytest.mark.nondestructive
def test_sign_up_failure(base_url, selenium):
    page = VPNInvitePage(selenium, base_url).open()
    page.type_email('invalid@email')
    page.select_country('United Kingdom')
    page.select_language('English')
    page.click_sign_me_up(expected_result='error')
    assert page.is_form_error_displayed
