# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region
from selenium.webdriver.common.by import By


class NewsFeed(Region):

    _root_locator = (By.CLASS_NAME, 'news-feed')
    _article_locator = (By.CLASS_NAME, 'entry')

    @property
    def articles(self):
        els = [el for el in self.find_elements(*self._article_locator)
               if el.is_displayed()]
        assert len(els) > 0, 'Expected at least one news feed item to be displayed'
        return els
