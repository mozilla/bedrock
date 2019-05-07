# flake8: noqa
# newrelic import & initialization must come first
# https://docs.newrelic.com/docs/agents/python-agent/installation/python-agent-advanced-integration#manual-integration
try:
    import newrelic.agent
except ImportError:
    newrelic = False
else:
    newrelic.agent.initialize('newrelic.ini')


import os

from bedrock.base.config_manager import config


IS_HTTPS = os.environ.get('HTTPS', '').strip() == 'on'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bedrock.settings')

# must be imported after env var is set above.
from django.core.handlers.wsgi import WSGIRequest
from django.core.wsgi import get_wsgi_application

from whitenoise.django import DjangoWhiteNoise
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry


class WSGIHTTPSRequest(WSGIRequest):
    def _get_scheme(self):
        if IS_HTTPS:
            return 'https'

        return super(WSGIHTTPSRequest, self)._get_scheme()

application = get_wsgi_application()
application.request_class = WSGIHTTPSRequest
application = DjangoWhiteNoise(application)
application = Sentry(application)

if newrelic:
    application = newrelic.agent.wsgi_application()(application)
