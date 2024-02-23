# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from urllib.parse import unquote

import pytest

from pages.products.landing import ProductsPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_download_menu_list_displays(base_url, selenium):
    page = ProductsPage(selenium, base_url).open()
    page.firefox_menu_list.click()
    assert page.firefox_menu_list.list_is_open


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_focus_download_menu_list_displays(base_url, selenium):
    page = ProductsPage(selenium, base_url).open()
    page.focus_menu_list.click()
    assert page.focus_menu_list.list_is_open


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_pocket_download_menu_list_displays(base_url, selenium):
    page = ProductsPage(selenium, base_url).open()
    page.pocket_menu_list.click()
    assert page.pocket_menu_list.list_is_open


@pytest.mark.nondestructive
def test_account_form(base_url, selenium):
    page = ProductsPage(selenium, base_url).open()
    page.join_firefox_form.type_email("success@example.com")
    page.join_firefox_form.click_continue()
    url = unquote(selenium.current_url)
    assert "email=success@example.com" in url, "Email address is not in URL"
