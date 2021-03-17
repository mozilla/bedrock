# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_87 import FirefoxWhatsNew87Page


@pytest.mark.nondestructive
def test_sign_up_success_de(base_url, selenium):
    page = FirefoxWhatsNew87Page(selenium, base_url, locale='de').open()
    page.type_email('success@example.com')
    page.select_country('Deutschland')
    page.select_language('Deutsch')
    page.click_sign_me_up()
    assert page.is_form_success_displayed


@pytest.mark.nondestructive
def test_sign_up_failure_de(base_url, selenium):
    page = FirefoxWhatsNew87Page(selenium, base_url, locale='de').open()
    page.type_email('invalid@email')
    page.select_country('Deutschland')
    page.select_language('Deutsch')
    page.click_sign_me_up(expected_result='error')
    assert page.is_form_error_displayed


@pytest.mark.nondestructive
def test_sign_up_success_fr(base_url, selenium):
    page = FirefoxWhatsNew87Page(selenium, base_url, locale='fr').open()
    page.type_email('success@example.com')
    page.select_country('France')
    page.select_language('Français')
    page.click_sign_me_up()
    assert page.is_form_success_displayed


@pytest.mark.nondestructive
def test_sign_up_failure_fr(base_url, selenium):
    page = FirefoxWhatsNew87Page(selenium, base_url, locale='fr').open()
    page.type_email('invalid@email')
    page.select_country('France')
    page.select_language('Français')
    page.click_sign_me_up(expected_result='error')
    assert page.is_form_error_displayed
