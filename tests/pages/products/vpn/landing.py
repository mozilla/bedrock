# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class VPNLandingPage(BasePage):

    _URL_TEMPLATE = '/{locale}/products/vpn/{params}'

    # Hero
    _get_vpn_hero_fixed_price_button_locator = (By.CSS_SELECTOR, '.vpn-hero .js-vpn-fixed-pricing .mzp-c-button')
    _get_vpn_hero_variable_price_anchor_locator = (By.CSS_SELECTOR, '.vpn-hero .js-vpn-variable-pricing .mzp-c-button')
    _join_waitlist_hero_button_locator = (By.CSS_SELECTOR, '.vpn-hero .js-vpn-waitlist .mzp-c-button')

    # Navigation
    _get_vpn_navigation_fixed_price_button_locator = (By.CSS_SELECTOR,
                                                      '.c-navigation-shoulder .mzp-c-button[data-cta-text="Get Mozilla VPN monthly"]')
    _get_vpn_navigation_variable_price_button_locator = (By.CSS_SELECTOR,
                                                         '.c-navigation-shoulder .mzp-c-button[data-cta-text="Scroll to pricing"]')
    _join_waitlist_navigation_button_locator = (By.CSS_SELECTOR,
                                                '.c-navigation-shoulder .mzp-c-button[data-cta-text="Join the VPN Waitlist"]')

    # Connect section
    _get_vpn_conntect_now_fixed_price_button_locator = (By.CSS_SELECTOR,
                                                        '.js-connect-to-countries-and-servers .js-vpn-fixed-pricing .mzp-c-button')
    _get_vpn_conntect_now_variable_price_anchor_locator = (By.CSS_SELECTOR,
                                                           '.js-connect-to-countries-and-servers .js-vpn-variable-pricing .mzp-c-button')
    _join_waitlist_coming_soon_button_locator = (By.CSS_SELECTOR, '.js-more-countries-coming-soon .js-vpn-waitlist .mzp-c-button')

    # Pricing section
    _get_vpn_fixed_price_section_button_locator = (By.CSS_SELECTOR, '.vpn-fixed-pricing-block .js-vpn-fixed-pricing .mzp-c-button')
    _get_vpn_variable_price_monthly_button_locator = (By.CSS_SELECTOR, '.vpn-pricing-monthly .mzp-c-button')
    _get_vpn_variable_price_6_months_button_locator = (By.CSS_SELECTOR, '.vpn-pricing-6-months .mzp-c-button')
    _get_vpn_variable_price_12_months_button_locator = (By.CSS_SELECTOR, '.vpn-pricing-12-months .mzp-c-button')
    _join_waitlist_fixed_price_section_button_locator = (By.CSS_SELECTOR, '.vpn-fixed-pricing-block .js-vpn-waitlist .mzp-c-button')

    # Footer
    _get_vpn_footer_fixed_price_button_locator = (By.CSS_SELECTOR, '.vpn-footer .js-vpn-fixed-pricing .mzp-c-button')
    _get_vpn_footer_variable_price_anchor_locator = (By.CSS_SELECTOR, '.vpn-footer .js-vpn-variable-pricing .mzp-c-button')
    _join_waitlist_footer_button_locator = (By.CSS_SELECTOR, '.vpn-footer .js-vpn-waitlist .mzp-c-button')

    # Hero
    @property
    def is_get_vpn_hero_fixed_price_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_hero_fixed_price_button_locator)

    @property
    def is_get_vpn_hero_variable_price_anchor_displayed(self):
        return self.is_element_displayed(*self._get_vpn_hero_variable_price_anchor_locator)

    @property
    def is_join_waitlist_hero_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_hero_button_locator)

    # Navigation
    @property
    def is_get_vpn_navigation_fixed_price_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_navigation_fixed_price_button_locator)

    @property
    def is_get_vpn_navigation_variable_price_anchor_displayed(self):
        return self.is_element_displayed(*self._get_vpn_navigation_variable_price_button_locator)

    @property
    def is_join_waitlist_navigation_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_navigation_button_locator)

    # Connect section
    @property
    def is_get_vpn_conntect_now_fixed_price_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_conntect_now_fixed_price_button_locator)

    @property
    def is_get_vpn_conntect_now_variable_price_anchor_displayed(self):
        return self.is_element_displayed(*self._get_vpn_conntect_now_variable_price_anchor_locator)

    @property
    def is_join_waitlist_coming_soon_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_coming_soon_button_locator)

    # Pricing section
    @property
    def is_get_vpn_fixed_price_section_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_fixed_price_section_button_locator)

    @property
    def is_get_vpn_vpn_variable_price_monthly_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_variable_price_monthly_button_locator)

    @property
    def is_get_vpn_vpn_variable_price_6_months_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_variable_price_6_months_button_locator)

    @property
    def is_get_vpn_vpn_variable_price_12_months_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_variable_price_12_months_button_locator)

    @property
    def is_join_waitlist_fixed_price_section_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_fixed_price_section_button_locator)

    # Footer
    @property
    def is_get_vpn_footer_fixed_price_button_displayed(self):
        return self.is_element_displayed(*self._get_vpn_footer_fixed_price_button_locator)

    @property
    def is_get_vpn_footer_variable_price_anchor_displayed(self):
        return self.is_element_displayed(*self._get_vpn_footer_variable_price_anchor_locator)

    @property
    def is_join_waitlist_footer_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_footer_button_locator)
