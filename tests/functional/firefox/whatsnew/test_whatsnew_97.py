# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_97 import FirefoxWhatsNew97Page


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
def test_pocket_button_is_displayed(base_url, selenium):
    page = FirefoxWhatsNew97Page(selenium, base_url, locale="en-US").open()
    assert page.is_pocket_button_displayed


@pytest.mark.skip_if_not_firefox(reason="Welcome pages are shown to Firefox only.")
@pytest.mark.nondestructive
def test_open_video_modal_de(base_url, selenium):
    page = FirefoxWhatsNew97Page(selenium, base_url, locale="de").open()
    modal = page.click_modal_button()
    assert modal.is_displayed
    modal.close()


@pytest.mark.skip_if_not_firefox(reason="Welcome pages are shown to Firefox only.")
@pytest.mark.nondestructive
def test_open_video_modal_fr(base_url, selenium):
    page = FirefoxWhatsNew97Page(selenium, base_url, locale="fr").open()
    modal = page.click_modal_button()
    assert modal.is_displayed
    modal.close()
