#!/bin/bash -xe
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program \
gunicorn wsgi.app:application -b 0.0.0.0:${PORT:-8000} \
                              -w ${WEB_CONCURRENCY:-2} \
                              --error-logfile - \
                              --access-logfile - \
                              --log-level ${LOGLEVEL:-info} \
                              --worker-class ${GUNICORN_WORKER_CLASS:-meinheld.gmeinheld.MeinheldWorker}
