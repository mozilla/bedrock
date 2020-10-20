# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base import BasePage
from pages.regions.download_button import DownloadButton


class FirefoxReleaseNotesPage(BasePage):

    _URL_TEMPLATE = '/{locale}/firefox/{slug}/releasenotes/'

    _primary_download_button_release_locator = (By.ID, 'download-release-primary')
    _secondary_download_button_release_locator = (By.ID, 'download-release-secondary')
    _primary_download_button_beta_locator = (By.ID, 'download-beta-primary')
    _secondary_download_button_beta_locator = (By.ID, 'download-beta-secondary')
    _primary_download_button_aurora_locator = (By.ID, 'download-dev-edition-primary')
    _secondary_download_button_aurora_locator = (By.ID, 'download-dev-edition-secondary')
    _primary_download_button_dev_edition_locator = (By.ID, 'download-dev-edition-primary')
    _secondary_download_button_dev_edition_locator = (By.ID, 'download-dev-edition-secondary')
    _primary_download_button_nightly_locator = (By.ID, 'download-nightly-primary')
    _secondary_download_button_nightly_locator = (By.ID, 'download-nightly-secondary')
    _primary_download_button_esr_locator = (By.ID, 'download-esr-primary')
    _secondary_download_button_esr_locator = (By.ID, 'download-esr-secondary')
    _primary_download_button_android_beta_locator = (By.ID, 'download-android-beta-primary')
    _secondary_download_button_android_beta_locator = (By.ID, 'download-android-beta-secondary')
    _primary_download_button_android_nightly_locator = (By.ID, 'download-android-nightly-primary')
    _secondary_download_button_android_nightly_locator = (By.ID, 'download-android-nightly-secondary')
    _primary_play_store_button_locator = (By.ID, 'download-android-primary')
    _secondary_play_store_button_locator = (By.ID, 'download-android-secondary')
    _primary_app_store_button_locator = (By.ID, 'download-ios-primary')
    _secondary_app_store_button_locator = (By.ID, 'download-ios-secondary')

    @property
    def primary_download_button_release(self):
        el = self.find_element(*self._primary_download_button_release_locator)
        return DownloadButton(self, root=el)

    @property
    def secondary_download_button_release(self):
        el = self.find_element(*self._secondary_download_button_release_locator)
        return DownloadButton(self, root=el)

    @property
    def primary_download_button_beta(self):
        el = self.find_element(*self._primary_download_button_beta_locator)
        return DownloadButton(self, root=el)

    @property
    def secondary_download_button_beta(self):
        el = self.find_element(*self._secondary_download_button_beta_locator)
        return DownloadButton(self, root=el)

    @property
    def primary_download_button_aurora(self):
        el = self.find_element(*self._primary_download_button_aurora_locator)
        return DownloadButton(self, root=el)

    @property
    def secondary_download_button_aurora(self):
        el = self.find_element(*self._secondary_download_button_aurora_locator)
        return DownloadButton(self, root=el)

    @property
    def primary_download_button_dev_edition(self):
        el = self.find_element(*self._primary_download_button_dev_edition_locator)
        return DownloadButton(self, root=el)

    @property
    def secondary_download_button_dev_edition(self):
        el = self.find_element(*self._secondary_download_button_dev_edition_locator)
        return DownloadButton(self, root=el)

    @property
    def primary_download_button_nightly(self):
        el = self.find_element(*self._primary_download_button_nightly_locator)
        return DownloadButton(self, root=el)

    @property
    def secondary_download_button_nightly(self):
        el = self.find_element(*self._secondary_download_button_nightly_locator)
        return DownloadButton(self, root=el)

    @property
    def primary_download_button_esr(self):
        el = self.find_element(*self._primary_download_button_esr_locator)
        return DownloadButton(self, root=el)

    @property
    def secondary_download_button_esr(self):
        el = self.find_element(*self._secondary_download_button_esr_locator)
        return DownloadButton(self, root=el)

    @property
    def primary_download_button_android_beta(self):
        el = self.find_element(*self._primary_download_button_android_beta_locator)
        return DownloadButton(self, root=el)

    @property
    def secondary_download_button_android_beta(self):
        el = self.find_element(*self._secondary_download_button_android_beta_locator)
        return DownloadButton(self, root=el)

    @property
    def primary_download_button_android_nightly(self):
        el = self.find_element(*self._primary_download_button_android_nightly_locator)
        return DownloadButton(self, root=el)

    @property
    def secondary_download_button_android_nightly(self):
        el = self.find_element(*self._secondary_download_button_android_nightly_locator)
        return DownloadButton(self, root=el)

    @property
    def is_primary_play_store_button_displayed(self):
        return self.is_element_displayed(*self._primary_play_store_button_locator)

    @property
    def is_secondary_play_store_button_displayed(self):
        return self.is_element_displayed(*self._secondary_play_store_button_locator)

    @property
    def is_primary_app_store_button_displayed(self):
        return self.is_element_displayed(*self._primary_app_store_button_locator)

    @property
    def is_secondary_app_store_button_displayed(self):
        return self.is_element_displayed(*self._secondary_app_store_button_locator)

    @property
    def is_pre_releases_menu_displayed(self):
        return self.is_element_displayed(*self._pre_releases_menu_locator)
