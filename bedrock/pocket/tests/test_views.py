# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from http import HTTPStatus
from http.cookies import SimpleCookie
from unittest import mock

from django.conf import settings
from django.test import override_settings
from django.urls import reverse

import pytest


@override_settings(ROOT_URLCONF="bedrock.urls.pocket_mode")
@mock.patch("bedrock.pocket.views.braze_client.subscribe")
def test_newsletter_subscribe_access__denied_for_get(mock_braze_subscribe, client):
    dest = reverse("pocket.newsletter-subscribe")
    resp = client.get(dest, follow=True)
    assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert mock_braze_subscribe.call_count == 0


@override_settings(ROOT_URLCONF="bedrock.urls.pocket_mode")
@mock.patch("bedrock.pocket.views.braze_client.subscribe")
def test_newsletter_subscribe_access__allowed_for_post(mock_braze_subscribe, client):
    dest = reverse("pocket.newsletter-subscribe")
    resp = client.post(
        dest,
        data=json.dumps({"email": "test@example.com", "newsletter": "news"}),  # Smallest amount of acceptable data
        content_type="application/json",
    )
    assert resp.status_code == HTTPStatus.OK
    assert json.loads(resp.content) == {"status": "success"}
    assert mock_braze_subscribe.call_count == 1


@override_settings(ROOT_URLCONF="bedrock.urls.pocket_mode")
@mock.patch("bedrock.pocket.views.braze_client.subscribe")
def test_newsletter_subscribe__happiest_path(mock_braze_subscribe, client):
    "Test a Braze submission with all possible data available"
    dest = reverse("pocket.newsletter-subscribe")
    client.cookies = SimpleCookie(
        {
            settings.BRAZE_POCKET_COOKIE_NAME: "test-external-id-123",
        }
    )
    resp = client.post(
        dest,
        data=json.dumps(
            {
                "email": "test@example.com",
                "newsletter": "news",
                "campaign": "test",
                "medium": "unit-tests",
                "source": "testland",
                "language": "en-GB",
                "country": "GB",
                "form_source": "word-of-mouth",
            }
        ),
        content_type="application/json",
    )
    assert resp.status_code == HTTPStatus.OK
    assert json.loads(resp.content) == {"status": "success"}
    assert mock_braze_subscribe.call_count == 1
    mock_braze_subscribe.assert_called_once_with(
        "test@example.com",
        "news",
        external_id="test-external-id-123",
        campaign="test",
        medium="unit-tests",
        source="testland",
        language="en-GB",
        country="GB",
        form_source="word-of-mouth",
    )


@override_settings(ROOT_URLCONF="bedrock.urls.pocket_mode")
@mock.patch("bedrock.pocket.views.braze_client.subscribe")
def test_newsletter_subscribe__happyish_path(mock_braze_subscribe, client):
    "Test a Braze submission with all minimal but sufficient data"
    dest = reverse("pocket.newsletter-subscribe")
    # NB: no cookie this time
    resp = client.post(
        dest,
        data=json.dumps(
            {
                "email": "test@example.com",
                "newsletter": "news",
            }
        ),
        content_type="application/json",
    )
    assert resp.status_code == HTTPStatus.OK
    assert json.loads(resp.content) == {"status": "success"}
    assert mock_braze_subscribe.call_count == 1
    mock_braze_subscribe.assert_called_once_with(
        "test@example.com",
        "news",
        external_id=None,  # NB: None is explicitly set if the cookie is not present (vs '')
    )


@override_settings(ROOT_URLCONF="bedrock.urls.pocket_mode")
def test_newsletter_subscribe__bad_data(client):
    dest = reverse("pocket.newsletter-subscribe")

    # Send non-JSON, to blow up json.loads()
    resp = client.post(
        dest,
        data={
            "email": "test@example.com",
            "newsletter": "news",
        },
    )
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert json.loads(resp.content) == {
        "status": "error",
        "detail": "Error parsing JSON data",
    }


@pytest.mark.parametrize(
    "bad_payload",
    (
        {
            "email": "not_an_email_address",
            "newsletter": "news",
        },
        {
            "email": "test@example.com",
            "newsletter": "never-going-to-be-a-real-newsletter-choice",
        },
        {
            "email": "test@example.com",
        },
        {
            "newsletter": "never-going-to-be-a-real-newsletter",
        },
    ),
    ids=[
        "bad email, valid newsletter",
        "valid email, invalid newsletter",
        "missing email",
        "missing newsletter",
    ],
)
@override_settings(ROOT_URLCONF="bedrock.urls.pocket_mode")
def test_newsletter_subscribe__invalid_form_data(bad_payload, client):
    dest = reverse("pocket.newsletter-subscribe")

    resp = client.post(
        dest,
        data=json.dumps(bad_payload),
        content_type="application/json",
    )
    assert resp.status_code == HTTPStatus.BAD_REQUEST

    response_data = json.loads(resp.content)
    assert response_data["status"] == "error"


@override_settings(ROOT_URLCONF="bedrock.urls.pocket_mode")
@mock.patch("bedrock.pocket.views.braze_client.subscribe")
def test_newsletter_subscribe__braze_error(mock_braze_subscribe, client):
    dest = reverse("pocket.newsletter-subscribe")

    mock_braze_subscribe.side_effect = Exception("Deliberately failing")

    resp = client.post(
        dest,
        data=json.dumps({"email": "test@example.com", "newsletter": "news"}),
        content_type="application/json",
    )
    assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert json.loads(resp.content) == {
        "status": "error",
        "detail": "Error contacting subscription provider",
    }
