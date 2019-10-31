# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.modal import ModalProtocol


class FirefoxWhatsNew67Page(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/67.0/whatsnew/all/{params}'

    _firefox_accounts_form_locator = (By.ID, 'fxa-email-form')
    _newsletter_form_locator = (By.ID, 'newsletter-sticky-form')
    _lockwise_link_locator = (By.CSS_SELECTOR, '.wn67-benefit-link[data-app="lockwise"]')
    _lockwise_qr_code_locator = (By.CSS_SELECTOR, '.mzp-c-modal .mobile-lockwise .mobile-qr')
    _pocket_link_locator = (By.CSS_SELECTOR, '.wn67-benefit-link[data-app="pocket"]')
    _pocket_qr_code_locator = (By.CSS_SELECTOR, '.mzp-c-modal .mobile-pocket .mobile-qr')

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, 'body')
        self.wait.until(lambda s: 'state-fxa-default' not in el.get_attribute('class'))
        return self

    def open_modal(self, locator):
        modal = ModalProtocol(self)
        self.find_element(*locator).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal

    @property
    def is_firefox_accounts_form_displayed(self):
        return self.is_element_displayed(*self._firefox_accounts_form_locator)

    @property
    def is_newsletter_form_displayed(self):
        return self.is_element_displayed(*self._newsletter_form_locator)

    @property
    def is_lockwise_qr_code_displayed(self):
        return self.is_element_displayed(*self._lockwise_qr_code_locator)

    @property
    def is_pocket_qr_code_displayed(self):
        return self.is_element_displayed(*self._pocket_qr_code_locator)

    def click_get_lockwise_link(self):
        self.scroll_element_into_view(*self._lockwise_link_locator)
        return self.open_modal(self._lockwise_link_locator)

    def click_get_pocket_link(self):
        self.scroll_element_into_view(*self._lockwise_link_locator)
        return self.open_modal(self._pocket_link_locator)
