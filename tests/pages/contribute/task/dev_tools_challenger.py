# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.contribute.base import ContributeBasePage
from pages.regions.download_button import DownloadButton


class DevToolsChallengerTaskPage(ContributeBasePage):

    URL_TEMPLATE = '/{locale}/contribute/task/devtools-challenger/'

    _download_button_locator = (By.ID, 'download-button-desktop-alpha')
    _visit_dev_tools_challenger_locator = (By.CSS_SELECTOR, 'a[data-task="devtools"]')

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def is_visit_dev_tools_challenger_button_displayed(self):
        return self.is_element_displayed(*self._visit_dev_tools_challenger_locator)
