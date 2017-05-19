# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class InternetHealthPage(BasePage):

    URL_TEMPLATE = '/{locale}/internet-health'

    _blog_feed_locator = (By.CLASS_NAME, 'news-feed')
    _blog_feed_articles_locator = (By.CSS_SELECTOR, '.news-feed article')

    @property
    def is_blog_feed_displayed(self):
        return self.is_element_displayed(*self._blog_feed_locator)

    @property
    def number_of_blog_articles_present(self):
        return len(self.find_elements(*self._blog_feed_articles_locator))
