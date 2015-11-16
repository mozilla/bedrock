# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.contribute.signup import ContributeSignUpPage


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1225170')
def test_toggle_category_with_areas(base_url, selenium):
    page = ContributeSignUpPage(base_url, selenium).open()
    page.select_coding_category()
    assert page.is_areas_region_displayed
    assert page.is_coding_area_displayed
    assert page.is_coding_area_required


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1225170')
def test_toggle_category_without_areas(base_url, selenium):
    page = ContributeSignUpPage(base_url, selenium).open()
    page.select_helping_category()
    assert not page.is_areas_region_displayed


@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1225170')
def test_successful_sign_up_coding(base_url, selenium):
    page = ContributeSignUpPage(base_url, selenium).open()
    page.select_coding_category()
    page.select_coding_area('Firefox')
    page.type_name('Automated test')
    page.type_email('noreply@mozilla.com')
    page.select_country('United Kingdom')
    page.select_text_format()
    page.accept_privacy_policy()
    page.click_start_contributing()
    assert '/{0}'.format('?c=coding') in selenium.current_url, 'Category is not in URL'


@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1221526')
def test_successful_sign_up_helping(base_url, selenium):
    page = ContributeSignUpPage(base_url, selenium).open()
    page.select_helping_category()
    page.type_name('Automated test')
    page.type_email('noreply@mozilla.com')
    page.select_country('United Kingdom')
    page.select_text_format()
    page.accept_privacy_policy()
    page.click_start_contributing()
    assert '/{0}'.format('?c=helping') in selenium.current_url, 'Category is not in URL'


@pytest.mark.nondestructive
@pytest.mark.skipif(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1225170')
def test_sign_up_fails_when_missing_required_fields(base_url, selenium):
    page = ContributeSignUpPage(base_url, selenium).open()
    with pytest.raises(TimeoutException):
        page.click_start_contributing()
