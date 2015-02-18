# coding=utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings

import cronjobs
import requests
import logging

from bedrock.events.models import Event

logger = logging.getLogger(__name__)


@cronjobs.register
def update_reps_ical():
    # TODO get dependencies for TLS SNI installed on servers
    # see http://bugzil.la/1080571

    # if the ical feed is down catch the exception, log the error
    # and fail silently.
    # http://bugzil.la/1129961
    try:
        resp = requests.get(settings.REPS_ICAL_FEED, verify=False)
        if resp.status_code == 200:
            Event.objects.sync_with_ical(resp.text)
            return

        logger.error("Request returned error code: %d and error body: %s" %
                     (resp.status_code, resp.text))
    except Exception as e:
        logger.error("Exception caught: %s" % repr(e))
