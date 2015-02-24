#!/bin/bash

# script to push out svn locale updates via cron

/data/bedrock/src/www.mozilla.org-django/bedrock/bin/update-scripts/prod/update-prod-locale.sh && \
/data/bedrock/deploy www.mozilla.org-django/bedrock/locale
