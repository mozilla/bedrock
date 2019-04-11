# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.contribute.tasks import ContributeSignUpPage


@pytest.mark.nondestructive
def test_contribute_task_twitter(base_url, selenium):
    page = ContributeSignUpPage(selenium, base_url).open()
    twitter_task_page = page.open_twitter_task()
    assert twitter_task_page.seed_url in selenium.current_url
    assert twitter_task_page.is_share_button_displayed
    assert twitter_task_page.is_follow_button_displayed


@pytest.mark.nondestructive
def test_contribute_task_firefox_mobile(base_url, selenium):
    page = ContributeSignUpPage(selenium, base_url).open()
    mobile_task_page = page.open_mobile_task()
    assert mobile_task_page.seed_url in selenium.current_url
    assert mobile_task_page.is_android_download_button_displayed
    assert mobile_task_page.is_ios_download_button_displayed


@pytest.mark.nondestructive
def test_contribute_task_encryption(base_url, selenium):
    page = ContributeSignUpPage(selenium, base_url).open()
    encryption_task_page = page.open_encryption_task()
    assert encryption_task_page.seed_url in selenium.current_url
    assert encryption_task_page.is_take_the_pledge_button_displayed


@pytest.mark.nondestructive
def test_contribute_task_joy_of_coding(base_url, selenium):
    page = ContributeSignUpPage(selenium, base_url).open()
    joy_of_coding_task_page = page.open_joy_of_coding_task()
    assert joy_of_coding_task_page.seed_url in selenium.current_url
    assert joy_of_coding_task_page.is_video_displayed
    assert joy_of_coding_task_page.is_watch_the_video_button_displayed


@pytest.mark.nondestructive
def test_contribute_task_dev_tools_challenger(base_url, selenium):
    page = ContributeSignUpPage(selenium, base_url).open()
    dev_tools_challenger_task_page = page.open_dev_tools_challenger_task()
    assert dev_tools_challenger_task_page.seed_url in selenium.current_url
    assert dev_tools_challenger_task_page.download_button.is_displayed
    assert dev_tools_challenger_task_page.is_visit_dev_tools_challenger_button_displayed


@pytest.mark.nondestructive
def test_contribute_task_stumbler(base_url, selenium):
    page = ContributeSignUpPage(selenium, base_url).open()
    stumbler_task_page = page.open_stumbler_task()
    assert stumbler_task_page.seed_url in selenium.current_url
    assert stumbler_task_page.is_stumbler_button_displayed
