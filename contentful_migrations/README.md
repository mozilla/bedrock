# Contentful Migration Scripts

## What is this?

This directory contains simple JS scripts that execute Contentful migrations related to content used in Bedrock - eg, changes to the schema or data of a particular Contentful environment.

It does not, currently, contain a complete CMS-as-Code approach. Each migration in here is a one-off scripted change intended for one-off use, outside of CI.

## How do I use it?

* Have Node.js installed (any recent/LTS version will be ok)
* `$ cd /path/to/checkout/of/bedrock/contentful_migrations/`
* `$ npm install`
* `$ npx contentful login`
* `$ npx migrations init`

<!-- * UPDATE ALL THE FOLLOWING * UPDATE ALL THE FOLLOWING * UPDATE ALL THE FOLLOWING *

* Have the following env vars set (either via the CLI or by adding an .env file)
  * `CONTENTFUL_SPACE_ID`
  * `CONTENTFUL_ACCESS_TOKEN` - this is a Personal Access Token in your name
  * There is a template .env file in the repo which you can duplicate for use with `$ cp .env.dist .env`

TODO UPDATE ME FROM HERE ON  * Note that you will have to pass the environment as a CLI arg, to ensure you're definitely working on the thing you want to work on



Each migration script is executable from the CLI - eg:

UPADTE THIS

  `$ ./migrations/0099_flux_capacitor_upgrade.js --environment=lebowski-dev`

## Is there a safe mode or dry run option?

No. If you're unsure about what the script does, fork the production environment in Contentful to a new environment and then try the script on that first.

## Roadmap

The plan is to make this more sophisticated, including:

* Store state for which envs have had which migrations applied and when. This info will live in a shared store (eg Contentful itself, or Bedrock's DB)


-->
