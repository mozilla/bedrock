# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.download_button import DownloadButton
from pages.regions.sticky_promo import StickyPromo


class FeaturePage(BasePage):

    _URL_TEMPLATE = '/{locale}/firefox/features/{slug}/'

    _download_button_locator = (By.ID, 'features-header-download')

    # Used as a scroll target to move down the page, to trigger the sticky promo element
    _page_main_content_locator = (By.CSS_SELECTOR, '.main-content')

    _sticky_promo_modal_content_locator = (By.CSS_SELECTOR, '.mzp-c-sticky-promo')

    def init_promo(self):
        assert not self.is_promo_displayed, 'Promo detail is not displayed'
        # scroll down page to trigger promo to display
        self.scroll_element_into_view(*self._page_main_content_locator)

        if self.selenium.capabilities.get('browserName').lower() != 'firefox':
            promo = self.find_element(*self._sticky_promo_modal_content_locator)
            self.wait.until(lambda s: 'is-displayed' in promo.get_attribute('class'))

    @property
    def is_promo_displayed(self):
        return self.is_element_displayed(*self._sticky_promo_modal_content_locator)

    @property
    def download_button(self):
        el = self.find_element(*self._download_button_locator)
        return DownloadButton(self, root=el)

    @property
    def promo(self):
        return StickyPromo(self)
