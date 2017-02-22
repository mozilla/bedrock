#!/bin/bash
set -ex
if [ ! -e ./manage.py ]; then
    # this does not support symlinks
    script_parent_dir=${0%/*}/..
    cd $script_parent_dir
fi
./manage.py migrate --noinput --database bedrock
./manage.py rnasync
./manage.py cron update_ical_feeds
./manage.py update_product_details_files --database bedrock
./manage.py update_blog_feeds --database bedrock
./manage.py update_externalfiles
./manage.py update_security_advisories
./manage.py l10n_update
#requires twitter api credentials not distributed publicly
./manage.py cron update_tweets
./manage.py runscript update_firefox_os_feeds
