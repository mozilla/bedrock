# 4. Use Fluent For Localization

Date: 2019-12-16

## Status

Accepted

## Context

The current localization (l10n) system uses the outdated and unsupported .lang format, which our l10n team would prefer
to no longer support. Mozilla's current l10n standard for products and websites is [Fluent][].

## Decision

In order to update our l10n practices and technology and support from Mozilla's existing l10n infrastructure and teams
we will decomission the .lang system in bedrock and implement one based on [Fluent][]. We will support both during a
transition period.

## Consequences

Dealing with strings and templates is very different in Fluent (see the updated [bedrock docs][]). There will be a period
of developer training and adjustment to the new way of writing and previewing templates. The biggest change is that strings
are no longer in the templates at all, and are instead referenced by string IDs which are in Fluent files (.ftl files).

The positive side of this change is that the developer has total control over the strings in the translation files
and there are no string extraction or merge steps.

[Fluent]: https://projectfluent.org/
[bedrock docs]: https://bedrock.readthedocs.io/en/latest/l10n.html#fluent
