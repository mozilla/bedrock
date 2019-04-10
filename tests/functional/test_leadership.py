# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random
import pytest

from pages.leadership import LeadershipPage


@pytest.mark.nondestructive
def test_open_corporation_biography(base_url, selenium):
    page = LeadershipPage(selenium, base_url).open()
    leader = random.choice(page.corporation)
    modal = page.open_biography(leader)
    assert modal.is_displayed
    assert page.is_biography_displayed(leader)
    next_leader = page.get_next_leader(leader, page.corporation)
    page.click_next()
    assert page.is_biography_displayed(next_leader)
    page.click_previous()
    assert page.is_biography_displayed(leader)
    modal.close()


@pytest.mark.nondestructive
def test_open_foundation_biography(base_url, selenium):
    page = LeadershipPage(selenium, base_url).open()
    leader = random.choice(page.foundation)
    modal = page.open_biography(leader)
    assert modal.is_displayed
    assert page.is_biography_displayed(leader)
    next_leader = page.get_next_leader(leader, page.foundation)
    page.click_next()
    assert page.is_biography_displayed(next_leader)
    page.click_previous()
    assert page.is_biography_displayed(leader)
    modal.close()
