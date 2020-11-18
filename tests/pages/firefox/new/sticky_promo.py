# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.sticky_promo import StickyPromo


class StickyPromoPage(BasePage):

    URL_TEMPLATE = '/{locale}/firefox/new/'

    _sticky_promo_modal_content_locator = (By.CSS_SELECTOR, '.mzp-c-sticky-promo.mzp-a-slide-in')

    def wait_for_page_to_load(self):
        el = self.find_element(By.TAG_NAME, 'html')
        self.wait.until(lambda s: 'loaded' in el.get_attribute('class'))
        promo = self.find_element(*self._sticky_promo_modal_content_locator)
        self.wait.until(lambda s: 'is-displayed' in promo.get_attribute('class'))
        return self

    @property
    def promo(self):
        return StickyPromo(self)
