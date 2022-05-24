# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.analytics.index import AnalyticsTestPage


def assert_ga_loaded(page):
    # if the datalayer list doesnt contain
    # the gtm.load event then GA has not been loaded or it has been blocked
    assert page.is_ga_loaded, (
        "These tests require Google Analytics to be configured. "
        "Please ensure you have set a GTM_CONTAINER_ID environment "
        "variable in your .env and you are not blocking GA in your browser."
    )


@pytest.mark.nondestructive
def test_download_button(base_url, selenium):
    page = AnalyticsTestPage(selenium, base_url).open()
    assert_ga_loaded(page)
    assert page.download_button_is_displayed
    page.click_download_button()
    data_layer = selenium.execute_script("return window.dataLayer")
    link_type = page.download_button.get_attribute("data-link-type")
    assert any("gtm.element" in layer and layer["gtm.element"].get_attribute("data-link-type") == link_type for layer in data_layer)


@pytest.mark.nondestructive
def test_link_button(base_url, selenium):
    page = AnalyticsTestPage(selenium, base_url).open()
    assert_ga_loaded(page)
    assert page.link_button_is_displayed
    page.click_link_button()
    data_layer = selenium.execute_script("return window.dataLayer")
    cta_type = page.link_button.get_attribute("data-cta-type")
    assert any("gtm.element" in layer and layer["gtm.element"].get_attribute("data-cta-type") == cta_type for layer in data_layer)


@pytest.mark.nondestructive
def test_account_button(base_url, selenium):
    page = AnalyticsTestPage(selenium, base_url).open()
    assert_ga_loaded(page)
    assert page.account_button_is_displayed
    page.click_account_button()
    data_layer = selenium.execute_script("return window.dataLayer")
    cta_type = page.account_button.get_attribute("data-cta-type")
    assert any("gtm.element" in layer and layer["gtm.element"].get_attribute("data-cta-type") == cta_type for layer in data_layer)
