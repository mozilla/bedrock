# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.whatsnew.whatsnew_124 import FirefoxWhatsNew124Page


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
@pytest.mark.parametrize("params", [("?v=1&geo=us"), ("?v=2&geo=us")])
def test_monitor_free_scan_button_displayed(params, base_url, selenium):
    page = FirefoxWhatsNew124Page(selenium, base_url, params=params).open()
    assert page.is_monitor_free_scan_button_displayed


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
def test_set_as_default_button_displayed(base_url, selenium):
    page = FirefoxWhatsNew124Page(selenium, base_url, locale="de", params="?v=1").open()
    assert page.is_set_as_default_button_displayed


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
def test_youtube_channel_button_displayed(base_url, selenium):
    page = FirefoxWhatsNew124Page(selenium, base_url, locale="de", params="?v=2").open()
    assert page.is_youtube_channel_button_displayed


@pytest.mark.skip_if_not_firefox(reason="Whatsnew pages are shown to Firefox only.")
@pytest.mark.nondestructive
def test_share_modal_displayed(base_url, selenium):
    page = FirefoxWhatsNew124Page(selenium, base_url, locale="de", params="?v=3").open()
    page.open_share_modal()
    assert page.is_share_copy_button_displayed
