# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.enterprise.landing import EnterprisePage


@pytest.mark.nondestructive
def test_primary_download_button_displayed(base_url, selenium):
    page = EnterprisePage(selenium, base_url).open()
    assert page.is_primary_download_button_displayed


@pytest.mark.nondestructive
def test_click_contact_sales_button(base_url, selenium):
    page = EnterprisePage(selenium, base_url).open()
    signup_page = page.click_contact_sales_button()
    assert signup_page.seed_url in selenium.current_url


@pytest.mark.nondestructive
def test_comparison_buttons_displayed_desktop(base_url, selenium):
    page = EnterprisePage(selenium, base_url).open()
    assert not page.is_comparison_basic_tab_button_displayed
    assert not page.is_comparison_premium_tab_button_displayed
    assert page.is_comparison_download_button_displayed
    assert page.is_comparison_sales_button_displayed


@pytest.mark.nondestructive
def test_comparison_plan_displayed_mobile(base_url, selenium_mobile):
    page = EnterprisePage(selenium_mobile, base_url).open()
    assert page.is_comparison_basic_tab_button_displayed
    assert page.is_comparison_premium_tab_button_displayed
    assert page.is_comparison_basic_plan_displayed
    assert not page.is_comparison_premium_plan_displayed
    page.click_premium_plan_tab_button()
    assert page.is_comparison_premium_plan_displayed
    assert not page.is_comparison_basic_plan_displayed
    page.click_basic_plan_tab_button()
    assert not page.is_comparison_premium_plan_displayed
    assert page.is_comparison_basic_plan_displayed


@pytest.mark.nondestructive
def test_package_download_buttons_displayed(base_url, selenium):
    page = EnterprisePage(selenium, base_url).open()
    assert page.is_package_win64_download_button_displayed
    assert page.is_package_mac_download_button_displayed
    assert page.is_package_win32_download_button_displayed
