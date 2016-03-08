# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.contribute.base import ContributeBasePage


class ContributeFriendsPage(ContributeBasePage):

    _url = '{base_url}/{locale}/contribute/friends'

    _privacy_policy_link_locator = (By.CSS_SELECTOR, 'label[for="id_privacy"] a')
    _show_signup_form_button_locator = (By.ID, 'ff-show-signup-form')
    _signup_form_locator = (By.ID, 'newsletter-form')

    @property
    def is_signup_form_displayed(self):
        return self.is_element_displayed(self._signup_form_locator)

    @property
    def is_privacy_policy_link_displayed(self):
        return self.is_element_displayed(self._privacy_policy_link_locator)

    def click_show_signup_form(self):
        assert not self.is_signup_form_displayed, 'Form is already displayed'
        self.find_element(self._show_signup_form_button_locator).click()
        self.wait.until(lambda s: self.is_privacy_policy_link_displayed)
