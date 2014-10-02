# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings

import cronjobs
import requests

from bedrock.events.models import Event


@cronjobs.register
def update_reps_ical():
    resp = requests.get(settings.REPS_ICAL_FEED)
    Event.objects.sync_with_ical(resp.text)
