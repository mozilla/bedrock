#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# We deliberately don't set -e here because we don't want a failure to block subsequent tasks
set -x

# run all jobs
ALL=false
# run jobs that require secrets
AUTH=false

# parse cli args
while [[ $# -ge 1 ]]; do
    key="$1"
    case $key in
        --all)
            ALL=true
            ;;
        --auth)
            AUTH=true
            ;;
    esac
    shift # past argument or value
done

failure_detected=false

# Please ensure all new command calls are suffixed with || failure_detected=true

python manage.py update_product_details_files || failure_detected=true
python manage.py update_security_advisories --quiet || failure_detected=true
python manage.py update_wordpress --quiet || failure_detected=true
python manage.py update_release_notes --quiet || failure_detected=true
python manage.py update_content_cards --quiet || failure_detected=true
python manage.py update_contentful --quiet || failure_detected=true
python manage.py update_externalfiles --quiet || failure_detected=true
python manage.py update_newsletter_data --quiet || failure_detected=true
python manage.py update_www_config --quiet || failure_detected=true
python manage.py update_legal_docs --quiet || failure_detected=true
python manage.py update_webvision_docs --quiet || failure_detected=true
python manage.py update_sitemaps_data --quiet || failure_detected=true
python manage.py sync_greenhouse --quiet || failure_detected=true

if [[ "$AUTH" == true ]]; then
    # jobs that require some auth. don't run these during build.
    python manage.py update_pocketfeed --quiet || failure_detected=true
fi

# If all is well, ping DMS to avoid an alert being raised.
if [[ $failure_detected == false ]]; then
    echo "No failures detected across all update scripts"
    if [[ -n "${DB_UPDATE_SCRIPT_DMS_URL}" ]]; then
        curl "${DB_UPDATE_SCRIPT_DMS_URL}"
        echo "Pinged snitch"
    fi
else
    echo "WARNING: Failure detected during update scripts - snitch not pinged"
fi
