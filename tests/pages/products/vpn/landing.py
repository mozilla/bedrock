# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class VPNLandingPage(BasePage):

    _URL_TEMPLATE = "/{locale}/products/vpn/{params}"

    # Hero
    _get_vpn_hero_button_locator = (By.CSS_SELECTOR, '.vpn-hero .mzp-c-button[data-cta-text="Scroll to pricing"]')
    _join_waitlist_hero_button_locator = (By.CSS_SELECTOR, '.vpn-hero .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    # Navigation
    _get_vpn_navigation_button_locator = (By.CSS_SELECTOR, '.c-navigation-shoulder .mzp-c-button[data-cta-text="Scroll to pricing"]')
    _join_waitlist_navigation_button_locator = (By.CSS_SELECTOR, '.c-navigation-shoulder .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    # Pricing section
    _get_vpn_monthly_button_locator = (By.CSS_SELECTOR, ".vpn-pricing-monthly .mzp-c-button")
    _get_vpn_6_months_button_locator = (By.CSS_SELECTOR, ".vpn-pricing-6-months .mzp-c-button")
    _get_vpn_12_months_button_locator = (By.CSS_SELECTOR, ".vpn-pricing-12-months .mzp-c-button")

    # Waitlist features section
    _join_waitlist_features_button_locator = (By.CSS_SELECTOR, '.vpn-waitlist-feature-block .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    # Connect section
    _get_vpn_conntect_now_button_locator = (By.CSS_SELECTOR, '.vpn-connect-to-countries-and-servers .mzp-c-button[data-cta-text="Scroll to pricing"]')
    _join_waitlist_coming_soon_button_locator = (
        By.CSS_SELECTOR,
        '.vpn-more-countries-coming-soon .mzp-c-button[data-cta-text="Join the VPN Waitlist"]',
    )

    # Footer
    _get_vpn_footer_button_locator = (By.CSS_SELECTOR, '.vpn-footer .mzp-c-button[data-cta-text="Scroll to pricing"]')
    _join_waitlist_footer_button_locator = (By.CSS_SELECTOR, '.vpn-footer .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

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

    # Pricing section

    @property
    def is_get_vpn_monthly_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_monthly_button_locator)

    @property
    def is_get_vpn_6_months_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_6_months_button_locator)

    @property
    def is_get_vpn_12_months_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_12_months_button_locator)

    # Waitlist Features section

    @property
    def is_join_waitlist_features_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_features_button_locator)

    # Connect section

    @property
    def is_get_vpn_conntect_now_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_conntect_now_button_locator)

    @property
    def is_join_waitlist_coming_soon_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_coming_soon_button_locator)

    # Footer

    @property
    def is_get_vpn_footer_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_footer_button_locator)

    @property
    def is_join_waitlist_footer_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_footer_button_locator)
