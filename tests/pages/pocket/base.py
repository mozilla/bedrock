# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected


class BaseRegion(Region):
    pass


class BasePage(Page):
    def __init__(self, selenium, pocket_base_url, locale="en", **url_kwargs):
        super(BasePage, self).__init__(selenium, pocket_base_url, locale=locale, **url_kwargs)

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, "html")
        self.wait.until(lambda s: "loaded" in el.get_attribute("class"))

        # Dismiss cookie prompt before running tests
        self.wait.until(lambda s: expected.presence_of_element_located(s.find_element(By.ID, "onetrust-banner-sdk")))
        cookie_banner = self.find_element(By.ID, "onetrust-banner-sdk")
        self.wait.until(lambda s: "animation-name" not in cookie_banner.get_attribute("style"))

        accept_cookie_button = self.find_element(By.ID, "onetrust-accept-btn-handler")
        self.wait.until(lambda s: expected.element_to_be_clickable(accept_cookie_button))
        accept_cookie_button.click()

        self.wait.until(lambda s: cookie_banner.is_displayed() is False)

        return self

    @property
    def URL_TEMPLATE(self):
        if "{params}" in self._URL_TEMPLATE:
            return f"{self._URL_TEMPLATE}&automation=true"
        else:
            return f"{self._URL_TEMPLATE}?automation=true"

    @property
    def navigation(self):
        return self.Navigation(self)

    class Navigation(BaseRegion):

        _content_wrapper_locator = (By.TAG_NAME, "body")
        _mobile_menu_open_btn_locator = (By.CLASS_NAME, "global-nav-mobile-menu-btn")
        _mobile_menu_close_btn_locator = (By.CLASS_NAME, "mobile-nav-close-btn")
        _mobile_menu_locator = (By.CLASS_NAME, "mobile-nav")
        _mobile_menu_wrapper_locator = (By.CLASS_NAME, "mobile-nav-wrapper")
        _mobile_menu_link_locator = (By.CSS_SELECTOR, ".mobile-nav-list-link")

        @property
        def is_mobile_menu_nav_link_displayed(self):
            return self.is_element_displayed(*self._mobile_menu_link_locator)

        @property
        def is_mobile_menu_open(self):
            return (
                "mobile-nav-open" in self.find_element(*self._content_wrapper_locator).get_attribute("class")
                and self.mobile_menu_open_button.get_attribute("aria-expanded") == "true"
            )

        @property
        def is_mobile_menu_closed(self):
            return (
                "mobile-nav-open" not in self.find_element(*self._content_wrapper_locator).get_attribute("class")
                and self.mobile_menu_open_button.get_attribute("aria-expanded") == "false"
            )

        @property
        def is_mobile_menu_open_button_displayed(self):
            return self.mobile_menu_open_button

        @property
        def is_mobile_menu_close_button_displayed(self):
            return self.mobile_menu_close_button

        @property
        def mobile_menu_open_button(self):
            return self.find_element(*self._mobile_menu_open_btn_locator)

        @property
        def mobile_menu_close_button(self):
            return self.find_element(*self._mobile_menu_close_btn_locator)

        def open_mobile_menu(self):
            assert not self.is_mobile_menu_open, "Menu is already open"
            self.mobile_menu_open_button.click()
            self.wait.until(lambda s: self.is_mobile_menu_open)
            return self

        def close_mobile_menu(self):
            assert not self.is_mobile_menu_closed, "Menu is already closed"
            self.mobile_menu_close_button.click()
            self.wait.until(lambda s: self.is_mobile_menu_closed)
            return self
