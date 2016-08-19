# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.contribute.base import ContributeBasePage


class ContributeEventsPage(ContributeBasePage):

    URL_TEMPLATE = '/{locale}/contribute/events/'

    _events_table_locator = (By.CSS_SELECTOR, '.events-table > tbody > tr')

    @property
    def events_table_is_displayed(self):
        return self.is_element_displayed(*self._events_table_locator)
