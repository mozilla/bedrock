#!/bin/bash -e

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
columns_to_nullify_sql="/tmp/columns_to_nullify.sql"

all_well=true

check_status_and_handle_failure() {
    if [[ $? -ne 0 || $all_well == false ]]; then
        echo "[ERROR] There was a problem with the export process: $1"
        echo "Deleting export-related files"
        rm -f $output_db $columns_to_nullify_sql
        exit 128
    fi
}

# 0. Are we configured appropriately?
ACTIVE_DATABASE=$(python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['ENGINE'])")

if [[ $ACTIVE_DATABASE != *"postgres"* ]]; then
    echo "ERROR: Django's active database does not point to a Postgres database."
    all_well=false
fi

check_status_and_handle_failure "Bad source database"
echo "Checked that source DB is Postgres"

# Back up DATABASE_URL
export ORIGINAL_DATABASE_URL=$DATABASE_URL

# 1. Dump out to json from the default, source DB
echo "Dumping JSON from the source DB:"

python manage.py dumpdata \
    contenttypes \
    --indent 2 \
    --output /tmp/export_contenttypes.json || all_well=false

check_status_and_handle_failure "Could not dump contenttypes"

python manage.py dumpdata \
    wagtailcore.Locale \
    --indent 2 \
    --output /tmp/export_wagtail_locales.json || all_well=false

check_status_and_handle_failure "Could not dump wagtailcore.Locale"

# Deliberate exclusions:
# sessions.Session  # Excluded: security risk
# contenttypes.ContentType  # Excluded: Dumped separately
# wagtailusers.UserProfile  # Excluded: PII
# wagtailimages.Rendition  # Excluded: Renditions
# wagtail_localize_smartling  # Excluded wholesale: translation data may leak draft content
# wagtail_localize  # Excluded wholesale: translation data may leak draft content
# wagtailsearch.IndexEntry  # Excluded: WagtailSearch indices need rebuilding and search history is not important
# wagtailcore.Locale  # Excluded: dumped separately
# wagtailcore.ModelLogEntry  # Excluded: may contain PII
# wagtailcore.CollectionViewRestriction  # Excluded: may include passwords
# wagtailcore.UploadedFile  # Excluded: unavailable data in local builds
# wagtailcore.ReferenceIndex  # Excluded: can be rebuilt locally
# wagtailcore.Revision  # Excluded: drafts may leak pre-published content, or stale/dead content
# wagtailcore.PageViewRestriction  # Excluded: may include passwords
# wagtailcore.TaskState  # Excluded: comment field may contain sensitive info
# wagtailcore.PageLogEntry  # Excluded: may contain sensitive info
# wagtailcore.Comment  # Excluded: may contain sensitive info
# wagtailcore.CommentReply  # Excluded: may contain sensitive info
# wagtailcore.PageSubscription  # Excluded: dependent on User model
# django_rq.Queue  # Excluded: irrelevant and may contain sensitive data in RQ obs

# Deliberate TEMPORARY INCLUSIONS (because without them we cannot load the data) - tables are cleaned at the end
# auth.User  # Will be excluded because of  PII
# wagtailcore.Revision  # Will be excluded: drafts may leak pre-published content, or stale/dead content

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
    wagtailcore.WorkflowState \
    taggit.Tag \
    taggit.TaggedItem \
    base.ConfigValue \
    cms.StructuralPage \
    cms.SimpleRichTextPage \
    cms.BedrockImage \
    cms.BedrockRendition \
    legal_docs.LegalDoc \
    mozorg.WebvisionDoc \
    newsletter.Newsletter \
    externalfiles.ExternalFile \
    security.Product \
    security.SecurityAdvisory \
    security.HallOfFamer \
    security.MitreCVE \
    releasenotes.ProductRelease \
    contentcards.ContentCard \
    contentful.ContentfulEntry \
    utils.GitRepoState \
    wordpress.BlogPost \
    sitemaps.SitemapURL \
    pocketfeed.PocketArticle \
    careers.Position \
    admin.LogEntry \
    --indent 2 \
    --output /tmp/export_remainder.json || all_well=false

check_status_and_handle_failure "Could not dump main data"

# 2. Prep a fresh sqlite DB with schema, deleting the original
echo "Setting up a fresh Sqlite DB ($output_db) and running migrations:"

rm -f $output_db || all_well=false

export DATABASE_URL=sqlite:///$output_db  # Note that the three slashes is key - see dj-database-url docs

check_status_and_handle_failure "Failed to powerwash db output path $output_db"

PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage \
    python manage.py migrate || all_well=false

check_status_and_handle_failure "Failed to run Django migrations"

# 3. We want to use all the data from the JSON, so let's drop the rows
# that have been automatically populated during migrate, including all the Wagtail ones
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

echo "Purged data that was automatically added via Django/Wagtail migrations"

# 4. Load the data, getting the contenttypes table in first
PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage \
    python manage.py loaddata \
        "/tmp/export_contenttypes.json" \
        "/tmp/export_wagtail_locales.json" \
        "/tmp/export_remainder.json" \
        || all_well=false

check_status_and_handle_failure "Failed to load data from JSON"

# 5. There are things we can't omit or redact in the steps above, so
# we need to manually delete them once we've served their purpose
echo "Preparing statements for nullifying columns in temporary sql file. (Output is hidden because it's captured from stdout)."

# Define the array of tables to be nullified
tables_to_nullify=("auth_user" "wagtailcore_revision")

# Convert the array into a comma-separated string suitable for the SQL IN clause
tables_list=$(printf "'%s'," "${tables_to_nullify[@]}")
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
.output $columns_to_nullify_sql
SELECT
    'UPDATE "' || table_name || '" SET "' || fk_column || '" = NULL;'
FROM
    fk_relations;
.output stdout

-- Step 3: Execute the generated SQL statements
.read $columns_to_nullify_sql

COMMIT;
EOF

echo "This is the SQL we ran to null out the columns:"
cat $columns_to_nullify_sql || all_well=false
check_status_and_handle_failure "Unable to show temporary SQL file"

rm -f $columns_to_nullify_sql || all_well=false
check_status_and_handle_failure "Unable to remove temporary SQL file"
echo "Deleted that temporary sql"

# 6. Delete rows from tables mentioned in tables_to_nullify
for table in "${tables_to_nullify[@]}"
do
    sqlite3 $output_db "DELETE FROM $table"
    echo "Purged now-redundant data from: $table"
done

# 7. Check if tables in tables_to_nullify are empty
for table in "${tables_to_nullify[@]}"
do
    count=$(sqlite3 $output_db "SELECT COUNT(*) FROM $table")
    if [[ $count -ne 0 ]]; then
        echo "ERROR: Table $table is not empty"
        all_well=false
    fi
done
echo "Checked that the tables we expect to be empty are empty"

check_status_and_handle_failure "Tables in tables_to_nullify are not empty when they should be"

export DATABASE_URL=$ORIGINAL_DATABASE_URL
echo "Restored original DATABASE_URL to $DATABASE_URL"

check_status_and_handle_failure "Final check for all_well turned out to be false"

echo "Export to $output_db successful"
