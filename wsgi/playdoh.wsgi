import os
import site

try:
    import newrelic.agent
except ImportError:
    newrelic = False


if newrelic:
    newrelic.agent.initialize(os.environ['NEWRELIC_PYTHON_INI_FILE'])

os.environ['CELERY_LOADER'] = 'django'

# Add the app dir to the python path so we can import manage.
wsgidir = os.path.dirname(__file__)
site.addsitedir(os.path.abspath(os.path.join(wsgidir, '../')))

# manage adds /apps, /lib, and /vendor to the Python path.
import manage

import django.core.handlers.wsgi
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
application = django.core.handlers.wsgi.WSGIHandler()

if newrelic:
    application = newrelic.agent.wsgi_application()(application)
