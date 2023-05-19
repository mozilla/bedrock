# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class VPNLandingPage(BasePage):
    _URL_TEMPLATE = "/{locale}/products/vpn/{params}"

    # Hero
    _get_vpn_hero_button_locator = (By.CSS_SELECTOR, '.c-hero .mzp-c-button[data-cta-text="Save on Mozilla VPN"]')
    _join_waitlist_hero_button_locator = (By.CSS_SELECTOR, '.c-hero .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    # Navigation
    _get_vpn_navigation_button_locator = (By.CSS_SELECTOR, '.c-navigation-shoulder .mzp-c-button[data-cta-text="Get Mozilla VPN"]')
    _join_waitlist_navigation_button_locator = (By.CSS_SELECTOR, '.c-navigation-shoulder .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    # Secondary
    _get_vpn_secondary_button_locator = (By.CSS_SELECTOR, '.c-aside.secondary .mzp-c-button[data-cta-text="Get Mozilla VPN"]')
    _join_waitlist_secondary_button_locator = (By.CSS_SELECTOR, '.c-aside.secondary .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    # Tertiary
    _get_vpn_tertiary_button_locator = (By.CSS_SELECTOR, '.c-aside.tertiary .mzp-c-button[data-cta-text="Get Mozilla VPN"]')
    _join_waitlist_tertiary_button_locator = (By.CSS_SELECTOR, '.c-aside.tertiary .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    # Footer
    _get_vpn_footer_button_locator = (By.CSS_SELECTOR, '.c-aside.footer .mzp-c-button[data-cta-text="Get Mozilla VPN"]')
    _join_waitlist_footer_button_locator = (By.CSS_SELECTOR, '.c-aside.footer .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    # Hero

    @property
    def is_get_vpn_hero_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_hero_button_locator)

    @property
    def is_join_waitlist_hero_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_hero_button_locator)

    # Navigation

    @property
    def is_get_vpn_navigation_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_navigation_button_locator)

    @property
    def is_join_waitlist_navigation_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_navigation_button_locator)

    # Secondary

    @property
    def is_get_vpn_secondary_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_secondary_button_locator)

    @property
    def is_join_waitlist_secondary_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_secondary_button_locator)

    # Secondary

    @property
    def is_get_vpn_tertiary_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_tertiary_button_locator)

    @property
    def is_join_waitlist_tertiary_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_tertiary_button_locator)

    # Footer

    @property
    def is_get_vpn_footer_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_footer_button_locator)

    @property
    def is_join_waitlist_footer_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_footer_button_locator)
