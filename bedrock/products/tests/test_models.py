# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from unittest import mock

from django.utils.dateparse import parse_date, parse_datetime

import pytest

from bedrock.products.models import Breach


def _update(**kwargs):
    Breach.objects.filter(name="Twitter").update(**kwargs)


def test_is_delayed(breach):
    assert breach.is_delayed is True


def test_is_not_delayed(breach):
    _update(breach_date=parse_date("2022-07-01"))
    breach = Breach.objects.get(name="Twitter")
    assert breach.is_delayed is False


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        (None, "website-breach"),
        ({"name": "Apollo"}, "data-aggregator-breach"),
        ({"is_sensitive": True}, "sensitive-breach"),
        ({"domain": ""}, "data-aggregator-breach"),
    ],
)
def test_category(breach, kwargs, expected):
    if kwargs:
        _update(**kwargs)
    breach = Breach.objects.get()
    assert breach.category == expected


BREACH_JSON = {
    "Name": "Twitter",
    "Title": "Twitter",
    "Domain": "twitter.com",
    "BreachDate": "2022-01-01",
    "AddedDate": "2022-08-01T01:23:45Z",
    "ModifiedDate": "2022-08-01T01:23:45Z",
    "PwnCount": 6682453,
    "Description": "Example description. We don't use this field.",
    "LogoPath": "/path/to/twitter.com.ico",
    "DataClasses": ["Bios", "Email addresses", "Geographic locations", "Names", "Phone numbers", "Profile photos", "Usernames"],
    "IsVerified": True,
    "IsFabricated": False,
    "IsSensitive": False,
    "IsRetired": False,
    "IsSpamList": False,
    "IsMalware": False,
    "IsSubscriptionFree": False,  # We don't use this field.
}


@mock.patch("bedrock.products.models.requests.get")
def test_sync_db(mock_requests, db):
    mock_requests.return_value.json.return_value = [BREACH_JSON]
    added, updated = Breach.objects.sync_db()
    assert added == 1
    assert updated == 0
    assert Breach.objects.count() == 1
    breach = Breach.objects.get()
    assert breach.name == "Twitter"
    assert breach.title == "Twitter"
    assert breach.domain == "twitter.com"
    assert breach.breach_date == parse_date("2022-01-01")
    assert breach.added_date == parse_datetime("2022-08-01T01:23:45Z")
    assert breach.modified_date == parse_datetime("2022-08-01T01:23:45Z")
    assert breach.pwn_count == 6682453
    assert breach.logo_path == ""
    assert breach.data_classes == ["Bios", "Email addresses", "Geographic locations", "Names", "Phone numbers", "Profile photos", "Usernames"]
    assert breach.is_verified is True
    assert breach.is_fabricated is False
    assert breach.is_sensitive is False
    assert breach.is_retired is False
    assert breach.is_spam_list is False
    assert breach.is_malware is False


@mock.patch("bedrock.products.models.requests.get")
def test_sync_db__update(mock_requests, breach, db):
    BREACH_JSON["PwnCount"] = 9999999
    mock_requests.return_value.json.return_value = [BREACH_JSON]
    added, updated = Breach.objects.sync_db()
    assert added == 0
    assert updated == 1
    assert Breach.objects.count() == 1
