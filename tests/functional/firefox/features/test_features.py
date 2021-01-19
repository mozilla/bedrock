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


@pytest.mark.skip_if_firefox(reason='Sticky promo is displayed only to non-Firefox users')
@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    ('private-browsing')])
def test_sticky_promo(slug, base_url, selenium):
    page = FeaturePage(selenium, base_url, slug=slug).open()
    assert page.promo.is_displayed
    page.promo.close()
    assert not page.promo.is_displayed
