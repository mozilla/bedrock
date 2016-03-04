# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.win10_welcome import Win10WelcomePage


@pytest.mark.skip_if_firefox(reason='Firefox content is dependent on UITour API.')
@pytest.mark.nondestructive
def test_first_run(base_url, selenium):
    page = Win10WelcomePage(base_url, selenium).open()
    assert page.is_firefox_default_messaging_displayed
    assert page.is_links_section_displayed
