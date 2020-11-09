# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.sticky_promo import StickyPromoProtocol


class StickyPromo(BasePage):

    URL_TEMPLATE = '/{locale}/firefox/new/{params}'

    _sticky_promo_modal_content_locator = (By.CLASS_NAME, 'mzp-c-sticky-promo')

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.seed_url in s.current_url)
        el = self.find_element(By.TAG_NAME, 'html')
        self.wait.until(lambda s: 'loaded' in el.get_attribute('class'))
        return self

    @property
    def is_sticky_promo_displayed(self):
        return self.is_element_displayed(*self._sticky_promo_modal_content_locator)

    # @property
    # def open_sticky_promo_modal(self):
    #     stickyPromo = StickyPromoProtocol(self)
    #     self.wait.until(lambda s: stickyPromo.displays(self._sticky_promo_modal_content_locator))
    #     return stickyPromo.wait_for_page_to_load
