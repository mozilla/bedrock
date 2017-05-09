# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage
from pages.regions.news_feed import NewsFeed


class FirefoxAndroidHubPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/android/'

    _play_store_button_locator = (By.CSS_SELECTOR, '.header-download .google-play')

    @property
    def is_play_store_button_displayed(self):
        return self.is_element_displayed(*self._play_store_button_locator)

    @property
    def news_feed(self):
        return NewsFeed(self)
