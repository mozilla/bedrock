# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.firefox.releasenotes import FirefoxReleaseNotesPage


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_primary_download_button_release_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='75.0').open()
    assert page.primary_download_button_release.is_displayed


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_primary_download_button_beta_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='77.0beta').open()
    assert page.primary_download_button_beta.is_displayed


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_primary_download_button_aurora_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='34.0a2').open()
    assert page.primary_download_button_aurora.is_displayed


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_primary_download_button_dev_edition_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='54.0a2').open()
    assert page.primary_download_button_dev_edition.is_displayed


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_primary_download_button_nightly_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='68.8.0').open()
    assert page.primary_download_button_esr.is_displayed


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_primary_download_button_esr_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='78.0a1').open()
    assert page.primary_download_button_nightly.is_displayed


@pytest.mark.skip_if_firefox(reason='Play Store button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_primary_download_button_android_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='android/68.8.0').open()
    assert page.is_primary_play_store_button_displayed


@pytest.mark.skip_if_firefox(reason='Play Store button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_primary_download_button_android_beta_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='android/68.7beta').open()
    assert page.primary_download_button_android_beta.is_displayed


@pytest.mark.skip_if_firefox(reason='Download button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_primary_download_button_android_nightly_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='android/54.0a2').open()
    assert page.primary_download_button_android_nightly.is_displayed


@pytest.mark.skip_if_firefox(reason='App Store button is displayed only to non-Firefox users')
@pytest.mark.nondestructive
def test_primary_download_button_ios_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='ios/25.0').open()
    assert page.is_primary_app_store_button_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_secondary_download_button_release_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='75.0').open()
    assert page.secondary_download_button_release.is_displayed


@pytest.mark.nondestructive
def test_secondary_download_button_beta_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='77.0beta').open()
    assert page.secondary_download_button_beta.is_displayed


@pytest.mark.nondestructive
def test_secondary_download_button_aurora_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='34.0a2').open()
    assert page.secondary_download_button_aurora.is_displayed


@pytest.mark.nondestructive
def test_secondary_download_button_dev_edition_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='54.0a2').open()
    assert page.secondary_download_button_dev_edition.is_displayed


@pytest.mark.nondestructive
def test_secondary_download_button_nightly_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='78.0a1').open()
    assert page.secondary_download_button_nightly.is_displayed


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_secondary_download_button_esr_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='68.8.0').open()
    assert page.secondary_download_button_esr.is_displayed


@pytest.mark.nondestructive
def test_secondary_download_button_android_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='android/68.8.0').open()
    assert page.is_secondary_play_store_button_displayed


@pytest.mark.nondestructive
def test_secondary_download_button_android_beta_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='android/68.7beta').open()
    assert page.secondary_download_button_android_beta.is_displayed


@pytest.mark.nondestructive
def test_secondary_download_button_android_nightly_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='android/54.0a2').open()
    assert page.secondary_download_button_android_nightly.is_displayed


@pytest.mark.nondestructive
def test_secondary_download_button_ios_displayed(base_url, selenium):
    page = FirefoxReleaseNotesPage(selenium, base_url, slug='ios/25.0').open()
    assert page.is_secondary_app_store_button_displayed
