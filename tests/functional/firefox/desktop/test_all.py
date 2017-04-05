# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.desktop.all import FirefoxDesktopBasePage


@pytest.mark.skip_if_firefox(reason='Download button is not shown for up-to-date Firefox browsers.')
@pytest.mark.nondestructive
@pytest.mark.parametrize(('slug', 'locale'), [
    ('', None),
    ('customize', None),
    ('fast', 'de'),
    ('trust', None)])
def test_download_button_is_displayed(slug, locale, base_url, selenium):
    locale = locale or 'en-US'
    page = FirefoxDesktopBasePage(selenium, base_url, locale, slug=slug).open()
    assert page.download_button.is_displayed
