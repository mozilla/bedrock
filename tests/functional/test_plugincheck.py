# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.plugincheck import PluginCheckPage


@pytest.mark.skip_if_firefox
@pytest.mark.nondestructive
def test_not_supported_message(base_url, selenium):
    page = PluginCheckPage(base_url, selenium).open()
    assert page.is_not_supported_message_displayed


@pytest.mark.skip_if_not_firefox(reason='https://bugzilla.mozilla.org/show_bug.cgi?id=1245208')
@pytest.mark.smoke
@pytest.mark.nondestructive
def test_newsletter_default_values(base_url, selenium):
    page = PluginCheckPage(base_url, selenium).open()
    page.newsletter.expand_form()
    assert '' == page.newsletter.email
    assert 'United States' == page.newsletter.country
    assert not page.newsletter.privacy_policy_accepted
    assert page.newsletter.is_privacy_policy_link_displayed
