# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.contact import ContactPage, SpacesPage, CommunitiesPage


@pytest.mark.nondestructive
def test_tab_navigation(base_url, selenium):
    contact_page = ContactPage(selenium, base_url).open()
    assert contact_page.contact_tab.is_selected
    assert not contact_page.spaces_tab.is_selected
    assert not contact_page.communities_tab.is_selected

    spaces_page = SpacesPage(selenium, base_url, slug='').open()
    assert not spaces_page.contact_tab.is_selected
    assert spaces_page.spaces_tab.is_selected
    assert not spaces_page.communities_tab.is_selected
    assert spaces_page.seed_url in selenium.current_url

    communities_page = CommunitiesPage(selenium, base_url, slug='').open()
    assert not communities_page.contact_tab.is_selected
    assert not communities_page.spaces_tab.is_selected
    assert communities_page.communities_tab.is_selected
    assert communities_page.seed_url in selenium.current_url


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    ('mountain-view'),
    ('beijing'),
    ('berlin'),
    ('london'),
    ('paris'),
    ('portland'),
    ('san-francisco'),
    ('taipei'),
    ('toronto'),
    ('vancouver')])
def test_spaces_menus(slug, base_url, selenium):
    page = SpacesPage(selenium, base_url, slug=slug).open()
    assert not page.is_mobile_nav_displayed
    space_menu = [s for s in page.spaces if s.id == slug]
    assert len(space_menu) == 1
    assert space_menu[0].is_selected


@pytest.mark.nondestructive
@pytest.mark.parametrize('slug', [
    ('north-america'),
    ('latin-america'),
    ('europe'),
    ('asia-south-pacific'),
    ('africa-middle-east')])
def test_communities_region_menus(slug, base_url, selenium):
    page = CommunitiesPage(selenium, base_url, slug=slug).open()
    assert not page.is_mobile_nav_displayed
    region_menu = [s for s in page.regions if s.id == slug]
    assert len(region_menu) == 1
    assert region_menu[0].is_selected
    assert region_menu[0].is_open
    for community in region_menu[0].communities:
        assert community.is_displayed


@pytest.mark.nondestructive
@pytest.mark.viewport('mobile')
def test_spaces_mobile_navigation(base_url, selenium):
    page = SpacesPage(selenium, base_url, slug='').open()
    assert not page.is_desktop_nav_displayed
    assert page.is_mobile_nav_displayed
    expected_url = '/contact/spaces/mountain-view/'
    page.select_mobile_nav_item('Mountain View', expected_url)
    assert expected_url in selenium.current_url, 'Page did not navigate to expected URL'


@pytest.mark.nondestructive
@pytest.mark.viewport('mobile')
def test_communities_mobile_navigation(base_url, selenium):
    page = CommunitiesPage(selenium, base_url, slug='').open()
    assert not page.is_desktop_nav_displayed
    assert page.is_mobile_nav_displayed
    expected_url = '/contact/communities/north-america/'
    page.select_mobile_nav_item('North America', expected_url)
    assert expected_url in selenium.current_url, 'Page did not navigate to expected URL'
