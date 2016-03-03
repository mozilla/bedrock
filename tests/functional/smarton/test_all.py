# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.smarton.base import SmartOnBasePage


@pytest.mark.skip_if_firefox(reason='Download button is not shown to Firefox browsers.')
@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    pytest.mark.smoke(('tracking')),
    ('security'),
    ('surveillance')])
def test_download_button_displayed(slug, base_url, selenium):
    page = SmartOnBasePage(base_url, selenium, slug=slug).open()
    assert page.download_button.is_displayed


@pytest.mark.skip_if_not_firefox(reason='Newsletter is only shown to Firefox browsers.')
@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    pytest.mark.smoke(('tracking')),
    ('security'),
    ('surveillance')])
def test_newsletter_default_values(slug, base_url, selenium):
    page = SmartOnBasePage(base_url, selenium, slug=slug).open()
    page.newsletter.expand_form()
    assert '' == page.newsletter.email
    assert 'United States' == page.newsletter.country
    assert not page.newsletter.privacy_policy_accepted
    assert page.newsletter.is_privacy_policy_link_displayed
