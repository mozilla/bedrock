# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class ContainsEverything(object):
    """An object whose instances will claim to contain anything."""
    def __contains__(self, item):
        return True
