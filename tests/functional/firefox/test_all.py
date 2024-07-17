# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.all import FirefoxAllPage

# product lists


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_desktop_product_list(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url, slug="").open()
    list_length = page.desktop_product_list_length
    assert list_length == 5


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_mobile_product_list(base_url, selenium):
    page = FirefoxAllPage(selenium, base_url, slug="").open()
    list_length = page.mobile_product_list_length
    assert list_length == 4


RELEASE_PLATFORM_COUNT = [("desktop-release", 9), ("desktop-esr", 8), ("desktop-beta", 9), ("desktop-developer", 8), ("desktop-nightly", 8)]

# platform lists


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("slug, count", RELEASE_PLATFORM_COUNT)
def test_desktop_platform_list(slug, count, base_url, selenium):
    slug = f"{slug}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    list_length = page.platform_list_length
    assert list_length == count


WIN_OS_LANG_PAIRS = [
    # all platforms in english
    ("win64", "en-US"),
    ("win64-msi", "en-US"),
    ("win64-aarch64", "en-US"),
    ("win", "en-US"),
    ("win-msi", "en-US"),
    # all platforms in some other languages
    ("win64", "de"),
    ("win64-msi", "fr"),
    ("win64-aarch64", "hi-IN"),
    ("win", "ja"),
    ("win-msi", "es-ES"),
]

MAC_OS_LANG_PAIRS = [
    # all platforms in english
    ("osx", "en-US"),
    # all platforms in some other languages
    ("osx", "de"),
    ("osx", "fr"),
    ("osx", "hi-IN"),
]

LINUX_OS_LANG_PAIRS = [
    # all platforms in english
    ("linux64", "en-US"),
    ("linux", "en-US"),
    # all platforms in some other languages
    ("linux64", "de"),
    ("linux", "fr"),
    ("linux64", "hi-IN"),
    ("linux", "ja"),
]

LINUX_OS_LANG_PAIRS_NIGHTLY = [
    # all platforms in english
    ("linux64", "en-US"),
    ("linux", "en-US"),
    ("linux64-aarch64", "en-US"),
    # all platforms in some other languages
    ("linux64", "de"),
    ("linux", "fr"),
    ("linux64", "hi-IN"),
    ("linux", "ja"),
    ("linux64-aarch64", "es-ES"),
    ("linux64-aarch64", "pt-BR"),
]

# desktop release


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", WIN_OS_LANG_PAIRS)
def test_firefox_win_release(os, lang, base_url, selenium):
    slug = f"desktop-release/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-latest-ssl" and f"os={os}" and f"lang={lang}" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_microsoft_store_release(base_url, selenium):
    slug = "desktop-release/win-store/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_ms_store_download_button_displayed
    assert "https://apps.microsoft.com/detail/9nzvdkpmr9rd" in page.microsoft_store_link


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", MAC_OS_LANG_PAIRS)
def test_firefox_macos_release(os, lang, base_url, selenium):
    slug = f"desktop-release/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-latest-ssl" and "os={os}" and "lang=en-US" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", LINUX_OS_LANG_PAIRS)
def test_firefox_linux_release(os, lang, base_url, selenium):
    slug = f"desktop-release/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-latest-ssl" and "os={os}" and "lang=en-US" in page.desktop_download_link
    assert page.is_linux_atp_link_displayed
    assert "https://support.mozilla.org/kb/install-firefox-linux" in page.linux_atp_link


# desktop beta - check by platform


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", WIN_OS_LANG_PAIRS)
def test_firefox_win_beta(os, lang, base_url, selenium):
    slug = f"desktop-beta/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-beta-latest" and f"os={os}" and f"lang={lang}" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_microsoft_store_beta(base_url, selenium):
    slug = "desktop-beta/win-store/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_ms_store_download_button_displayed
    assert "https://apps.microsoft.com/detail/9nzw26frndln" in page.microsoft_store_link


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", MAC_OS_LANG_PAIRS)
def test_firefox_macos_beta(os, lang, base_url, selenium):
    slug = f"desktop-beta/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-beta-latest" and f"os={os}" and f"lang={lang}" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", LINUX_OS_LANG_PAIRS)
def test_firefox_linux_beta(os, lang, base_url, selenium):
    slug = f"desktop-beta/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-beta-latest" and f"os={os}" and f"lang={lang}" in page.desktop_download_link
    assert page.is_linux_atp_link_displayed
    assert "https://support.mozilla.org/kb/install-firefox-linux" in page.linux_atp_link


# desktop developer - check by platform


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", WIN_OS_LANG_PAIRS)
def test_firefox_win_developer(os, lang, base_url, selenium):
    slug = f"desktop-developer/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-devedition-latest" and f"os={os}" and f"lang={lang}" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", MAC_OS_LANG_PAIRS)
def test_firefox_macos_developer(os, lang, base_url, selenium):
    slug = f"desktop-developer/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-devedition-latest" and f"os={os}" and f"lang={lang}" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", LINUX_OS_LANG_PAIRS)
def test_firefox_linux_developer(os, lang, base_url, selenium):
    slug = f"desktop-developer/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-devedition-latest" and f"os={os}" and f"lang={lang}" in page.desktop_download_link
    assert page.is_linux_atp_link_displayed
    assert "https://support.mozilla.org/kb/install-firefox-linux" in page.linux_atp_link


# desktop nightly - check by platform


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", WIN_OS_LANG_PAIRS)
def test_firefox_win_nightly(os, lang, base_url, selenium):
    slug = f"desktop-nightly/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-nightly-latest" and f"os={os}" and f"lang={lang}" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", MAC_OS_LANG_PAIRS)
def test_firefox_macos_nightly(os, lang, base_url, selenium):
    slug = f"desktop-nightly/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-nightly-latest" and f"os={os}" and f"lang={lang}" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", LINUX_OS_LANG_PAIRS_NIGHTLY)
def test_firefox_linux_nightly(os, lang, base_url, selenium):
    slug = f"desktop-nightly/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-nightly-latest" and f"os={os}" and f"lang={lang}" in page.desktop_download_link
    assert page.is_linux_atp_link_displayed
    assert "https://support.mozilla.org/kb/install-firefox-linux" in page.linux_atp_link


# desktop esr - check by platform


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", WIN_OS_LANG_PAIRS)
def test_firefox_win_esr(os, lang, base_url, selenium):
    slug = f"desktop-esr/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-esr-latest-ssl" and f"os={os}" and f"lang={lang}" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", MAC_OS_LANG_PAIRS)
def test_firefox_macos_esr(os, lang, base_url, selenium):
    slug = f"desktop-esr/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-esr-latest-ssl" and f"os={os}" and f"lang={lang}" in page.desktop_download_link


@pytest.mark.smoke
@pytest.mark.nondestructive
@pytest.mark.parametrize("os, lang", LINUX_OS_LANG_PAIRS)
def test_firefox_linux_esr(os, lang, base_url, selenium):
    slug = f"desktop-esr/{os}/{lang}/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_desktop_download_button_displayed
    assert "product=firefox-esr-latest-ssl" and f"os={os}" and f"lang={lang}" in page.desktop_download_link
    assert page.is_linux_atp_link_displayed
    assert "https://support.mozilla.org/kb/install-firefox-linux" in page.linux_atp_link


# mobile release - check by platform


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_mobile_release(base_url, selenium):
    slug = "mobile-release/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_android_download_button_displayed
    assert page.is_ios_download_button_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_android_release(base_url, selenium):
    slug = "android-release/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_android_download_button_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_ios_release(base_url, selenium):
    slug = "ios-release/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_ios_download_button_displayed


# mobile beta - check by platform


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_android_beta(base_url, selenium):
    slug = "android-beta/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_android_download_button_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_ios_beta(base_url, selenium):
    slug = "ios-beta/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_ios_download_button_displayed


# mobile nightly - check by platform


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_android_nightly(base_url, selenium):
    slug = "android-nightly/"
    page = FirefoxAllPage(selenium, base_url, slug=slug).open()
    assert page.is_android_download_button_displayed
