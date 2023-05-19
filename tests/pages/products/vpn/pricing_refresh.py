# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class VPNPricingPage(BasePage):
    _URL_TEMPLATE = "/{locale}/products/vpn/pricing/{params}"

    _get_vpn_monthly_button_locator = (By.CSS_SELECTOR, '.c-pricing-block .mzp-c-button[data-cta-text="Get Mozilla VPN monthly"]')
    _get_vpn_12_months_button_locator = (By.CSS_SELECTOR, '.c-pricing-block .mzp-c-button[data-cta-text="Get Mozilla VPN 12-month"]')
    _join_waitlist_button_locator = (By.CSS_SELECTOR, '.c-pricing-main-header .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    @property
    def is_get_vpn_monthly_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_monthly_button_locator)

    @property
    def is_get_vpn_12_months_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_12_months_button_locator)

    @property
    def is_join_waitlist_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_button_locator)
