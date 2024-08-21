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

# 0. Are we configured appropriately?
ACTIVE_DATABASE=$(python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['ENGINE'])")

if [[ $ACTIVE_DATABASE != *"postgres"* ]]; then
    echo "ERROR: Django's active database does not point to a Postgres database."
    all_well=false
fi

# Back up DATABASE_URL
export ORIGINAL_DATABASE_URL=$DATABASE_URL

check_status 100

# 1. Dump out to json from the default, source DB

python manage.py dumpdata \
    contenttypes \
    --natural-primary \
    --natural-foreign \
    --indent 2 \
    --output /tmp/export_contenttypes.json || all_well=false

python manage.py dumpdata \
    wagtailcore.Locale \
    --natural-primary \
    --natural-foreign \
    --indent 2 \
    --output /tmp/export_wagtail_locales.json || all_well=false


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
    --natural-primary \
    --natural-foreign \
    --indent 2 \
    --output /tmp/export_remainder.json || all_well=false

check_status 99

# 2. Prep a fresh sqlite DB with schema, deleting the original
rm -f $output_db

export DATABASE_URL=sqlite:///$output_db  # Note that the three slashes is key - see dj-database-url docs

check_status 98

PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage \
    python manage.py migrate --verbosity=3 || all_well=false

check_status 97

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

# 4. Load the data, getting the contenttypes table in first
PROD_DETAILS_STORAGE=product_details.storage.PDFileStorage \
    python manage.py loaddata \
        "/tmp/export_contenttypes.json" \
        "/tmp/export_wagtail_locales.json" \
        "/tmp/export_remainder.json" \
        || all_well=false

check_status 96

# 5. There are things we can't omit or redact in the steps above, so
# we need to manually delete them

sqlite3 $output_db "DELETE FROM auth_user";
sqlite3 $output_db "DELETE FROM wagtailcore_revision";

check_status 95

echo "Export to $output_db successful"

# Back up DATABASE_URL
export DATABASE_URL=$ORIGINAL_DATABASE_URL
echo "Restoring original DATABASE_URL to $DATABASE_URL"
