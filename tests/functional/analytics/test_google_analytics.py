# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.externalpages.analytics.index import AnalyticsTestPage


def parse_event(data_layer, element):
    for item in data_layer:
        return filter(lambda x: x["gtm.element"][item] == element)


@pytest.mark.nondestructive
def test_download_button(base_url, selenium):
    page = AnalyticsTestPage(selenium, base_url).open()
    assert page.download_button_is_displayed
    page.click_download_button()
    data_layer = selenium.execute_script("return window.dataLayer")
    link_type = page.download_button.get_attribute("data-link-type")
    assert any("gtm.element" in layer and layer["gtm.element"].get_attribute("data-link-type") == link_type for layer in data_layer)


@pytest.mark.nondestructive
def test_link_button(base_url, selenium):
    page = AnalyticsTestPage(selenium, base_url).open()
    assert page.link_button_is_displayed
    page.click_link_button()
    data_layer = selenium.execute_script("return window.dataLayer")
    cta_type = page.link_button.get_attribute("data-cta-type")
    assert any("gtm.element" in layer and layer["gtm.element"].get_attribute("data-cta-type") == cta_type for layer in data_layer)


@pytest.mark.nondestructive
def test_account_button(base_url, selenium):
    page = AnalyticsTestPage(selenium, base_url).open()
    assert page.account_button_is_displayed
    page.click_account_button()
    data_layer = selenium.execute_script("return window.dataLayer")
    cta_type = page.account_button.get_attribute("data-cta-type")
    assert any("gtm.element" in layer and layer["gtm.element"].get_attribute("data-cta-type") == cta_type for layer in data_layer)
