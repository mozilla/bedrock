# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.features.feature import FeaturePage


@pytest.mark.skip_if_firefox(reason="Download button is displayed only to non-Firefox users")
@pytest.mark.nondestructive
@pytest.mark.parametrize(
    "slug",
    [
        ("adblocker"),
        ("add-ons"),
        ("block-fingerprinting"),
        ("bookmarks"),
        ("customize"),
        ("eyedropper"),
        ("fast"),
        ("password-manager"),
        ("pdf-editor"),
        ("picture-in-picture"),
        ("pinned-tabs"),
        ("private-browsing"),
        ("private"),
        ("sync"),
        ("translate"),
    ],
)
def test_download_button_is_displayed(slug, base_url, selenium):
    page = FeaturePage(selenium, base_url, slug=slug).open()
    assert page.download_button.is_displayed
