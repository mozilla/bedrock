# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.new.thank_you import ThankYouPage


@pytest.mark.skip_if_internet_explorer(reason='https://github.com/SeleniumHQ/selenium/issues/448')
@pytest.mark.smoke
@pytest.mark.sanity
@pytest.mark.nondestructive
def test_direct_download_link_thank_you(base_url, selenium):
    page = ThankYouPage(base_url, selenium).open()
    assert page.is_direct_download_link_displayed
    assert page.is_direct_download_link_valid
