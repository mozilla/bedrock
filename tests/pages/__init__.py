# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Fix for pypom being incompatible with Python 3.10+ due to
# "Moved Collections Abstract Base Classes to the collections.abc module."
import collections
import collections.abc

# Shim `collections.Iterable`` for pypom.
# Workaround for pyupgrade trying to rewrite `collections.Iterable` to `collections.abc.Iterable`.
setattr(collections, "Iterable", collections.abc.Iterable)


# The above is set before importing ``WebView`` to avoid ``AttributeError``.
from pypom.view import WebView  # noqa: E402


def scroll_element_into_view(self, strategy, locator, x=0, y=0):
    el = self.find_element(strategy, locator)
    self.selenium.execute_script("arguments[0].scrollIntoView();window.scrollBy(arguments[1], arguments[2]);", el, x, y)
    return el


def set_attribute(self, el, att_name, att_value):
    self.selenium.execute_script("arguments[0].setAttribute(arguments[1], arguments[2]);", el, att_name, att_value)
    return el


WebView.scroll_element_into_view = scroll_element_into_view
WebView.set_attribute = set_attribute
