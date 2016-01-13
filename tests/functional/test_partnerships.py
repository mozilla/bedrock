# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from selenium.common.exceptions import TimeoutException

from pages.partnerships import PartnershipsPage


@pytest.mark.flaky(reruns=1)
def test_request_partnership(base_url, selenium):
    page = PartnershipsPage(base_url, selenium).open()
    page.type_first_name('Automated')
    page.type_last_name('Test')
    page.type_company('Mozilla')
    page.type_email('noreply@mozilla.com')
    page.submit_request()
    assert page.request_successful


@pytest.mark.nondestructive
def test_request_fails_when_missing_required_fields(base_url, selenium):
    page = PartnershipsPage(base_url, selenium).open()
    with pytest.raises(TimeoutException):
        page.submit_request()
