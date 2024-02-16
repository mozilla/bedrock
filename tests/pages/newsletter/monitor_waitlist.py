# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class MonitorWaitlistNewsletterPage(BasePage):
    _URL_TEMPLATE = "/{locale}/newsletter/monitor-waitlist/{params}"

    _unavailable_country_message_locator = (By.CLASS_NAME, "c-not-available")

    @property
    def is_unavailable_country_message_displayed(self):
        return self.is_element_displayed(*self._unavailable_country_message_locator)
