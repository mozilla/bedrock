# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pypom import Page, Region
from selenium.webdriver.common.by import By


class BaseRegion(Region):
    pass


class BasePage(Page):
    def __init__(self, selenium, base_url, locale="en-US", **url_kwargs):
        super(BasePage, self).__init__(selenium, base_url, locale=locale, **url_kwargs)

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, "html")
        self.wait.until(lambda s: "loaded" in el.get_attribute("class"))

        # Dismiss cookie prompt before running tests
        cookie_prompt = self.wait.until(lambda s: s.find_element(By.ID, "onetrust-accept-btn-handler"))
        cookie_prompt.click()
        self.wait.until(lambda s: cookie_prompt.is_displayed() is False)

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

        _mobile_menu_open_btn_locator = (By.CLASS_NAME, "global-nav-mobile-menu-btn")
        _mobile_menu_close_btn_locator = (By.CLASS_NAME, "mobile-nav-close-btn")
        _mobile_menu_locator = (By.CLASS_NAME, "mobile-nav-list")
        _home_mobile_menu_locator = (By.CSS_SELECTOR, '.mobile-nav-list-link[href="https://getpocket.com/home?src=navbar"]')
        _my_list_mobile_menu_locator = (By.CSS_SELECTOR, '.mobile-nav-list-link[href="https://getpocket.com/my-list?src=navbar"]')

        @property
        def is_mobile_menu_home_link_displayed(self):
            return self.is_element_displayed(*self._home_mobile_menu_locator)

        @property
        def is_mobile_menu_my_list_link_displayed(self):
            return self.is_element_displayed(*self._my_list_mobile_menu_locator)

        @property
        def is_mobile_menu_open(self):
            return self.is_element_displayed(*self._mobile_menu_locator) and self.mobile_menu_open_button.get_attribute("aria-expanded") == "true"

        @property
        def is_mobile_menu_closed(self):
            return (
                not self.is_element_displayed(*self._mobile_menu_locator) and self.mobile_menu_open_button.get_attribute("aria-expanded") == "false"
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
