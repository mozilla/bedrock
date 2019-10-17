from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage


class FirefoxLockwisePage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/lockwise/'

    _ios_download_button_locator = (By.CSS_SELECTOR, '.mobile-buttons-download .ios-button')
    _android_download_button_locator = (By.CSS_SELECTOR, '.mobile-buttons-download .android-button')
    _firefox_add_on_button_locator = (By.CSS_SELECTOR, '.add-on-download.for-firefox-69-and-below')

    @property
    def is_ios_download_button_displayed(self):
        return self.is_element_displayed(*self._ios_download_button_locator)

    @property
    def is_android_download_button_displayed(self):
        return self.is_element_displayed(*self._android_download_button_locator)

    @property
    def is_firefox_add_on_button_displayed(self):
        return self.is_element_displayed(*self._firefox_add_on_button_locator)
