# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class VPNFeaturesPage(BasePage):
    _URL_TEMPLATE = "/{locale}/products/vpn/features/{params}"

    # Footer
    _get_vpn_footer_button_locator = (By.CSS_SELECTOR, '.c-aside.footer .mzp-c-button[data-cta-text="Get Mozilla VPN"]')
    _join_waitlist_footer_button_locator = (By.CSS_SELECTOR, '.c-aside.footer .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    # Footer

    @property
    def is_get_vpn_footer_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_footer_button_locator)

    @property
    def is_join_waitlist_footer_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_footer_button_locator)
