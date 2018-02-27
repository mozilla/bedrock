# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom import Region

from pages.base import BasePage


class ScrollElementIntoView(object):

    def scroll_element_into_view(self, strategy, locator):
        # scroll elements so they are not beneath the header
        offset = {'x': 0, 'y': -100}
        return super(ScrollElementIntoView, self).scroll_element_into_view(
            strategy, locator, **offset)


class FirefoxBaseRegion(ScrollElementIntoView, Region):
    pass


class FirefoxBasePage(ScrollElementIntoView, BasePage):
    pass
