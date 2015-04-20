# flake8: noqa

import os

try:
    import newrelic.agent
except ImportError:
    newrelic = False


if newrelic:
    newrelic_ini = os.getenv('NEWRELIC_PYTHON_INI_FILE', False)
    if newrelic_ini:
        newrelic.agent.initialize(newrelic_ini)
    else:
        newrelic = False

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bedrock.settings')

# must be imported after env var is set above.
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)

if newrelic:
    application = newrelic.agent.wsgi_application()(application)
