# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pypom.view import WebView


def scroll_element_into_view(self, strategy, locator, x=0, y=0):
    el = self.find_element(strategy, locator)
    self.selenium.execute_script(
        'arguments[0].scrollIntoView();'
        'window.scrollBy(arguments[1], arguments[2]);', el, x, y)
    return el


WebView.scroll_element_into_view = scroll_element_into_view
