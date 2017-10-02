# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.firefox.base import FirefoxBasePage, FirefoxBaseRegion
from pages.regions.modal import Modal


class FirefoxQuantumPage(FirefoxBasePage):

    URL_TEMPLATE = '/{locale}/firefox/quantum/'

    _modal_link_locator = (By.CSS_SELECTOR, '.header-content .sign-up')
    _newsletter_locator = (By.ID, 'newsletter-form')
    _video_carousel_locator = (By.CLASS_NAME, 'feature-carousel-container')

    @property
    def video_carousel(self):
        el = self.find_element(*self._video_carousel_locator)
        return VideoCarousel(self, root=el)

    def open_sign_up_modal(self):
        modal = Modal(self)
        self.find_element(*self._modal_link_locator).click()
        self.wait.until(lambda s: modal.displays(self._newsletter_locator))
        return modal


class VideoCarousel(FirefoxBaseRegion):

    _current_video_locator = (By.CLASS_NAME, 'cycle-slide-active')
    _bookmarking_video_locator = (By.CSS_SELECTOR, '.video-bookmarking.cycle-slide-active')
    _new_tab_video_locator = (By.CSS_SELECTOR, '.video-new-tab.cycle-slide-active')
    _screenshots_video_locator = (By.CSS_SELECTOR, '.video-screenshots.cycle-slide-active')
    _previous_button_locator = (By.CLASS_NAME, 'feature-carousel-previous')
    _next_button_locator = (By.CLASS_NAME, 'feature-carousel-next')

    @property
    def is_bookmarking_video_displayed(self):
        return self.is_element_displayed(*self._bookmarking_video_locator)

    @property
    def is_new_tab_video_displayed(self):
        return self.is_element_displayed(*self._new_tab_video_locator)

    @property
    def is_screenshots_video_displayed(self):
        return self.is_element_displayed(*self._screenshots_video_locator)

    def click_next(self):
        current_video = self.find_element(*self._current_video_locator)
        self.scroll_element_into_view(*self._next_button_locator).click()
        self.wait.until(lambda s: not current_video.is_displayed())

    def click_previous(self):
        current_video = self.find_element(*self._current_video_locator)
        self.scroll_element_into_view(*self._previous_button_locator).click()
        self.wait.until(lambda s: not current_video.is_displayed())
