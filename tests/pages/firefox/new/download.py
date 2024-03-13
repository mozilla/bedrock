# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class DownloadPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/new/"

    _download_button_locator = (By.CSS_SELECTOR, "#download-button-thanks > .download-link")

    @property
    def is_download_button_displayed(self):
        return self.is_element_displayed(*self._download_button_locator)

    def download_firefox(self):
        link = self.find_element(*self._download_button_locator)
        href = link.get_attribute("href")
        self.set_attribute(link, att_name="href", att_value=href + "?automation=true")
        link.click()
        from pages.firefox.new.thank_you import ThankYouPage

        return ThankYouPage(self.selenium, self.base_url).wait_for_page_to_load()
