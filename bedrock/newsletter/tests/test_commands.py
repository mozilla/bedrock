# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError

import pytest
from basket import BasketException

from bedrock.newsletter.management.commands import update_newsletter_data
from bedrock.newsletter.models import Newsletter

pytestmark = pytest.mark.django_db

NEWSLETTERS = {
    "mozilla-and-you": {"title": "Firefox", "show": True, "active": True},
    "about-mozilla": {"title": "Mozilla Community", "show": True, "active": True},
}


@pytest.fixture
def get_newsletters():
    with patch.object(update_newsletter_data.basket, "get_newsletters", return_value=NEWSLETTERS) as basket_mock:
        yield basket_mock


def test_newsletters_are_loaded(get_newsletters, capsys):
    call_command("update_newsletter_data")

    assert Newsletter.objects.serialize() == NEWSLETTERS
    assert capsys.readouterr().out == "Updated 2 newsletters\n"


def test_unchanged_data_is_left_alone(get_newsletters, capsys):
    call_command("update_newsletter_data")
    capsys.readouterr()

    call_command("update_newsletter_data")

    assert Newsletter.objects.serialize() == NEWSLETTERS
    assert capsys.readouterr().out == "Nothing to update\n"


def test_old_newsletters_are_replaced(get_newsletters):
    Newsletter.objects.create(slug="retired", data={"title": "Retired", "active": False})

    call_command("update_newsletter_data")

    assert Newsletter.objects.serialize() == NEWSLETTERS


@pytest.mark.parametrize("empty_response", [{}, None])
def test_no_data_from_basket_keeps_what_we_have(get_newsletters, empty_response):
    Newsletter.objects.create(slug="mozilla-and-you", data={"title": "Firefox"})
    get_newsletters.return_value = empty_response

    with pytest.raises(CommandError, match="No data from basket"):
        call_command("update_newsletter_data")

    assert Newsletter.objects.serialize() == {"mozilla-and-you": {"title": "Firefox"}}


def test_quiet(get_newsletters, capsys):
    call_command("update_newsletter_data", quiet=True)

    assert Newsletter.objects.count() == 2
    assert capsys.readouterr().out == ""


@patch("bedrock.utils.management.decorators.capture_exception")
def test_error_goes_to_sentry(capture_exception, get_newsletters):
    error = BasketException("basket is down")
    get_newsletters.side_effect = error

    with pytest.raises(BasketException):
        call_command("update_newsletter_data")

    capture_exception.assert_called_once_with(error)
