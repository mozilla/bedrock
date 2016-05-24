# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class ContributeBasePage(BasePage):

    _next_event_link_locator = (By.CSS_SELECTOR, '.extra-event .event-link')

    @property
    def next_event_is_displayed(self):
        return self.is_element_displayed(*self._next_event_link_locator)
