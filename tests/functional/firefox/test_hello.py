# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.hello import HelloPage


@pytest.mark.smoke
@pytest.mark.skipif(reason='Skipped until Firefox 45 is available on Sauce Labs')
@pytest.mark.skip_if_not_firefox(reason='Hello button is shown only to Firefox browsers.')
@pytest.mark.nondestructive
def test_try_hello_button_is_displayed(base_url, selenium):
    page = HelloPage(base_url, selenium).open()
    assert page.is_try_hello_header_button_displayed
    assert page.is_try_hello_footer_button_displayed


@pytest.mark.smoke
@pytest.mark.skip_if_firefox(reason='Download button is not shown for Firefox browsers.')
@pytest.mark.nondestructive
def test_download_button_is_displayed(base_url, selenium):
    page = HelloPage(base_url, selenium).open()
    assert page.primary_download_button.is_displayed
    assert page.secondary_download_button.is_displayed
