# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.modal import ModalProtocol


class YandexDownloadPage(BasePage):

    _URL_TEMPLATE = '/{locale}/firefox/new/{params}'

    _download_button_locator = (By.CSS_SELECTOR, '#download-button-thanks > .download-link')
    _join_firefox_modal_content_locator = (By.CLASS_NAME, 'join-firefox-content')
    _yandex_download_button_locator = (By.CSS_SELECTOR, '.t-yandex .mzp-c-button.mzp-t-product')

    @property
    def is_download_button_displayed(self):
        return self.is_element_displayed(*self._download_button_locator)

    def download_firefox(self):
        link = self.find_element(*self._download_button_locator)
        href = link.get_attribute('href')
        self.set_attribute(link, att_name='href', att_value=href + '?automation=true')
        link.click()
        from pages.firefox.new.thank_you import ThankYouPage
        return ThankYouPage(self.selenium, self.base_url).wait_for_page_to_load()

    def open_join_firefox_modal(self):
        modal = ModalProtocol(self)
        self.find_element(*self._download_button_locator).click()
        self.wait.until(lambda s: modal.displays(self._join_firefox_modal_content_locator))
        return modal

    @property
    def is_yandex_download_button_displayed(self):
        button = self.find_element(*self._yandex_download_button_locator)
        return button.is_displayed() and 'https://yandex.ru/firefox/mozilla/' in button.get_attribute('href')
