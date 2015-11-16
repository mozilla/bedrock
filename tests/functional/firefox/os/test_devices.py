# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.os.devices import DevicesPage


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_family_navigation(base_url, selenium):
    page = DevicesPage(base_url, selenium).open()
    page.family_navigation.open_menu()
    assert page.family_navigation.is_menu_displayed


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_open_close_modal(base_url, selenium):
    page = DevicesPage(base_url, selenium).open()
    page.select_location('Germany')
    modal = page.get_a_phone()
    assert modal.is_displayed
    modal.close()


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_open_close_phone(base_url, selenium):
    page = DevicesPage(base_url, selenium).open()
    phone = page.open_phone_detail()
    assert phone.is_displayed
    assert phone.is_features_displayed
    phone.close()
    assert not phone.is_displayed
    assert not phone.is_features_displayed


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_open_close_tv(base_url, selenium):
    page = DevicesPage(base_url, selenium).open()
    tv = page.open_tv_detail()
    assert tv.is_displayed
    assert tv.is_features_displayed
    tv.close()
    assert not tv.is_displayed
    assert not tv.is_features_displayed


@pytest.mark.sanity
@pytest.mark.nondestructive
def test_toggle_detail_tabs(base_url, selenium):
    page = DevicesPage(base_url, selenium).open()
    phone = page.open_phone_detail()
    assert not phone.is_specifications_displayed
    phone.show_specifications()
    assert phone.is_specifications_displayed
    phone.show_features()
    assert not phone.is_specifications_displayed
    assert phone.is_features_displayed
    phone.close()
