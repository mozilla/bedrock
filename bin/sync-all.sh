#!/bin/bash
set -ex
if [ ! -e ./manage.py ]; then
    # this does not support symlinks
    script_parent_dir=${0%/*}/..
    cd $script_parent_dir
fi

# for heroku demos
# heroku doesn't pull git submodules
if [[ ! -d ./vendor-local/src/legal-docs/firefox_privacy_notice ]]; then
    rm -rf ./vendor-local/src/legal-docs
    git clone --depth 1 https://github.com/mozilla/legal-docs.git vendor-local/src/legal-docs
fi

./bin/run-db-download.py --force
./manage.py migrate --noinput
./bin/run-db-update.sh --all || true
./manage.py l10n_update
./manage.py update_sitemaps
