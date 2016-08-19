# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.contact import ContactPage, SpacesPage, CommunitiesPage


@pytest.mark.nondestructive
def test_tab_navigation(base_url, selenium):
    page = ContactPage(selenium, base_url).open()
    assert page.contact_tab.is_selected
    assert not page.spaces_tab.is_selected
    assert not page.communities_tab.is_selected

    spaces_page = page.click_spaces_tab()
    assert not spaces_page.contact_tab.is_selected
    assert spaces_page.spaces_tab.is_selected
    assert not spaces_page.communities_tab.is_selected
    assert spaces_page.seed_url in selenium.current_url

    communities_page = spaces_page.click_communities_tab()
    assert not communities_page.contact_tab.is_selected
    assert not communities_page.spaces_tab.is_selected
    assert communities_page.communities_tab.is_selected
    assert communities_page.seed_url in selenium.current_url

    contact_page = communities_page.click_contact_tab()
    assert contact_page.contact_tab.is_selected
    assert not contact_page.spaces_tab.is_selected
    assert not contact_page.communities_tab.is_selected
    assert contact_page.seed_url in selenium.current_url


@pytest.mark.nondestructive
def test_spaces_list(base_url, selenium):
    page = SpacesPage(selenium, base_url).open()
    assert page.displayed_map_pins == len(page.spaces)
    for space in page.spaces:
        space.click()
        assert space.is_selected
        assert space.is_displayed
        assert 1 == page.displayed_map_pins


@pytest.mark.nondestructive
def test_communities_region_list(base_url, selenium):
    page = CommunitiesPage(selenium, base_url).open()
    for region in page.regions:
        region.click()
        assert region.is_selected
        assert region.is_displayed
        key = next(k for k in page.keys if k.id == region.id)
        assert key.is_selected


@pytest.mark.nondestructive
def test_communities_region_legend(base_url, selenium):
    page = CommunitiesPage(selenium, base_url).open()
    for key in page.keys:
        key.click()
        assert key.is_selected
        region = next(r for r in page.regions if r.id == key.id)
        assert region.is_selected
        assert region.is_displayed


@pytest.mark.nondestructive
def test_communities_region_menus(base_url, selenium):
    page = CommunitiesPage(selenium, base_url).open()
    north_america = page.regions[0]
    assert not north_america.is_menu_open
    north_america.click()
    assert north_america.is_menu_open
    canada = north_america.communities[0]
    assert not canada.is_selected
    assert not canada.is_displayed
    canada.click()
    assert canada.is_selected
    assert canada.is_displayed
    page.regions[1].click()
    assert not north_america.is_menu_open
    assert not canada.is_selected
    assert not canada.is_displayed
