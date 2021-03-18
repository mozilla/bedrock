#!/bin/bash -xe

export prometheus_multiproc_dir=/tmp/prometheus_metrics
# ensure the multiproc dir is empty
rm -rf "$prometheus_multiproc_dir" && mkdir -p "$prometheus_multiproc_dir"

function run-gunicorn () {
    if [[ -z "$NEW_RELIC_LICENSE_KEY" ]]; then
        exec gunicorn "$@"
    else
        export NEW_RELIC_CONFIG_FILE=newrelic.ini
        exec newrelic-admin run-program gunicorn "$@"
    fi
}

# look for the required files and fail quickly if it's not there
STARTUP_FILES=(
    "data/bedrock.db"
    "data/last-run-update_locales"
    "data/last-run-download_database"
)
for fname in "${STARTUP_FILES[@]}"; do
    if [[ ! -f "$fname" ]]; then
        echo "$fname not found";
        exit 1
    fi
done

run-gunicorn wsgi.app:application --config wsgi/config.py
