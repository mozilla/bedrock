# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

import pytest

from pages.firefox.new.download import DownloadPage


@pytest.mark.nondestructive
def test_change_language(base_url, selenium):
    page = DownloadPage(selenium, base_url, params='').open()
    initial = page.footer.language
    # avoid selecting the same language or locales that have homepage redirects
    excluded = [initial, 'ja', 'ja-JP-mac', 'zh-CN']
    available = [l for l in page.footer.languages if l not in excluded]
    new = random.choice(available)
    page.footer.select_language(new)
    assert '/{0}/'.format(new) in selenium.current_url, 'Language is not in URL'
    assert new == page.footer.language, 'Language has not been selected'
