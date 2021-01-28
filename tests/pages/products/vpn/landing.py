# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class VPNLandingPage(BasePage):

    _URL_TEMPLATE = '/{locale}/products/vpn/{params}'

    _try_vpn_hero_button_locator = (By.CSS_SELECTOR, '.vpn-hero .js-try-vpn')
    _join_waitlist_hero_button_locator = (By.CSS_SELECTOR, '.vpn-hero .js-join-waitlist')

    _try_vpn_navigation_button_locator = (By.CSS_SELECTOR, '.c-navigation-shoulder .js-try-vpn')
    _join_waitlist_navigation_button_locator = (By.CSS_SELECTOR, '.c-navigation-shoulder .js-join-waitlist')

    _try_vpn_price_section_button_locator = (By.CSS_SELECTOR, '.vpn-content-well-price .js-try-vpn')
    _join_waitlist_price_section_button_locator = (By.CSS_SELECTOR, '.vpn-content-well-price .js-join-waitlist')

    _join_waitlist_section_button_locator = (By.CSS_SELECTOR, '.vpn-content-well-waitlist .vpn-button.waitlist')

    _try_vpn_footer_button_locator = (By.CSS_SELECTOR, '.vpn-faq-footer .js-try-vpn')
    _join_waitlist_footer_button_locator = (By.CSS_SELECTOR, '.vpn-faq-footer .js-join-waitlist')

    @property
    def is_try_vpn_hero_button_displayed(self):
        return self.is_element_displayed(*self._try_vpn_hero_button_locator)

    @property
    def is_join_waitlist_hero_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_hero_button_locator)

    @property
    def is_try_vpn_navigation_button_displayed(self):
        return self.is_element_displayed(*self._try_vpn_navigation_button_locator)

    @property
    def is_join_waitlist_navigation_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_navigation_button_locator)

    @property
    def is_try_vpn_price_section_button_displayed(self):
        return self.is_element_displayed(*self._try_vpn_price_section_button_locator)

    @property
    def is_join_waitlist_price_section_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_price_section_button_locator)

    @property
    def is_join_waitlist_section_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_section_button_locator)

    @property
    def is_try_vpn_footer_button_displayed(self):
        return self.is_element_displayed(*self._try_vpn_footer_button_locator)

    @property
    def is_join_waitlist_footer_button_displayed(self):
        return self.is_element_displayed(*self._join_waitlist_footer_button_locator)
