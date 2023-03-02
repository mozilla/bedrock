# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.contact import ContactPage, SpacesPage


@pytest.mark.nondestructive
def test_tab_navigation(base_url, selenium):
    contact_page = ContactPage(selenium, base_url).open()
    assert contact_page.contact_tab.is_selected
    assert not contact_page.spaces_tab.is_selected

    spaces_page = SpacesPage(selenium, base_url, slug="").open()
    assert not spaces_page.contact_tab.is_selected
    assert spaces_page.spaces_tab.is_selected


@pytest.mark.nondestructive
@pytest.mark.parametrize("slug", [("toronto/"), ("san-francisco/"), ("berlin/"), ("paris/"), ("beijing/")])
def test_spaces_menus(slug, base_url, selenium):
    page = SpacesPage(selenium, base_url, slug=slug).open()
    space_menu = [s for s in page.spaces if s.id in slug]
    assert len(space_menu) == 1
    assert space_menu[0].is_selected


@pytest.mark.nondestructive
def test_spaces_mobile_navigation(base_url, selenium_mobile):
    page = SpacesPage(selenium_mobile, base_url, slug="").open()
    assert page.is_mobile_menu_toggle_displayed
    page.open_spaces_mobile_menu()
    assert page.is_nav_displayed
