# flake8: noqa
import os

from decouple import config


try:
    import newrelic.agent
except ImportError:
    newrelic = False


if newrelic:
    newrelic_ini = config('NEWRELIC_PYTHON_INI_FILE', default=False)
    if newrelic_ini:
        newrelic.agent.initialize(newrelic_ini)
    else:
        newrelic = False

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bedrock.settings')

# must be imported after env var is set above.
from django.core.wsgi import get_wsgi_application
from bedrock.base.static import BedrockWhiteNoise

application = get_wsgi_application()
application = BedrockWhiteNoise(application)

if newrelic:
    application = newrelic.agent.wsgi_application()(application)
