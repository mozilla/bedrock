#!/bin/bash -e

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Exports the postgres database to a sqlite file, which can be copied to the
# cloud bucket for consumption by web pods.

# CRITICAL: requires DATABASE_URL in the environment (or temporarily set at the
# time of running), pointing to the source *Postgres* DB

# Usage if you have DATABASE_URL in your Environment:
# cd /path/to/checkout/of/bedrock/
# ./bin/export-db-to-sqlite.sh /path/to/output.db

# Usage if you do not have DATABASE_URL in your Environment:
# cd /path/to/checkout/of/bedrock/
# DATABASE_URL="postgres://user:pass@host:5432/bedrock" ./bin/export-db-to-sqlite.sh /path/to/output.db

# If you want to run this in debug mode, insert `bash -ex` (without quotes) before ./bin/

# Set up variables to point to the new output DB and to a temporary sql script which we'll generate later

output_db=$1
nullify_specific_columns_sql="/tmp/nullify_specific_columns.sql"

# We'll use this sentinel to track success, along with a helper function that
# checks the most recent return code and the sentinel are 'truthy'/happy

all_well=true

check_status_and_handle_failure() {
    if [[ $? -ne 0 || $all_well == false ]]; then
        echo "[ERROR] There was a problem with the export process: $1"
        echo "Deleting export DB and utility sql scripts"
        rm -f $output_db $nullify_specific_columns_sql
        exit 128
    fi
}

# There are some tables that get auto-populated - eg via Django migrations -
# that we need to purge to ensure there are no conflicts with the data we load
# in from the source DB.
# We define these up here for easier exensibility.

tables_to_wipe_after_initial_migrate=(
    "django_content_type"
    "django_session"
    "auth_group_permissions"
    "auth_group"
    "auth_permission"
    "product_details_productdetailsfile"
)

# There are some tables that we can't avoid porting to sqlite from the
# source DB, but which we want to exclude from the export, and also ensure
# we nullify any relations that link TO these tables rather than cascade on
# delete.
# We define these up here for easier exensibility.

tables_to_wipe_after_import=(
    "auth_user"
    "auth_user_groups"
    "auth_user_user_permissions"
    "wagtailcore_revision"
)

# We should be reading data from a Postgres DB. Are we configured appropriately?
ACTIVE_DATABASE=$(python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['ENGINE'])")

if [[ $ACTIVE_DATABASE != *"postgres"* ]]; then
    echo "ERROR: Django's active database does not point to a Postgres database."
    all_well=false
fi

check_status_and_handle_failure "Getting source Postgres database"
echo "Checked that source DB is Postgres"

# Back up DATABASE_URL, to restore later
export ORIGINAL_DATABASE_URL=$DATABASE_URL

# Dump out to JSON from the default, source DB
echo "Dumping JSON from the source DB:"

python manage.py dumpdata \
    contenttypes \
    --indent 2 \
    --output /tmp/export_contenttypes.json || all_well=false

check_status_and_handle_failure "Dumping contenttypes"

python manage.py dumpdata \
    wagtailcore.Locale \
    --indent 2 \
    --output /tmp/export_wagtail_locales.json || all_well=false

check_status_and_handle_failure "Dumping wagtailcore.Locale"

# Deliberate exclusions:
# sessions.Session              # Excluded: security risk
# contenttypes.ContentType      # Excluded: Dumped separately
# wagtailusers.UserProfile      # Excluded: PII
# wagtailimages.Rendition       # Excluded: Renditions
# wagtail_localize_smartling    # Excluded wholesale: translation data may leak draft content
# wagtail_localize              # Excluded wholesale: translation data may leak draft content
# wagtailsearch.IndexEntry      # Excluded: WagtailSearch indices need rebuilding and search history is not important
# wagtailcore.Locale            # Excluded: dumped separately
# wagtailcore.ModelLogEntry     # Excluded: may contain PII
# wagtailcore.CollectionViewRestriction  # Excluded: may include passwords
# wagtailcore.UploadedFile      # Excluded: unavailable data in local builds
# wagtailcore.ReferenceIndex    # Excluded: can be rebuilt locally
# wagtailcore.Revision          # Excluded: drafts may leak pre-published content, or stale/dead content
# wagtailcore.PageViewRestriction  # Excluded: may include passwords
# wagtailcore.TaskState         # Excluded: comment field may contain sensitive info
# wagtailcore.WorkflowState     # Excluded: if included, causes integrity errors because it needs TaskState to be present, too
# wagtailcore.PageLogEntry      # Excluded: may contain sensitive info
# wagtailcore.Comment           # Excluded: may contain sensitive info
# wagtailcore.CommentReply      # Excluded: may contain sensitive info
# wagtailcore.PageSubscription  # Excluded: dependent on User model
# django_rq.Queue               # Excluded: irrelevant to local use and not a real DB table: data lives in Redis
# django.contrib.admin.LogEntry # Excluded: dependent on User model
# wagtaildraftsharing.Wagtaildraftsharinglink  # Excluded: sensitive, linked to user, and also irrelevant because the Revisions do not exist

# Deliberate TEMPORARY INCLUSIONS (because without them we cannot load the data) - tables are
# cleaned at the end, which is why they are in the tables_to_wipe_after_import variable, defined earlier.
#
# auth.User                     # Will be purged because of  PII
# wagtailcore.Revision          # Will be purged: drafts may leak pre-published content, or stale/dead content

# MAIN LIST OF MODELS BEING EXPORTED

python manage.py dumpdata \
    auth.Permission \
    auth.Group \
    auth.User \
    product_details.ProductDetailsFile \
    wagtailredirects.Redirect \
    wagtaildocs.Document \
    wagtailembeds.Embed \
    wagtailimages.Image \
    wagtailadmin.Admin \
    wagtailcore.Site \
    wagtailcore.Collection \
    wagtailcore.GroupCollectionPermission \
    wagtailcore.Page \
    wagtailcore.Revision \
    wagtailcore.GroupPagePermission \
    wagtailcore.WorkflowPage \
    wagtailcore.WorkflowContentType \
    wagtailcore.WorkflowTask \
    wagtailcore.Task \
    wagtailcore.Workflow \
    wagtailcore.GroupApprovalTask \
    taggit.Tag \
    taggit.TaggedItem \
    waffle.Switch \
    cms.StructuralPage \
    cms.SimpleRichTextPage \
    cms.BedrockImage \
    legal_docs.LegalDoc \
    anonym.AnonymIndexPage \
    anonym.AnonymContentSubPage \
    anonym.AnonymNewsPage \
    anonym.AnonymNewsItemPage \
    anonym.AnonymCaseStudyItemPage \
    anonym.AnonymCaseStudyPage \
    anonym.AnonymContactPage \
    anonym.Person \
    mozorg.WebvisionDoc \
    mozorg.LeadershipPage \
    mozorg.AdvertisingIndexPage \
    mozorg.AdvertisingTwoColumnSubpage \
    mozorg.ContentSubpage \
    mozorg.HomePage \
    mozorg.ContactBannerSnippet \
    mozorg.NotificationSnippet \
    newsletter.Newsletter \
    products.VPNCallToActionSnippet \
    products.VPNResourceCenterIndexPage \
    products.VPNResourceCenterDetailPage \
    products.MonitorCallToActionSnippet \
    products.MonitorArticleIndexPage \
    products.MonitorArticlePage \
    externalfiles.ExternalFile \
    security.Product \
    security.SecurityAdvisory \
    security.HallOfFamer \
    security.MitreCVE \
    releasenotes.ProductRelease \
    contentcards.ContentCard \
    utils.GitRepoState \
    wordpress.BlogPost \
    sitemaps.SitemapURL \
    careers.Position \
    --indent 2 \
    --output /tmp/export_remainder.json || all_well=false

check_status_and_handle_failure "Dumping main data"

# Prep a fresh sqlite DB with schema, deleting the original
echo "Setting up a fresh Sqlite DB ($output_db) and running migrations:"

rm -f $output_db || all_well=false

export DATABASE_URL=sqlite:///$output_db  # Note that the three slashes is key - see dj-database-url docs

check_status_and_handle_failure "Setting up new output DB at $output_db"

PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage \
    python manage.py migrate || all_well=false

check_status_and_handle_failure "Running Django migrations"

# We want to use all the data from the JSON, so let's drop the rows
# that have been automatically populated during migrate, including all the Wagtail
# ones, except for wagtailsearch's tables because there's a virtual table that
# causes fatal problems when loading data if it's empty. We'll update this later
# in this script

for table in $(sqlite3 $output_db ".tables 'wagtail%'")
do
    if [[ $table != wagtailsearch_* ]]; then
        sqlite3 $output_db "DELETE FROM $table;"
        echo "Purged default-added data from: $table"
    fi
done

# Let's also purge the the Django ones we lined up for cleaning earlier
for table in "${tables_to_wipe_after_initial_migrate[@]}"
do
    sqlite3 $output_db "DELETE FROM $table"
    echo "Purged default-added data from: $table"
done

# Don't forget to reset sequences
sqlite3 $output_db "VACUUM";

echo "Purged data that was automatically added via Django/Wagtail migrations"

# Load the data, getting the contenttypes table in first
PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage \
    python manage.py loaddata \
        "/tmp/export_contenttypes.json" \
        "/tmp/export_wagtail_locales.json" \
        "/tmp/export_remainder.json" \
        || all_well=false

check_status_and_handle_failure "Loading data from JSON"

# There are things we can't omit or redact in the steps above, so
# we need to manually delete them once we've served their purpose

# Delete rows from tables mentioned in tables_to_wipe_after_import
for table in "${tables_to_wipe_after_import[@]}"
do
    sqlite3 $output_db "DELETE FROM $table"
    echo "Purged now-redundant data from: $table"
done

# Delete Wagtail Page records that are not marked as Live
# sqlite3 $output_db "DELETE FROM wagtailcore_page WHERE live=0;"
# echo "Purged Page records that are not marked as live any more"

# And to be sure that there are no relations pointing back to non-existent rows
echo "Preparing statements for nullifying columns in temporary sql file. (Output is hidden because it's captured from stdout)."

# Convert the array into a comma-separated string suitable for the SQL IN clause
tables_list=$(printf "'%s'," "${tables_to_wipe_after_import[@]}")
tables_list=${tables_list%,}  # Remove the trailing comma

# Execute the SQLite commands
sqlite3 "$output_db" <<EOF
BEGIN;

-- Step 1: Create a temporary table to store the relations
CREATE TEMPORARY TABLE fk_relations AS
SELECT
    fk_table.name AS table_name,
    fk."from" AS fk_column
FROM
    sqlite_master AS fk_table
JOIN
    pragma_foreign_key_list(fk_table.name) AS fk
WHERE
    fk."table" IN ($tables_list)
AND
    fk_table.type = 'table';

-- Step 2: Generate and execute UPDATE statements in a loop
-- Output the UPDATE statements and execute them immediately
.output $nullify_specific_columns_sql
SELECT
    'UPDATE "' || table_name || '" SET "' || fk_column || '" = NULL;'
FROM
    fk_relations;
.output stdout

-- Step 3: Execute the generated SQL statements
.read $nullify_specific_columns_sql

COMMIT;
EOF

echo "This is the SQL we ran to null out the columns:"
cat $nullify_specific_columns_sql || all_well=false
check_status_and_handle_failure "Showing temporary SQL file"

rm -f $nullify_specific_columns_sql || all_well=false
check_status_and_handle_failure "Removing temporary SQL file"
echo "Deleted that temporary sql"

python manage.py rebuild_references_index
check_status_and_handle_failure "Running rebuild_references_index"

python manage.py wagtail_update_index
check_status_and_handle_failure "Running wagtail_update_index"
echo "Rebuilt Wagtail object reference helper and search index"

# Check if tables in tables_to_wipe_after_import are empty
echo "Checking that the tables we expect to be empty are empty"
for table in "${tables_to_wipe_after_import[@]}"
do
    count=$(sqlite3 $output_db "SELECT COUNT(*) FROM $table")
    if [[ $count -ne 0 ]]; then
        echo "ERROR: Table $table is not empty"
        all_well=false
    fi
done
check_status_and_handle_failure "Seeking expected empty tables"

export DATABASE_URL=$ORIGINAL_DATABASE_URL
echo "Restored original DATABASE_URL to $DATABASE_URL"

check_status_and_handle_failure "Checking all_well at the end of the run"

echo "Export to $output_db successful"

# If all is well, ping DMS to avoid an alert being raised.
if [[ -n "${DB_EXPORT_SCRIPT_DMS_URL}" ]]; then
    curl -m 10 --retry 5 "${DB_EXPORT_SCRIPT_DMS_URL}"
    echo "Pinged snitch"
fi
