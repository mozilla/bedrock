# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.internet_health import InternetHealthPage


@pytest.mark.skip_if_firefox(reason='https://github.com/mozilla/bedrock/issues/6629')
@pytest.mark.nondestructive
def test_download_button_is_displayed(base_url, selenium):
    page = InternetHealthPage(selenium, base_url).open()
    assert page.download_button.is_displayed
