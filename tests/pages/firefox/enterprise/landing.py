# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class EnterprisePage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/enterprise/'

    _primary_download_button_locator = (By.ID, 'primary-download-button')
    _comparison_download_button_locator = (By.ID, 'comparison-download-button')
    _comparison_sales_button_locator = (By.ID, 'comparison-sales-button')
    _comparison_tab_button_basic_locator = (By.ID, 'pager-tab-button-basic')
    _comparison_tab_button_premium_locator = (By.ID, 'pager-tab-button-premium')
    _comparison_basic_plan_locator = (By.ID, 'pager-page-basic')
    _comparison_premium_plan_locator = (By.ID, 'pager-page-premium')
    _package_win64_download_button_locator = (By.ID, 'package-win64-download-button')
    _package_mac_download_button_locator = (By.ID, 'package-mac-download-button')
    _package_win32_download_button_locator = (By.ID, 'package-win32-download-button')

    @property
    def is_primary_download_button_displayed(self):
        return self.is_element_displayed(*self._primary_download_button_locator)

    @property
    def is_comparison_download_button_displayed(self):
        return self.is_element_displayed(*self._comparison_download_button_locator)

    @property
    def is_comparison_sales_button_displayed(self):
        return self.is_element_displayed(*self._comparison_sales_button_locator)

    @property
    def is_comparison_basic_tab_button_displayed(self):
        return self.is_element_displayed(*self._comparison_tab_button_basic_locator)

    @property
    def is_comparison_premium_tab_button_displayed(self):
        return self.is_element_displayed(*self._comparison_tab_button_premium_locator)

    @property
    def is_comparison_premium_plan_displayed(self):
        return self.is_element_displayed(*self._comparison_premium_plan_locator)

    @property
    def is_comparison_basic_plan_displayed(self):
        return self.is_element_displayed(*self._comparison_basic_plan_locator)

    @property
    def is_package_win64_download_button_displayed(self):
        return self.is_element_displayed(*self._package_win64_download_button_locator)

    @property
    def is_package_mac_download_button_displayed(self):
        return self.is_element_displayed(*self._package_mac_download_button_locator)

    @property
    def is_package_win32_download_button_displayed(self):
        return self.is_element_displayed(*self._package_win32_download_button_locator)

    def click_premium_plan_tab_button(self):
        self.find_element(*self._comparison_tab_button_premium_locator).click()
        self.wait.until(lambda s: self.is_comparison_premium_plan_displayed)

    def click_basic_plan_tab_button(self):
        self.find_element(*self._comparison_tab_button_basic_locator).click()
        self.wait.until(lambda s: self.is_comparison_basic_plan_displayed)

    def click_contact_sales_button(self):
        self.find_element(*self._comparison_sales_button_locator).click()
        from pages.firefox.enterprise.signup import EnterpriseSignUpPage
        return EnterpriseSignUpPage(self.selenium, self.base_url).wait_for_page_to_load()
