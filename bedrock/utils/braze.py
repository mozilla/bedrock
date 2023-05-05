# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from datetime import datetime

from django.conf import settings

import requests


class BrazeClient:
    ALLOWED_PARAMS = ["campaign", "medium", "source", "language", "country", "form_source"]

    def __init__(self, api_url_base, api_key) -> None:
        self.api_key = api_key
        self.track_user_api_url = f"{api_url_base}/users/track"

    def subscribe(self, email, newsletter_id="news", external_id=None, **kwargs):
        if newsletter_id not in settings.BRAZE_API_NEWSLETTERS:
            raise RuntimeError("Invalid Newsletter ID")

        newsletter_braze_id = settings.BRAZE_API_NEWSLETTERS[newsletter_id]
        attributes = {
            "email": email,
            "email_subscribe": "subscribed",
            "subscription_groups": [
                {
                    "subscription_group_id": newsletter_braze_id,
                    "subscription_state": "subscribed",
                }
            ],
        }
        if external_id:
            attributes["external_id"] = external_id
        else:
            attributes["user_alias"] = {
                "alias_name": email,
                "alias_label": "email",
            }
            attributes["_update_existing_only"] = False

        event = {
            "name": "newsletter_signup",
            "time": f"{datetime.utcnow().isoformat()}Z",
            "newsletter": newsletter_braze_id,
            "subscriber_form_type": "website",
        }
        if external_id:
            event["external_id"] = external_id
        else:
            event["user_alias"] = {
                "alias_name": email,
                "alias_label": "email",
            }

        for name, value in kwargs.items():
            if name in self.ALLOWED_PARAMS:
                event[f"subscriber_{name}"] = value

        data = {"attributes": [attributes], "events": [event]}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        resp = requests.post(self.track_user_api_url, json=data, headers=headers)
        resp.raise_for_status()
        return resp.json()


client = BrazeClient(settings.BRAZE_API_URL_BASE, settings.BRAZE_API_KEY)
