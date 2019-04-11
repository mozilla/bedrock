# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.all import FirefoxAllPage


@pytest.mark.nondestructive
def test_search_language(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    language = 'english'
    page.search_for(language)
    for build in page.displayed_builds:
        assert language in build.language.lower()
