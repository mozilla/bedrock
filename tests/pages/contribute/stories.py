# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.contribute.base import ContributeBasePage


class ContributeStoriesPage(ContributeBasePage):

    # We're specifically testing Shreya's story. Stories all use
    # a shared template so it's probably overkill to test them all.
    URL_TEMPLATE = '/{locale}/contribute/stories/shreyas/'

    _story_locator = (By.CLASS_NAME, 'story-more')
    _story_toggle_locator = (By.CSS_SELECTOR, '.more-toggle > button')

    def show_story(self):
        assert not self.is_story_displayed, 'Story is already displayed'
        self.find_element(*self._story_toggle_locator).click()
        story = self.find_element(*self._story_locator)
        # Wait for aria-hidden attribute value to determine when animation has finished.
        self.wait.until(lambda m: story.get_attribute('aria-hidden') == 'false')

    def hide_story(self):
        assert self.is_story_displayed, 'Story is already hidden'
        self.find_element(*self._story_toggle_locator).click()
        story = self.find_element(*self._story_locator)
        # Wait for aria-hidden attribute value to determine when animation has finished.
        self.wait.until(lambda m: story.get_attribute('aria-hidden') == 'true')

    @property
    def is_story_displayed(self):
        return self.is_element_displayed(*self._story_locator)
