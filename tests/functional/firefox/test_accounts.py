# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from urllib.parse import unquote

import pytest

from pages.firefox.accounts import FirefoxAccountsPage


@pytest.mark.nondestructive
def test_account_form(base_url, selenium):
    page = FirefoxAccountsPage(selenium, base_url, params="?signed-in=false").open()
    page.join_firefox_form.type_email("success@example.com")
    page.join_firefox_form.click_continue()
    url = unquote(selenium.current_url)
    assert "email=success@example.com" in url, "Email address is not in URL"


@pytest.mark.nondestructive
@pytest.mark.skip_if_not_firefox(reason="Signed-in state is shown only to Firefox users.")
def test_signed_in_call_to_action(base_url, selenium):
    page = FirefoxAccountsPage(selenium, base_url, params="?signed-in=true").open()
    assert not page.join_firefox_form.is_displayed
    assert page.is_manage_button_displayed
