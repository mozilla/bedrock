# Contentful Migration Scripts

## What is this?

This directory contain scripts (written in Javascript) that execute Contentful migrations related to content used in Bedrock - eg, changes to the schema or data of a particular Contentful environment.

It does not, currently, contain a complete CMS-as-Code approach. Each migration in here is a
one-off scripted change intended for one-off use, outside of CI. The migrations are run via
the [contentful-migrations](https://github.com/jungvonmatt/contentful-migrations) framework,
which wraps Contentful's own `contentful-migration` library.

## How do I use it?

**Groundwork**

* Have Node.js installed (any recent/LTS version will be ok)
* `$ cd /path/to/checkout/of/bedrock/contentful_migrations/`
* `$ npm install` to add the `contentful-migrations` tool
* `$ npx contentful login` to get an authentication token via your browser

### To apply an existing migration

`npx migrations execute -e TARGET_CONTENTFUL_ENVIRONMENT -v migrations/MIGRATION_FILE_NAME.cjs`

This will run the migration and also set a `Migrations` Entry in Contentful, with the number of
the migration and a success state. This record is useful in showing us what migrations have
run on what environment.

### To unmark a migration as applied

Unlike Django Migrations, you can re-apply a Contentful migration without having to first roll
it back, as long as the operations in that migration still make sense compared to the state of
your target environment. However, say you manually un-do the changes set up by a migration and
you want to show others that it effectively no longer is applied there. In that case, do this:

`npx migrations version -e TARGET_CONTENTFUL_ENVIRONMENT -v --remove migrations/MIGRATION_FILE_NAME.cjs`

Honestly speaking, there's not a lot of value in this command right now, but maybe we can
contribute some improvements to make it more like Django Migrations in its locking/denying
behaviour.

### To make a new migration

`npx migrations generate` and then fill in the skeleton migration file created. The number used in the default filename is a timestamp, showing the order migration files were created in. You should
add to it so the filename helps indicate what the file does, too.

## Is there a safe mode or dry run option?

No. If you're unsure about what the script does, fork the production environment in Contentful to a new environment and then try the script on that first.

## Roadmap

* [DONE] - use migrations (via contentful-migrations framework) to move from Legacy Compose to new Compose. This also acts as a POC for using it within Bedrock. Migrations will be manually run for now.
* [TODO] - plan how we'll move to [CMS-as-Code](https://www.contentful.com/help/cms-as-code/) for Bedrock pages that use Contentful, including CI integration so that migrations are auto-run.
* [TODO] - Move to CMS-as-Code, formally.
