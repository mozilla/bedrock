# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.modal import ModalProtocol


class FirefoxAllPage(BasePage):
    _URL_TEMPLATE = "/{locale}/firefox/download/all/{slug}"

    # help modals

    def open_help_modal(self, value):
        modal = ModalProtocol(self)
        self.find_element(*(By.ID, value)).click()
        self.wait.until(lambda s: modal.is_displayed)
        return modal
