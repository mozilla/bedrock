# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class ElectionPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/election/'

    _facebook_container_button_locator = (By.ID, 'facebook-container-button')
    _pro_republica_button_locator = (By.ID, 'pro-republica-button')
    _funnelcake_download_button_locator = (By.CSS_SELECTOR, '#case-funnel .download-link')

    @property
    def is_facebook_container_button_displayed(self):
        return self.is_element_displayed(*self._facebook_container_button_locator)

    @property
    def is_pro_republica_button_displayed(self):
        return self.is_element_displayed(*self._pro_republica_button_locator)

    @property
    def is_funnelcake_download_button_displayed(self):
        els = [el for el in self.find_elements(*self._funnelcake_download_button_locator)
        if el.is_displayed()]
        assert len(els) == 1, 'Expected one platform link to be displayed'
        return els[0]
