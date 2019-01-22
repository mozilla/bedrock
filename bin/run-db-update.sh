#!/bin/bash
set -ex

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

python manage.py update_product_details_files
python manage.py update_security_advisories --quiet
python manage.py update_wordpress --quiet
python manage.py update_release_notes --quiet
python manage.py update_content_cards --quiet
python manage.py update_externalfiles --quiet
python manage.py update_newsletter_data --quiet
python manage.py update_www_config --quiet

if [[ "$AUTH" == true ]]; then
    # jobs that require some auth. don't run these during build.
    python manage.py update_pocketfeed --quiet
fi

if [[ "$ALL" == true ]]; then
    # less frequent. these will modify the DB every time.
    # TODO fix this
    if [[ "$AUTH" == true ]]; then
        python manage.py cron update_tweets
    fi
    python manage.py cron update_ical_feeds
fi
