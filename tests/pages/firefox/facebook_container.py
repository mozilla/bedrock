# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.download_button import DownloadButton


class FacebookContainerPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/facebookcontainer/"

    _facebook_container_link_locator = (By.CLASS_NAME, "extension-cta")
    _firefox_download_button_locator = (By.ID, "download-firefox-cta")

    @property
    def is_facebook_container_link_displayed(self):
        return self.is_element_displayed(*self._facebook_container_link_locator)

    @property
    def firefox_download_button(self):
        el = self.find_element(*self._firefox_download_button_locator)
        return DownloadButton(self, root=el)
