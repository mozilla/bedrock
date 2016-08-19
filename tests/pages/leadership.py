# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.modal import Modal


class LeadershipPage(BasePage):

    URL_TEMPLATE = '/{locale}/about/leadership/'

    _corporation_bios_locator = (By.CSS_SELECTOR, '.gallery.mgmt-corp .vcard.has-bio')
    _foundation_bios_locator = (By.CSS_SELECTOR, '.gallery.mgmt-foundation .vcard.has-bio')
    _next_button_locator = (By.CSS_SELECTOR, '#modal nav .next')
    _previous_button_locator = (By.CSS_SELECTOR, '#modal nav .prev')
    _modal_bio_locator = (By.CSS_SELECTOR, '#modal .vcard.has-bio')

    @property
    def corporation(self):
        leaders = self.find_elements(*self._corporation_bios_locator)
        return [l.get_attribute('id') for l in leaders]

    @property
    def foundation(self):
        leaders = self.find_elements(*self._foundation_bios_locator)
        return [l.get_attribute('id') for l in leaders]

    def open_biography(self, value):
        modal = Modal(self)
        self.find_element(*(By.ID, value)).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal

    def is_biography_displayed(self, value):
        return self.is_element_displayed(*(By.CSS_SELECTOR,
               '#modal .vcard.has-bio[data-id="{0}"]'.format(value)))

    def get_next_leader(self, index, leaders):
        current_index = leaders.index(index)
        if current_index == len(leaders) - 1:
            return leaders[0]
        return leaders[current_index + 1]

    def click_next(self):
        current = self.find_element(*self._modal_bio_locator).get_attribute('data-id')
        self.find_element(*self._next_button_locator).click()
        self.wait.until(lambda s: not self.is_biography_displayed(current))

    def click_previous(self):
        current = self.find_element(*self._modal_bio_locator).get_attribute('data-id')
        self.find_element(*self._previous_button_locator).click()
        self.wait.until(lambda s: not self.is_biography_displayed(current))
