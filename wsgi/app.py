# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# flake8: noqa
import os

IS_HTTPS = os.environ.get("HTTPS", "").strip() == "on"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bedrock.settings")

# must be imported after env var is set above.
from django.core.handlers.wsgi import WSGIRequest
from django.core.wsgi import get_wsgi_application


class WSGIHTTPSRequest(WSGIRequest):
    def _get_scheme(self):
        if IS_HTTPS:
            return "https"

        return super()._get_scheme()


application = get_wsgi_application()
application.request_class = WSGIHTTPSRequest
