# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class VPNLandingPage(BasePage):

    _URL_TEMPLATE = '/{locale}/products/vpn/{params}'

    _try_vpn_hero_fixed_price_button_locator = (By.CSS_SELECTOR, '.vpn-hero .mzp-c-button.js-text-vpn-fixed-price-available')
    _join_waitlist_hero_button_locator = (By.CSS_SELECTOR, '.vpn-hero .mzp-c-button.js-text-vpn-not-available')

    _try_vpn_navigation_fixed_price_button_locator = (By.CSS_SELECTOR, '.c-navigation-shoulder .mzp-c-button.js-text-vpn-fixed-price-available')
    _join_waitlist_navigation_button_locator = (By.CSS_SELECTOR, '.c-navigation-shoulder .mzp-c-button.js-text-vpn-not-available')

    _try_vpn_conntect_now_fixed_price_button_locator = (By.CSS_SELECTOR, '.vpn-content-media.js-section-vpn-fixed-price-available')
    _join_waitlist_coming_soon_button_locator = (By.CSS_SELECTOR, '.vpn-content-media.js-section-vpn-not-available')

    _try_vpn_fixed_pricing_section_button_locator = (By.CSS_SELECTOR, '.vpn-pricing-fixed .mzp-c-button.js-text-vpn-fixed-price-available')
    _join_waitlist_fixed_pricing_section_button_locator = (By.CSS_SELECTOR, '.vpn-pricing-fixed .mzp-c-button.js-text-vpn-not-available')

    _try_vpn_footer_fixed_price_button_locator = (By.CSS_SELECTOR, '.vpn-footer .mzp-c-button.js-text-vpn-fixed-price-available')
    _join_waitlist_footer_button_locator = (By.CSS_SELECTOR, '.vpn-footer .mzp-c-button.js-text-vpn-not-available')

    @property
    def is_try_vpn_hero_fixed_price_button_displayed(self):
        return self.is_element_displayed(*self._try_vpn_hero_fixed_price_button_locator)

    @property
    def is_join_waitlist_hero_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_hero_button_locator)

    @property
    def is_try_vpn_navigation_fixed_price_button_displayed(self):
        return self.is_element_displayed(*self._try_vpn_navigation_fixed_price_button_locator)

    @property
    def is_join_waitlist_navigation_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_navigation_button_locator)

    @property
    def is_try_vpn_conntect_now_fixed_price_button_displayed(self):
        return self.is_element_displayed(*self._try_vpn_conntect_now_fixed_price_button_locator)

    @property
    def is_join_waitlist_coming_soon_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_coming_soon_button_locator)

    @property
    def is_try_vpn_fixed_pricing_section_button_displayed(self):
        return self.is_element_displayed(*self._try_vpn_fixed_pricing_section_button_locator)

    @property
    def is_join_waitlist_fixed_pricing_section_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_fixed_pricing_section_button_locator)

    @property
    def is_try_vpn_footer_fixed_price_button_displayed(self):
        return self.is_element_displayed(*self._try_vpn_footer_fixed_price_button_locator)

    @property
    def is_join_waitlist_footer_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_footer_button_locator)
