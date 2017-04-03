# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as expected

from pypom import Page, Region
from regions.newsletter import NewsletterEmbedForm


class BasePage(Page):

    URL_TEMPLATE = '/{locale}'

    def __init__(self, selenium, base_url, locale='en-US', **url_kwargs):
        super(BasePage, self).__init__(selenium, base_url, locale=locale, **url_kwargs)

    _survey_message_locator = (By.ID, 'survey-message')
    _survey_close_button_locator = (By.CSS_SELECTOR, '#survey-message .survey-button-close')

    @property
    def is_survey_message_present(self):
        return self.is_element_present(*self._survey_message_locator)

    @property
    def is_survey_message_displayed(self):
        return self.is_element_displayed(*self._survey_message_locator)

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, 'html')
        self.wait.until(lambda s: 'loaded' in el.get_attribute('class'))
        # Bug 1341425: Task completion rate survey on mozilla.org
        if self.is_survey_message_present:
            if self.is_survey_message_displayed:
                survey = self.find_element(*self._survey_message_locator)
                self.wait.until(lambda s: 'animate' in survey.get_attribute('class'))
                self.wait.until(expected.element_to_be_clickable(self._survey_close_button_locator))
                self.find_element(*self._survey_close_button_locator).click()
                self.wait.until(lambda s: not self.is_survey_message_displayed)
        return self

    @property
    def navigation(self):
        return self.Navigation(self)

    @property
    def footer(self):
        return self.Footer(self)

    @property
    def newsletter(self):
        return NewsletterEmbedForm(self)

    class Navigation(Region):

        _root_locator = (By.ID, 'nav-main')
        _toggle_locator = (By.CLASS_NAME, 'toggle')
        _menu_locator = (By.ID, 'nav-main-menu')
        _internet_health_locator = (By.CSS_SELECTOR, 'a[data-link-name="Internet Health"]')
        _technology_locator = (By.CSS_SELECTOR, 'a[data-link-name="Web Innovations"]')

        def show(self):
            assert not self.is_displayed, 'Menu is already displayed'
            self.find_element(*self._toggle_locator).click()
            self.wait.until(lambda s: self.is_displayed)
            return self

        @property
        def is_displayed(self):
            toggle = self.find_element(*self._toggle_locator)
            return (self.find_element(*self._menu_locator).is_displayed() and
                toggle.get_attribute('aria-expanded') == 'true')

        def open_internet_health(self, locale='en-US'):
            self.find_element(*self._internet_health_locator).click()
            from internet_health import InternetHealthPage
            return InternetHealthPage(self.selenium, self.page.base_url, locale).wait_for_page_to_load()

        def open_technology(self, locale='en-US'):
            self.find_element(*self._technology_locator).click()
            from technology import TechnologyPage
            return TechnologyPage(self.selenium, self.page.base_url, locale).wait_for_page_to_load()

    class Footer(Region):

        _root_locator = (By.ID, 'colophon')
        _language_locator = (By.ID, 'page-language-select')

        @property
        def language(self):
            select = self.find_element(*self._language_locator)
            option = select.find_element(By.CSS_SELECTOR, 'option[selected]')
            return option.get_attribute('value')

        @property
        def languages(self):
            el = self.find_element(*self._language_locator)
            return [o.get_attribute('value') for o in Select(el).options]

        def select_language(self, value):
            el = self.find_element(*self._language_locator)
            Select(el).select_by_value(value)
            self.wait.until(lambda s: '/{0}/'.format(value) in s.current_url)
