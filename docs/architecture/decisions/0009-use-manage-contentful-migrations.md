# 9. Manage Contentful schema state via migrations

Date: 2022-09-09

## Status

Superseded by 0012

## Context

Our chosen CMS Contentful is powerful and can be configured via its UI  quite
easily. However, wanted to bring this under control using migrations so that
changes are explicit, reviewable, repeatable and stored. This would be a key
part of moving to a "CMS-as-Code" approach to using Contentful, where
content-type changes and data migrations (outside of regular content entry)
are managed via code.

## Decision

We wanted to have as close as possible to the experience provided by the
excellent Django Migrations framework, where we would:

* be able to script migrations, rather than resort to "clickops"
* be able to apply them individually or en masse
* be able to store the state of which migrations have/have not been applied
in a central datastore (and ideally Contentful)

We experimented with hand-cutting our own framework, which was looking viable,
but then we came across <https://github.com/jungvonmatt/contentful-migrations>
which does all of the above. We've evaluated it and it seems fit for purpose,
even if it has some gaps, so we've adopted it as our current way to manage and
apply migrations to our Contentful setup.

## Consequences

We've gained a tool that enables code-based changes to Contentful, which helps
in two ways:

1) It enables and eases the initial work to migrate from Legacy Compose to
new Compose (these are both ways of structuring pages in Contentful)
2) It lays tracks for moving to CMS-as-Code
