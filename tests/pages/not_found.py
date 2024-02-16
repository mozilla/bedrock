# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class NotFoundPage(BasePage):
    _URL_TEMPLATE = "/{locale}/404/"

    _go_back_button_locator = (By.ID, "go-back")

    @property
    def is_go_back_button_displayed(self):
        return self.is_element_displayed(*self._go_back_button_locator)
