#!/bin/bash -xe

function run-gunicorn () {
    if [[ -z "$NEW_RELIC_LICENSE_KEY" ]]; then
        gunicorn "$@"
    else
        NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn "$@"
    fi
}

# look for the database and fail quickly if it's not there
if [[ ! -f "data/bedrock.db" ]]; then
    echo "Database file not found";
    exit 1
fi

run-gunicorn wsgi.app:application -b 0.0.0.0:${PORT:-8000} \
                                  -w ${WEB_CONCURRENCY:-2} \
                                  --error-logfile - \
                                  --access-logfile - \
                                  --log-level ${LOGLEVEL:-info} \
                                  --worker-class ${GUNICORN_WORKER_CLASS:-meinheld.gmeinheld.MeinheldWorker}
