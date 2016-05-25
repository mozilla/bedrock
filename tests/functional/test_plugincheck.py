# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.plugincheck import PluginCheckPage


@pytest.mark.skip_if_firefox(reason='Not supported message is shown only to non-Firefox browsers.')
@pytest.mark.nondestructive
def test_not_supported_message(base_url, selenium):
    page = PluginCheckPage(selenium, base_url).open()
    assert page.is_not_supported_message_displayed
