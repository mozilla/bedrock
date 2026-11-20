# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import call, patch

from django.core.management import call_command
from django.core.management.base import CommandError

import pytest

from bedrock.wordpress.models import BlogPost


@pytest.fixture(autouse=True)
def wp_blogs(settings):
    settings.WP_BLOGS = {
        "careers": {"url": "https://blog.mozilla.org/careers/", "name": "Life@Mozilla"},
        "firefox": {"url": "https://blog.mozilla.org/firefox/", "name": "The Firefox Frontier"},
    }


@pytest.fixture
def refresh():
    with patch.object(BlogPost.objects, "refresh", return_value=(0, 0)) as refresh_mock:
        yield refresh_mock


def test_every_blog_is_refreshed(refresh):
    call_command("update_wordpress")

    assert refresh.call_args_list == [call("careers"), call("firefox")]


def test_refreshed_and_deleted_posts_are_reported(refresh, capsys):
    refresh.side_effect = [(5, 2), (3, 0)]

    call_command("update_wordpress")

    assert capsys.readouterr().out == (
        "Refreshed 5 posts from the careers blog\nDeleted 2 old posts from the careers blog\nRefreshed 3 posts from the firefox blog\n"
    )


def test_blog_with_nothing_new(refresh, capsys):
    call_command("update_wordpress")

    assert capsys.readouterr().out == "The careers blog is already up to date\nThe firefox blog is already up to date\n"


def test_failed_blog_does_not_stop_the_others(refresh, capsys):
    refresh.side_effect = [(None, None), (3, 0)]

    with pytest.raises(CommandError, match="^There was a problem updating the careers blog$"):
        call_command("update_wordpress")

    assert refresh.call_count == 2
    assert capsys.readouterr().out == "Refreshed 3 posts from the firefox blog\n"


def test_every_failed_blog_is_reported(refresh):
    refresh.return_value = (None, None)

    with pytest.raises(CommandError) as error_info:
        call_command("update_wordpress")

    assert str(error_info.value) == "There was a problem updating the careers blog\nThere was a problem updating the firefox blog"


def test_quiet(refresh, capsys):
    refresh.side_effect = [(5, 2), (None, None)]

    with pytest.raises(CommandError):
        call_command("update_wordpress", quiet=True)

    assert refresh.call_count == 2
    assert capsys.readouterr().out == ""


@patch("bedrock.utils.management.decorators.capture_exception")
def test_error_goes_to_sentry(capture_exception, refresh):
    error = RuntimeError("database is locked")
    refresh.side_effect = error

    with pytest.raises(RuntimeError):
        call_command("update_wordpress")

    capture_exception.assert_called_once_with(error)
