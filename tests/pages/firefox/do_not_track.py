# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait

from pages.page import PageRegion
from pages.firefox.base import FirefoxBasePage


class DoNotTrackPage(FirefoxBasePage):

    _url = '{base_url}/{locale}/firefox/dnt'

    _dnt_status = (By.CSS_SELECTOR, '#dnt-status > h5')
    _faqs_locator = (By.CSS_SELECTOR, '#faq > section')

    @property
    def frequently_asked_questions(self):
        return [FrequentlyAskedQuestion(self.selenium, root=el) for el in
                self.selenium.find_elements(*self._faqs_locator)]

    @property
    def is_do_not_track_status_displayed(self):
        return self.is_element_displayed(self._dnt_status)


class FrequentlyAskedQuestion(PageRegion):

    _question_locator = (By.CSS_SELECTOR, 'h3[role="tab"]')
    _answer_locator = (By.CSS_SELECTOR, 'div[role="tabpanel"]')

    def show_answer(self):
        assert not self.is_answer_displayed, 'Answer is already displayed'
        answer = self.root.find_element(*self._answer_locator)
        self.root.find_element(*self._question_locator).click()
        answer = self.root.find_element(*self._answer_locator)
        # Wait for aria-hidden attribute value to determine when animation has finished.
        Wait(self.selenium, self.timeout).until(
            lambda m: answer.get_attribute('aria-hidden') == 'false')

    def hide_answer(self):
        assert self.is_answer_displayed, 'Answer is already hidden'
        answer = self.root.find_element(*self._answer_locator)
        self.root.find_element(*self._question_locator).click()
        # Wait for aria-hidden attribute value to determine when animation has finished.
        Wait(self.selenium, self.timeout).until(
            lambda m: answer.get_attribute('aria-hidden') == 'true')

    @property
    def is_answer_displayed(self):
        return self.is_element_displayed(self._answer_locator)
