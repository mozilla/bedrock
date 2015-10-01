# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

import pytest

from ..pages.home import HomePage


@pytest.mark.nondestructive
def test_change_language(base_url, selenium):
    page = HomePage(base_url, selenium).open()
    initial = page.footer.language
    available = page.footer.languages
    available.remove(initial)  # avoid selecting the same language
    new = random.choice(available)  # pick a random lanugage
    page.footer.select_language(new)
    assert new in selenium.current_url, 'Language is not in URL'
    assert new == page.footer.language, 'Language has not been selected'
