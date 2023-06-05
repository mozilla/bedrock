# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest import mock

from django.test import override_settings

import pytest
import requests
from freezegun import freeze_time

from bedrock.utils.braze import BrazeClient


@pytest.fixture
def braze_client():
    client = BrazeClient(
        api_url_base="https://example.com/api",
        api_key="abcd1234",
    )
    return client


def test_BrazeClient__init__(braze_client):
    # Test the client made in the fixture is configured as we expect
    assert braze_client.track_user_api_url == "https://example.com/api/users/track"
    assert braze_client.api_key == "abcd1234"


def test_braze_subscribe__newsletter_id_check(braze_client):
    with pytest.raises(RuntimeError):
        braze_client.subscribe("test@example.com", "non-existent-newsletter-id")


@freeze_time("2023-01-02 12:34:56.123456")
@override_settings(BRAZE_API_NEWSLETTERS={"news": "99887766test"})
@mock.patch("bedrock.utils.braze.requests.post")
def test_braze_subscribe__external_id_present(mock_requests_post, braze_client):
    braze_client.subscribe("test@example.com", "news", external_id="test1234")
    mock_requests_post.assert_called_once_with(
        "https://example.com/api/users/track",
        json={
            "attributes": [
                {
                    "email": "test@example.com",
                    "email_subscribe": "subscribed",
                    "subscription_groups": [
                        {
                            "subscription_group_id": "99887766test",
                            "subscription_state": "subscribed",
                        }
                    ],
                    "external_id": "test1234",
                }
            ],
            "events": [
                {
                    "name": "newsletter_signup",
                    "time": "2023-01-02T12:34:56.123456Z",
                    "external_id": "test1234",
                    "properties": {
                        "newsletter": "99887766test",
                        "subscriber_form_type": "website",
                    },
                }
            ],
        },
        headers={"Authorization": "Bearer abcd1234"},
    )


@freeze_time("2023-01-02 12:34:56.123456")
@override_settings(BRAZE_API_NEWSLETTERS={"news": "99887766test"})
@mock.patch("bedrock.utils.braze.requests.post")
def test_braze_subscribe__no_external_id(mock_requests_post, braze_client):
    braze_client.subscribe("test@example.com", "news", external_id=None)
    mock_requests_post.assert_called_once_with(
        "https://example.com/api/users/track",
        json={
            "attributes": [
                {
                    "email": "test@example.com",
                    "email_subscribe": "subscribed",
                    "subscription_groups": [
                        {
                            "subscription_group_id": "99887766test",
                            "subscription_state": "subscribed",
                        }
                    ],
                    "user_alias": {
                        "alias_name": "test@example.com",
                        "alias_label": "email",
                    },
                    "_update_existing_only": False,
                }
            ],
            "events": [
                {
                    "name": "newsletter_signup",
                    "time": "2023-01-02T12:34:56.123456Z",
                    "user_alias": {
                        "alias_name": "test@example.com",
                        "alias_label": "email",
                    },
                    "properties": {
                        "newsletter": "99887766test",
                        "subscriber_form_type": "website",
                    },
                }
            ],
        },
        headers={"Authorization": "Bearer abcd1234"},
    )


@freeze_time("2023-01-02 12:34:56.123456")
@override_settings(BRAZE_API_NEWSLETTERS={"news": "99887766test"})
@mock.patch("bedrock.utils.braze.requests.post")
def test_braze_subscribe__allowed_params_processing(mock_requests_post, braze_client):
    extra_params = {
        # These will all be prefixed with subscriber_
        "campaign": "test",
        "medium": "unit-tests",
        "source": "testland",
        "language": "en-GB",
        "country": "GB",
        "form_source": "word-of-mouth",
        # This field will be ignored because it's not in ALLOWED_PARAMS
        "evil_field": "noise that should be ignored",
    }

    braze_client.subscribe("test@example.com", "news", external_id=None, **extra_params)
    mock_requests_post.assert_called_once_with(
        "https://example.com/api/users/track",
        json={
            "attributes": [
                {
                    "email": "test@example.com",
                    "email_subscribe": "subscribed",
                    "subscription_groups": [
                        {
                            "subscription_group_id": "99887766test",
                            "subscription_state": "subscribed",
                        }
                    ],
                    "user_alias": {
                        "alias_name": "test@example.com",
                        "alias_label": "email",
                    },
                    "_update_existing_only": False,
                }
            ],
            "events": [
                {
                    "name": "newsletter_signup",
                    "time": "2023-01-02T12:34:56.123456Z",
                    "user_alias": {
                        "alias_name": "test@example.com",
                        "alias_label": "email",
                    },
                    "properties": {
                        "newsletter": "99887766test",
                        "subscriber_form_type": "website",
                        "subscriber_campaign": "test",
                        "subscriber_medium": "unit-tests",
                        "subscriber_source": "testland",
                        "subscriber_language": "en-GB",
                        "subscriber_country": "GB",
                        "subscriber_form_source": "word-of-mouth",
                    },
                }
            ],
        },
        headers={"Authorization": "Bearer abcd1234"},
    )


@mock.patch("bedrock.utils.braze.requests.post")
def test_braze_subscribe__fake_braze_error(mock_requests_post, braze_client):
    server_error_response = requests.Response()
    server_error_response.status_code = 500
    mock_requests_post.return_value = server_error_response
    with pytest.raises(requests.RequestException):
        braze_client.subscribe("test@example.com", "news", external_id="test1234")
