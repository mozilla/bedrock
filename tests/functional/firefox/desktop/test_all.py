# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.desktop.all import FirefoxDesktopBasePage


@pytest.mark.skip_if_firefox(reason='Download button is not shown for up-to-date Firefox browsers.')
@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    pytest.mark.smoke(''),
    ('customize'),
    ('fast'),
    ('trust')])
def test_download_button_is_displayed(slug, base_url, selenium):
    page = FirefoxDesktopBasePage(selenium, base_url, slug=slug).open()
    assert page.download_button.is_displayed
