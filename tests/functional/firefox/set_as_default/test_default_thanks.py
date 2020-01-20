# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.set_as_default.thanks import DefaultThanksPage


@pytest.mark.nondestructive
@pytest.mark.skip_if_firefox(reason='Download button is only displayed to non-Firefox visitors.')
def test_download_button_is_displayed(base_url, selenium):
    page = DefaultThanksPage(selenium, base_url).open()
    assert page.download_button.is_displayed
