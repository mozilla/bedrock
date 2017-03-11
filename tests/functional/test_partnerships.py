# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.partnerships import PartnershipsPage


@pytest.mark.skipif(reason='Need to find a non-destructive solution for testing submission of form')
@pytest.mark.nondestructive
def test_request_partnership(base_url, selenium):
    page = PartnershipsPage(selenium, base_url).open()
    page.type_first_name('Automated')
    page.type_last_name('Test')
    page.type_company('Mozilla')
    page.type_email('success@example.com')
    page.submit_request()
    assert page.request_successful


@pytest.mark.nondestructive
def test_request_fails_when_missing_required_fields(base_url, selenium):
    page = PartnershipsPage(selenium, base_url).open()
    with pytest.raises(TimeoutException):
        page.submit_request()
