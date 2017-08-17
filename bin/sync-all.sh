#!/bin/bash
set -ex
if [ ! -e ./manage.py ]; then
    # this does not support symlinks
    script_parent_dir=${0%/*}/..
    cd $script_parent_dir
fi
./manage.py migrate --noinput --database bedrock
./manage.py cron update_ical_feeds
./manage.py update_product_details_files --database bedrock
./manage.py update_wordpress --database bedrock
./manage.py update_externalfiles
./manage.py update_security_advisories
./manage.py l10n_update
./manage.py update_release_notes
./manage.py update_sitemaps
#requires twitter api credentials not distributed publicly
./manage.py cron update_tweets
