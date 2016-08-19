# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage, FirefoxBaseRegion


class DoNotTrackPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/dnt/'

    _dnt_status_locator = (By.CSS_SELECTOR, '#dnt-status > h5')
    _faqs_locator = (By.CSS_SELECTOR, '#faq > section')

    @property
    def frequently_asked_questions(self):
        return [FrequentlyAskedQuestion(self, root=el) for el in
                self.find_elements(*self._faqs_locator)]

    @property
    def is_do_not_track_status_displayed(self):
        return self.is_element_displayed(*self._dnt_status_locator)


class FrequentlyAskedQuestion(FirefoxBaseRegion):

    _question_locator = (By.CSS_SELECTOR, 'h3[role="tab"]')
    _answer_locator = (By.CSS_SELECTOR, 'div[role="tabpanel"]')

    def show_answer(self):
        assert not self.is_answer_displayed, 'Answer is already displayed'
        self.scroll_element_into_view(*self._question_locator).click()
        answer = self.find_element(*self._answer_locator)
        # Wait for aria-hidden attribute value to determine when animation has finished.
        self.wait.until(lambda m: answer.get_attribute('aria-hidden') == 'false')

    def hide_answer(self):
        assert self.is_answer_displayed, 'Answer is already hidden'
        self.find_element(*self._question_locator).click()
        answer = self.find_element(*self._answer_locator)
        # Wait for aria-hidden attribute value to determine when animation has finished.
        self.wait.until(lambda m: answer.get_attribute('aria-hidden') == 'true')

    @property
    def is_answer_displayed(self):
        return self.is_element_displayed(*self._answer_locator)
