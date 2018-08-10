#!/bin/bash
set -ex
if [ ! -e ./manage.py ]; then
    # this does not support symlinks
    script_parent_dir=${0%/*}/..
    cd $script_parent_dir
fi

if [[ ! -f .env ]]; then
    cp .env-dist .env
fi

# get legal-docs
git submodule sync
git submodule update --init --recursive

# get fresh database
./bin/run-db-download.py --force

# get fresh l10n files
./manage.py l10n_update
