# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.download_button import DownloadButton


class PlatformDownloadPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/{slug}/"

    _download_button_locator = (By.ID, "download-button-thanks")

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)

    def download_firefox(self):
        href = self.download_button.platform_link.get_attribute("href")
        self.set_attribute(self.download_button.platform_link, att_name="href", att_value=href + "?automation=true")
        self.download_button.click()
        from pages.firefox.new.thank_you import ThankYouPage

        return ThankYouPage(self.selenium, self.base_url).wait_for_page_to_load()
