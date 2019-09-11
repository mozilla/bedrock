# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.all import FirefoxAllPage


@pytest.mark.nondestructive
def test_firefox_release(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product('Firefox')
    product.select_platform('Windows 64-bit')
    product.select_language('English (US)')
    assert page.is_download_button_displayed
    assert page.is_download_link_valid
    assert 'product=firefox-latest-ssl' and 'os=win64' and 'lang=en-US' in page.download_link


@pytest.mark.nondestructive
def test_firefox_beta(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product('Firefox Beta')
    product.select_platform('macOS')
    product.select_language(u'German — Deutsch')
    assert page.is_download_button_displayed
    assert page.is_download_link_valid
    assert 'product=firefox-beta-latest-ssl' and 'os=osx' and 'lang=de' in page.download_link


@pytest.mark.nondestructive
def test_firefox_developer(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product('Firefox Developer Edition')
    product.select_platform('Linux 64-bit')
    product.select_language('English (US)')
    assert page.is_download_button_displayed
    assert page.is_download_link_valid
    assert 'product=firefox-devedition-latest-ssl' and 'os=linux64' and 'lang=en-US' in page.download_link


@pytest.mark.nondestructive
def test_firefox_nightly(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product('Firefox Nightly')
    product.select_platform('Windows 32-bit')
    product.select_language(u'German — Deutsch')
    assert page.is_download_button_displayed
    assert page.is_download_link_valid
    assert 'product=firefox-nightly-latest-ssl' and 'os=win' and 'lang=de' in page.download_link


@pytest.mark.nondestructive
def test_firefox_esr(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product('Firefox Extended Support Release')
    product.select_platform('Linux 32-bit')
    product.select_language('English (US)')
    assert page.is_download_button_displayed
    assert page.is_download_link_valid
    assert 'product=firefox-esr-latest-ssl' and 'os=linux' and 'lang=en-US' in page.download_link


@pytest.mark.nondestructive
def test_firefox_android(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product('Firefox Android')
    product.select_platform('Intel devices (Android 4.1+ x86 CPU)')
    assert page.is_download_button_displayed
    assert page.is_download_link_valid
    assert 'product=fennec-latest' and 'os=android-x86' and 'lang=multi' in page.download_link


@pytest.mark.nondestructive
def test_firefox_android_beta(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product('Firefox Android')
    product.select_platform('ARM devices (Android 4.1+)')
    assert page.is_download_button_displayed
    assert page.is_download_link_valid
    assert 'product=fennec-beta-latest' and 'os=android' and 'lang=multi' in page.download_link


@pytest.mark.nondestructive
def test_firefox_android_nightly(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url).open()
    product = page.select_product('Firefox Android Nightly')
    product.select_platform('Intel devices (Android 4.1+ x86 CPU)')
    assert page.is_download_button_displayed
    assert page.is_download_link_valid
    assert 'product=fennec-nightly-latest' and 'os=android' and 'lang=multi' in page.download_link
