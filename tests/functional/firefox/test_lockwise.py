import pytest

from pages.firefox.lockwise import FirefoxLockwisePage


@pytest.mark.nondestructive
def test_mobile_button(base_url, selenium):
    page = FirefoxLockwisePage(selenium, base_url).open()
    assert page.is_ios_download_button_displayed
    assert page.is_android_download_button_displayed


@pytest.mark.nondestructive
def test_firefox_add_on_button(base_url, selenium):
    page = FirefoxLockwisePage(selenium, base_url).open()
    assert page.is_firefox_add_on_button_displayed
