# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_67 import FirefoxWhatsNew67Page


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_signed_out_firefox_accounts_form_displayed(base_url, selenium):
    page = FirefoxWhatsNew67Page(selenium, base_url, params='').open()
    assert page.is_firefox_accounts_form_displayed


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_signed_in_newsletter_form_displayed(base_url, selenium):
    page = FirefoxWhatsNew67Page(selenium, base_url, params='?signed-in=true').open()
    assert page.is_newsletter_form_displayed


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_get_lockwise_modal_displayed(base_url, selenium):
    page = FirefoxWhatsNew67Page(selenium, base_url, params='').open()
    modal = page.click_get_lockwise_link()
    assert modal.is_displayed
    assert page.is_lockwise_qr_code_displayed
    modal.close()


@pytest.mark.skip_if_not_firefox(reason='Whatsnew pages are shown to Firefox only.')
@pytest.mark.nondestructive
def test_get_pocket_modal_displayed(base_url, selenium):
    page = FirefoxWhatsNew67Page(selenium, base_url, params='').open()
    modal = page.click_get_pocket_link()
    assert modal.is_displayed
    assert page.is_pocket_qr_code_displayed
    modal.close()
