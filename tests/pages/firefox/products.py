# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pages.base import BasePage
from pages.regions.join_firefox_form import JoinFirefoxForm


class FirefoxProductsPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/products/"

    @property
    def join_firefox_form(self):
        return JoinFirefoxForm(self)
