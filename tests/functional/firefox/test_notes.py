# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.accounts import FirefoxNotesPage


@pytest.mark.nondestructive
def test_firefox_desktop_release_page(base_url, selenium):
    #firefox/65.0/releasenotes/
    page = FirefoxNotesPage(selenium, base_url).open()
    assert page.version is '65.0'
    assert page.channel is 'Firefox Release'
    assert page.gtm_id is '/firefox/releasenotes/'
    assert page.download_button_text is 'Download Firefox'
    assert page.download_button_link.contains('firefox-stub')
    assert page.logo is '/media/img/logos/firefox/logo-quantum-wordmark-large.png'
    assert page.download_all_url.contains('/firefox/all/')

@pytest.mark.nondestructive
def test_firefox_desktop_esr_page(base_url, selenium):
    #/firefox/60.5.2/releasenotes/
    page = FirefoxNotesPage(selenium, base_url).open()
    assert page.version is '60.5.2'
    assert page.channel is 'Firefox ESR'
    assert page.gtm_id is '/firefox/esr/releasenotes/'
    assert page.download_button_text is 'Download Firefox'
    assert page.download_button_link.contains('firefox-stub')
    assert page.logo is '/media/img/logos/firefox/logo-quantum-wordmark-large.png'
    assert page.download_all_url.contains('/firefox/all/')

@pytest.mark.nondestructive
def test_firefox_desktop_beta_page(base_url, selenium):
    #/firefox/65.0beta/releasenotes/
    page = FirefoxNotesPage(selenium, base_url).open()
    assert page.version is '65.0beta'
    assert page.channel is 'Firefox Beta'
    assert page.gtm_id is '/firefox/beta/releasenotes/'
    assert page.download_button_text is 'Download Firefox Beta'
    assert page.download_button_link.contains('firefox-beta-stub')
    assert page.logo is '/media/img/logos/firefox/logo-quantum-wordmark-large.png'
    assert page.download_all_url.contains('/firefox/beta/all/')

@pytest.mark.nondestructive
def test_firefox_desktop_developer_page(base_url, selenium):
    #/firefox/54.0a2/auroranotes/
    page = FirefoxNotesPage(selenium, base_url).open()
    assert page.version is '54.0a2'
    assert page.channel is 'Firefox Developer Edition'
    assert page.gtm_id is '/firefox/auroranotes/'
    assert page.download_button_text is 'Download Firefox Developer Edition'
    assert page.download_button_link.contains('firefox-devedition-stub')
    assert page.logo is '/media/img/firefox/developer/title-inverse.png'
    assert page.download_all_url.contains('/firefox/developer/all/')

@pytest.mark.nondestructive
def test_firefox_desktop_aurora_page(base_url, selenium):
    #/firefox/32.0a2/auroranotes/
    page = FirefoxNotesPage(selenium, base_url).open()
    assert page.version is '32.0a2'
    assert page.channel is 'Firefox Aurora'
    assert page.gtm_id is '/firefox/auroranotes/'
    assert page.download_button_text is 'Download Firefox Developer Edition'
    assert page.download_button_link.contains('firefox-devedition-stub')
    assert page.logo is '/media/img/firefox/template/header-logo.png'
    assert page.download_all_url.contains('/firefox/developer/all/')

@pytest.mark.nondestructive
def test_firefox_desktop_nightly_page(base_url, selenium):
    #/firefox/65.0a1/releasenotes/
    page = FirefoxNotesPage(selenium, base_url).open()
    assert page.version is '65.0a1'
    assert page.channel is 'Firefox Nightly'
    assert page.gtm_id is '/firefox/releasenotes/'
    assert page.download_button_text is 'Download Firefox Nightly'
    assert page.download_button_link.contains('firefox-nightly-stub')
    assert page.logo is '/media/img/firefox/template/header-logo-nightly.png'
    assert page.download_all_url.contains('/firefox/nightly/all/')

@pytest.mark.nondestructive
def test_firefox_android_release_page(base_url, selenium):
    #/firefox/android/65.0/releasenotes/
    page = FirefoxNotesPage(selenium, base_url).open()
    assert page.version is '65.0'
    assert page.channel is 'Firefox for Android'
    assert page.gtm_id is '/firefox/android/releasenotes/'
    !! play store link https://play.google.com/store/apps/details?id=org.mozilla.firefox
    assert page.logo is '/media/img/logos/firefox/logo-quantum-wordmark-large.png'
    assert page.download_all_url.contains('/firefox/android/all/')

@pytest.mark.nondestructive
def test_firefox_android_beta_page(base_url, selenium):
    #/firefox/android/65.0beta/releasenotes/
    page = FirefoxNotesPage(selenium, base_url).open()
    assert page.version is '65.0beta'
    assert page.channel is 'Firefox for Android Beta'
    assert page.gtm_id is '/firefox/android/beta/releasenotes/'
    !! play store link on green button https://play.google.com/store/apps/details?id=org.mozilla.firefox_beta
    assert page.logo is '/media/img/logos/firefox/logo-quantum-wordmark-large.png'
    assert page.download_all_url.contains('/firefox/android/beta/all/')

@pytest.mark.nondestructive
def test_firefox_ios_release_page(base_url, selenium):
    #/firefox/ios/15.0/releasenotes/
    page = FirefoxNotesPage(selenium, base_url).open()
    assert page.version is '15.0'
    assert page.channel is 'Firefox for iOS'
    assert page.gtm_id is '/firefox/ios/releasenotes/'
    !! no li, app store button !! https://itunes.apple.com/us/app/apple-store/id989804926?pt=373246&mt=8&ct=mozorg-releasenotes_page-appstore-button
    assert page.logo is '/media/img/logos/firefox/logo-quantum-wordmark-large.png'
    !! no all link
