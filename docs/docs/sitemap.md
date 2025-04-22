# Sitemaps {: #sitemap }

`bedrock` serves a root sitemap at `/all-urls.xml`, which links to localised sitemaps for each supported locale.

The sitemap data is (re)generated on a schedule by the command `manage.py update_sitemaps_data` which is run as part of
a kubernetes (k8s) cron job that updates a number of data tables.

Bedrock's k8s cron job regularly runs `bin/run-db-update.sh`, which calls the `update_sitemaps_data` management command.
This command is what pulls URL data from bedrock `urls.py` files as well as URLs defined in the database and refreshes the
`SitemapURL` records in Bedrock's database. It is from these `SitemapURL` records that the XML sitemap tree is rendered by `bedrock`.
