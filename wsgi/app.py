# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# flake8: noqa
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bedrock.settings")

# must be imported after env var is set above.
from django.core.wsgi import get_wsgi_application


django_application = get_wsgi_application()


# This is a hack to force Django to generate https URLs.
def https_application(environ, start_response):
    environ["wsgi.url_scheme"] = "https"
    return django_application(environ, start_response)


application = https_application
