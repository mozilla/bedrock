# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from pages.base import BasePage
from pages.regions.send_to_device import SendToDevice


class FirefoxWhatsNew81Page(BasePage):

    _URL_TEMPLATE = '/{locale}/firefox/81.0/whatsnew/all/'

    @property
    def send_to_device(self):
        return SendToDevice(self)
