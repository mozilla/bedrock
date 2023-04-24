# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class VPNPricingPage(BasePage):
    _URL_TEMPLATE = "/{locale}/products/vpn/pricing/{params}"

    _get_vpn_monthly_button_locator = (By.CSS_SELECTOR, ".vpn-pricing-monthly .mzp-c-button")
    _get_vpn_12_months_button_locator = (By.CSS_SELECTOR, ".vpn-pricing-12-months .mzp-c-button")
    _join_waitlist_button_locator = (By.CSS_SELECTOR, '.vpn-more-countries-coming-soon .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    @property
    def is_get_vpn_monthly_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_monthly_button_locator)

    @property
    def is_get_vpn_12_months_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_12_months_button_locator)

    @property
    def is_join_waitlist_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_button_locator)
