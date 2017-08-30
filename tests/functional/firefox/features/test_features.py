# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.features.feature import FeaturePage


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    ('private-browsing'),
    ('independent'),
    ('fast'),
    ('memory'),
    ('bookmarks'),
    ('password-manager')])
def test_download_button_is_displayed(slug, base_url, selenium):
    page = FeaturePage(selenium, base_url, slug=slug).open()
    assert page.download_button.is_displayed
