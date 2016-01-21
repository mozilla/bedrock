# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected

from base import BasePage
from page import PageRegion


class HomePage(BasePage):

    _promo_grid_locator = (By.CSS_SELECTOR, '.promo-grid.reveal')
    _promo_tile_locator = (By.CSS_SELECTOR, '.promo-grid > .item')
    _promo_tweet_locator = (By.ID, 'twt-body')
    _download_button_locator = (By.CSS_SELECTOR, '#download-button-desktop-release .download-link')

    @property
    def is_promo_grid_displayed(self):
        self.wait.until(expected.visibility_of_element_located(self._promo_grid_locator))
        return self.find_element(self._promo_grid_locator).is_displayed()

    @property
    def number_of_promos_present(self):
        return len(self.find_elements(self._promo_tile_locator))

    @property
    def is_tweet_promo_present(self):
        return self.is_element_present(self._promo_tweet_locator)

    @property
    def is_download_button_displayed(self):
        return self.download_button(self._download_button_locator).is_displayed()

    @property
    def upcoming_events(self):
        return UpcomingEvents(self)


class UpcomingEvents(PageRegion):

    _root_locator = (By.ID, 'upcoming-events')
    _next_event_locator = (By.CSS_SELECTOR, '.featured-event .event-detail > a')
    _events_list_locator = (By.CSS_SELECTOR, '.events-list')

    @property
    def is_next_event_displayed(self):
        return self.is_element_displayed(self._next_event_locator)

    @property
    def is_events_list_displayed(self):
        return self.is_element_displayed(self._events_list_locator)
