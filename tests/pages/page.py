# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.common.exceptions import NoSuchElementException


TIMEOUT = 10


class ViewPort(object):

    def scroll_into_view(self, target_locator, offset_locator, padding=100):
        """
        Scroll an element into view at the top of the viewport offset by the height of
        another alement, such as a sticky navigation header.
        :param target_locator: locator of the element to scroll into view.
        :param offset_locator: locator of the element to offset the scroll height.
        :param padding: number of extra pixels padding to add to the offset.
        """
        target = self.selenium.find_element(*target_locator)
        offset = self.selenium.find_element(*offset_locator)
        height = offset.size.get('height') + padding
        self.selenium.execute_script('arguments[0].scrollIntoView();'
            'window.scrollBy(0, arguments[1]);', target, -height)


class Page(ViewPort):

    _url = None

    def __init__(self, base_url, selenium, locale='en-US'):
        self.base_url = base_url
        self.selenium = selenium
        self.locale = locale
        self.timeout = TIMEOUT

    def open(self):
        self.selenium.get(self.url)
        self.wait_for_page_to_load()
        return self

    @property
    def url(self):
        if self._url is not None:
            return self._url.format(base_url=self.base_url, locale=self.locale)
        return self.base_url

    def wait_for_page_to_load(self):
        return self

    def is_element_present(self, locator):
        try:
            return self.selenium.find_element(*locator)
        except (NoSuchElementException):
            return False

    def is_element_displayed(self, locator):
        try:
            return self.selenium.find_element(*locator).is_displayed()
        except (NoSuchElementException):
            return False


class PageRegion(ViewPort):

    _root_locator = None

    def __init__(self, selenium, root=None):
        self.selenium = selenium
        self.timeout = TIMEOUT
        self.root_element = root

    @property
    def root(self):
        if self.root_element is None and self._root_locator is not None:
            self.root_element = self.selenium.find_element(*self._root_locator)
        return self.root_element

    def is_element_present(self, locator):
        try:
            return self.root.find_element(*locator)
        except (NoSuchElementException):
            return False

    def is_element_displayed(self, locator):
        try:
            return self.root.find_element(*locator).is_displayed()
        except (NoSuchElementException):
            return False
