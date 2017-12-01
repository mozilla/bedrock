#!/bin/bash
set -ex

python manage.py update_product_details_files
python manage.py update_security_advisories --quiet
python manage.py update_wordpress --quiet
python manage.py update_release_notes --quiet
python manage.py update_externalfiles --quiet

if [[ "$1" == "--all" ]]; then
    # less frequent. these will modify the DB every time.
    # TODO fix this
    python manage.py cron update_tweets
    python manage.py cron update_ical_feeds
fi
