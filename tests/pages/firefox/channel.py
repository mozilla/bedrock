# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage, FirefoxBaseRegion
from pages.regions.download_button import DownloadButton


class ChannelPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/channel/{hash}'

    _desktop_release_download_locator = (By.ID, 'download-button-desktop-release')
    _android_release_download_locator = (By.ID, 'download-button-android-release')
    _desktop_beta_download_locator = (By.ID, 'download-button-desktop-beta')
    _android_beta_download_locator = (By.ID, 'download-button-android-beta')
    _desktop_developer_download_locator = (By.ID, 'download-button-desktop-alpha')
    _android_aurora_download_locator = (By.ID, 'download-button-android-alpha')
    _right_carousel_button_locator = (By.ID, 'carousel-right')
    _left_carousel_button_locator = (By.ID, 'carousel-left')
    _channels_locator = (By.CLASS_NAME, 'pager-page')

    @property
    def _channels(self):
        return [Channel(self, root=el) for el in
                self.find_elements(*self._channels_locator)]

    @property
    def desktop_release_download_button(self):
        el = self.find_element(*self._desktop_release_download_locator)
        return DownloadButton(self, root=el)

    @property
    def android_release_download_button(self):
        el = self.find_element(*self._android_release_download_locator)
        return DownloadButton(self, root=el)

    @property
    def desktop_beta_download_button(self):
        el = self.find_element(*self._desktop_beta_download_locator)
        return DownloadButton(self, root=el)

    @property
    def android_beta_download_button(self):
        el = self.find_element(*self._android_beta_download_locator)
        return DownloadButton(self, root=el)

    @property
    def desktop_developer_download_button(self):
        el = self.find_element(*self._desktop_developer_download_locator)
        return DownloadButton(self, root=el)

    @property
    def android_aurora_download_button(self):
        el = self.find_element(*self._android_aurora_download_locator)
        return DownloadButton(self, root=el)

    def click_next(self):
        channel = next(c for c in self._channels if c.is_selected)
        self.find_element(*self._right_carousel_button_locator).click()
        self.wait.until(lambda s: not channel.is_selected)

    def click_previous(self):
        channel = next(c for c in self._channels if c.is_selected)
        self.find_element(*self._left_carousel_button_locator).click()
        self.wait.until(lambda s: not channel.is_selected)


class Channel(FirefoxBaseRegion):

    @property
    def is_selected(self):
        return (self.root.get_attribute('aria-hidden') == 'false' and
                self.root.is_displayed())
