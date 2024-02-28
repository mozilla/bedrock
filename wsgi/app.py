# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bedrock.settings")
django_application = get_wsgi_application()


# Always generate https URLs.
def https_application(environ, start_response):
    environ["wsgi.url_scheme"] = "https"
    return django_application(environ, start_response)


application = https_application
