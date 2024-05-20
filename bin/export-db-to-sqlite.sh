#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Exports the postgres database to a sqlite file, which can be copied to the
# cloud bucket for consumption by web pods.

# Usage:
# ./bin/export-db-to-sqlite.sh /path/to/output.db

# CRITICAL: requires DATABASE_URL in the environment (or temporarily set at the
# time of running), pointing to the source *Postgres* DB

output_db=$1

all_well=true

check_status() {
    if [[ $all_well == false ]]; then
        echo "ERROR: there was a problem with the export process. Error code: $1"
        exit $1
    fi
}

# 1. Dump out to json from the default, source DB

python manage.py dumpdata \
    contenttypes \
    --indent 2 \
    --natural-primary \
    --natural-foreign \
    --output /tmp/export_contenttypes.json || all_well=false

python manage.py dumpdata \
    wagtailcore.Locale \
    --indent 2 \
    --natural-foreign \
    --output /tmp/export_wagtail_locales.json || all_well=false


# Noted exclusions:
# * Sessions are transient and not needed
# * ContentTypes are dumped separately
# * Wagtail Locales are dumped separately
# * PageSubscription is based on User data, which is not ported over
# * Renditions are not needed as they can be regenerated
# * ReferenceIndex is not needed as it can be regenerated
# * WagtailSearch indices need rebuilding and search history is not important


python manage.py dumpdata \
    --natural-foreign \
    --exclude=contenttypes \
    --exclude=sessions.Session \
    --exclude=wagtailcore.Locale \
    --exclude=wagtailcore.PageSubscription \
    --exclude=wagtailimages.Rendition \
    --exclude=wagtailcore.ReferenceIndex \
    --exclude=wagtailsearch \
    --indent 2 \
    --output /tmp/export_remainder.json || all_well=false

check_status 99

# 2. Prep a fresh sqlite DB with schema, deleting the original
rm -f $output_db

PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage \
    DATABASE_URL=sqlite://$output_db \
    ./manage.py migrate || all_well=false

check_status 98

# 3. We want to use all the data from the JSON, so let's drop the ones
# that have been automatically populated including all the Wagtail ones
# except for the search indices

for tbl in $(sqlite3 $output_db ".tables 'wagtail%'")
do
    if [[ $tbl != wagtailsearch_* ]]; then
        sqlite3 $output_db "DELETE FROM $tbl;"
    fi
done

sqlite3 $output_db "DELETE FROM django_content_type";
sqlite3 $output_db "DELETE FROM django_session";
sqlite3 $output_db "DELETE FROM auth_group_permissions";
sqlite3 $output_db "DELETE FROM auth_group";
sqlite3 $output_db "DELETE FROM auth_permission";
sqlite3 $output_db "DELETE FROM auth_user_groups";
sqlite3 $output_db "DELETE FROM auth_user_user_permissions";
sqlite3 $output_db "DELETE FROM product_details_productdetailsfile";

# Don't forget to reset sequences
sqlite3 $output_db "VACUUM";

# 4. Load the data, getting the contenttypes table in first
PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage \
    DATABASE_URL=sqlite://$output_db \
    python manage.py loaddata \
        "/tmp/export_contenttypes.json" \
        "/tmp/export_wagtail_locales.json" \
        || all_well=false

check_status 97

PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage \
    DATABASE_URL=sqlite://$output_db \
    python manage.py loaddata "/tmp/export_remainder.json" || all_well=false

check_status 96

# 5. There are things we can't omit or redact in the steps above, so
# load the DB and programatically prune it, too
DATABASE_URL=sqlite://$output_db python manage.py scrub_exported_cms_data || all_well=false

check_status 95

echo "Export to $output_db successful"
