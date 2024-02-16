# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.all import FirefoxAllPage


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_release(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product("Firefox")
    product.select_platform("Windows 64-bit")
    product.select_language("English (US)")
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-latest-ssl" and "os=win64" and "lang=en-US" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_beta(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product("Firefox Beta")
    product.select_platform("macOS")
    product.select_language("German — Deutsch")
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-beta-latest-ssl" and "os=osx" and "lang=de" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_developer(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product("Firefox Developer Edition")
    product.select_platform("Linux 64-bit")
    product.select_language("English (US)")
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-devedition-latest-ssl" and "os=linux64" and "lang=en-US" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_nightly(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product("Firefox Nightly")
    product.select_platform("Windows 32-bit")
    product.select_language("German — Deutsch")
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-nightly-latest-ssl" and "os=win" and "lang=de" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_esr(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product("Firefox Extended Support Release")
    product.select_platform("Linux 32-bit")
    product.select_language("English (US)")
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-esr-latest-ssl" and "os=linux" and "lang=en-US" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_android(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    page.select_product("Firefox Android")
    assert page.is_android_download_button_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_android_beta(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    page.select_product("Firefox Android Beta")
    assert page.is_android_beta_download_button_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_android_nightly(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    page.select_product("Firefox Android Nightly")
    assert page.is_android_nightly_download_button_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_ios(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    page.select_product("Firefox iOS")
    assert page.is_ios_download_button_displayed
