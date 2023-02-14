# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.menu_list import MenuList
from pages.regions.sticky_promo import StickyPromo


class FirefoxHomePage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/"

    # browser download menu list
    _browser_menu_list_locator = (By.ID, "test-menu-browsers-wrapper")

    # facebook container extention link visiability
    _facebook_container_link_locator = (By.ID, "test-fbc")

    # floating/sticky box - download link
    _sticky_promo_modal_content_locator = (By.CSS_SELECTOR, ".mzp-c-sticky-promo")

    # Used as a scroll target to move down the page, to trigger the sticky promo element
    _page_promise_content_locator = (By.CSS_SELECTOR, ".t-promise")

    @property
    def fb_container_is_displayed(self):
        return self.is_element_displayed(*self._facebook_container_link_locator)

    @property
    def browser_menu_list(self):
        el = self.find_element(*self._browser_menu_list_locator)
        return MenuList(self, root=el)

    def init_promo(self):
        assert not self.is_promo_displayed, "Promo detail is not displayed"
        # scroll down page to trigger promo to display
        self.scroll_element_into_view(*self._page_promise_content_locator)
        promo = self.find_element(*self._sticky_promo_modal_content_locator)
        self.wait.until(lambda s: "is-displayed" in promo.get_attribute("class"))

    @property
    def is_promo_displayed(self):
        return self.is_element_displayed(*self._sticky_promo_modal_content_locator)

    @property
    def promo(self):
        return StickyPromo(self)
