# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

TIMEOUT = 10


class Page(object):

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


class PageRegion(object):

    _root_locator = None

    def __init__(self, selenium, root=None):
        self.selenium = selenium
        self.timeout = TIMEOUT
        self.root = root

        if self.root is None and self._root_locator is not None:
            self.root = self.selenium.find_element(*self._root_locator)
