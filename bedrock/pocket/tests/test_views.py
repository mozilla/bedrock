# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from http import HTTPStatus
from unittest import mock

from django.test import override_settings
from django.urls import reverse


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
    assert mock_braze_subscribe.call_count == 1
