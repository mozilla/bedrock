# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.internet_health import InternetHealthPage


@pytest.mark.nondestructive
def test_blog_feed_is_displayed(base_url, selenium):
    page = InternetHealthPage(selenium, base_url).open()
    assert page.is_blog_feed_displayed
    assert page.number_of_blog_articles_present == 3
