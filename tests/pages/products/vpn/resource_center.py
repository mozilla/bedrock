# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage


class VPNResourceCenterHomePage(BasePage):
    _URL_TEMPLATE = "/{locale}/products/vpn/resource-center/"

    # Header unit
    _resource_center_header_locator = (By.CSS_SELECTOR, ".mzp-c-call-out.resource-center-page-header.resource-center-hero")

    # Article link
    _resource_center_article_link_locator = (By.CSS_SELECTOR, ".resource-center-articles .mzp-c-card a.mzp-c-card-block-link")

    @property
    def is_resource_center_header_displayed(self):
        return self.is_element_displayed(*self._resource_center_header_locator)

    @property
    def is_article_card_with_link_displayed(self):
        return self.is_element_displayed(*self._resource_center_article_link_locator)
