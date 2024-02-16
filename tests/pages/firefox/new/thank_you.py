# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

from selenium.webdriver.common.by import By

from pages.base import BasePage


class ThankYouPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/download/thanks/"

    _direct_download_link_locator = (By.ID, "direct-download-link")

    _linux_button_group_locator = (By.CLASS_NAME, "c-linux-button-group")

    _linux_download_link_locator = (By.CSS_SELECTOR, ".c-linux-button-group .mzp-c-button")

    # Bug 1354334 - sometimes download is triggered before window.load.
    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, "html")
        self.wait.until(lambda s: "download-ready" in el.get_attribute("class"))
        return self

    @property
    def is_direct_download_link_displayed(self):
        return self.is_element_displayed(*self._direct_download_link_locator)

    @property
    def is_direct_download_link_valid(self):
        return settings.BOUNCER_URL in self.find_element(*self._direct_download_link_locator).get_attribute("href")

    @property
    def is_platform_linux(self):
        el = self.find_element(By.TAG_NAME, "html")
        return "linux" in el.get_attribute("class")

    @property
    def is_linux_button_group_displayed(self):
        return self.is_element_displayed(*self._linux_button_group_locator)

    @property
    def is_linux_link_valid(self):
        links = self.find_elements(*self._linux_download_link_locator)
        return all(settings.BOUNCER_URL in link.get_attribute("href") for link in links)
