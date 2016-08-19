# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.contribute.base import ContributeBasePage


class ContributeSignUpPage(ContributeBasePage):

    URL_TEMPLATE = '/{locale}/contribute/signup/'

    _twitter_task_locator = (By.CSS_SELECTOR, 'a[data-task="Connect with Mozilla on Twitter"]')
    _mobile_task_locator = (By.CSS_SELECTOR, 'a[data-task="Get Firefox on Your Phone"]')
    _encryption_task_locator = (By.CSS_SELECTOR, 'a[data-task="encryption"]')
    _joy_of_coding_task_locator = (By.CSS_SELECTOR, 'a[data-task="Joy of Coding"]')
    _dev_tools_challenger_task_locator = (By.CSS_SELECTOR, 'a[data-task="Learn about Coding"]')
    _stumbler_task_locator = (By.CSS_SELECTOR, 'a[data-task="Get Mozilla Stumbler"]')

    def open_twitter_task(self):
        self.find_element(*self._twitter_task_locator).click()
        from pages.contribute.task.twitter import TwitterTaskPage
        return TwitterTaskPage(self.selenium, self.base_url).wait_for_page_to_load()

    def open_mobile_task(self):
        self.find_element(*self._mobile_task_locator).click()
        from pages.contribute.task.mobile import MobileTaskPage
        return MobileTaskPage(self.selenium, self.base_url).wait_for_page_to_load()

    def open_encryption_task(self):
        self.find_element(*self._encryption_task_locator).click()
        from pages.contribute.task.encryption import EncryptionTaskPage
        return EncryptionTaskPage(self.selenium, self.base_url).wait_for_page_to_load()

    def open_joy_of_coding_task(self):
        self.find_element(*self._joy_of_coding_task_locator).click()
        from pages.contribute.task.joy_of_coding import JoyOfCodingTaskPage
        return JoyOfCodingTaskPage(self.selenium, self.base_url).wait_for_page_to_load()

    def open_dev_tools_challenger_task(self):
        self.find_element(*self._dev_tools_challenger_task_locator).click()
        from pages.contribute.task.dev_tools_challenger import DevToolsChallengerTaskPage
        return DevToolsChallengerTaskPage(self.selenium, self.base_url).wait_for_page_to_load()

    def open_stumbler_task(self):
        self.find_element(*self._stumbler_task_locator).click()
        from pages.contribute.task.stumbler import StumblerTaskPage
        return StumblerTaskPage(self.selenium, self.base_url).wait_for_page_to_load()
