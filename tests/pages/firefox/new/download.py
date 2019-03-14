# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.download_button import DownloadButton
from pages.regions.modal import Modal


class DownloadPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/new/{params}'

    _download_button_locator = (By.ID, 'download-button-desktop-release')
    _platforms_modal_link_locator = (By.ID, 'other-platforms-modal-link')
    _platforms_modal_content_locator = (By.ID, 'other-platforms')
    _account_modal_content_locator = (By.ID, 'firefox-account')

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)

    def download_firefox(self):
        self.download_button.click()
        from pages.firefox.new.thank_you import ThankYouPage
        return ThankYouPage(self.selenium, self.base_url).wait_for_page_to_load()

    def open_other_platforms_modal(self):
        modal = Modal(self)
        self.find_element(*self._platforms_modal_link_locator).click()
        self.wait.until(lambda s: modal.displays(self._platforms_modal_content_locator))
        return modal

    def open_firefox_account_modal(self):
        modal = Modal(self)
        self.download_button.click()
        self.wait.until(lambda s: modal.displays(self._account_modal_content_locator))
        return modal
