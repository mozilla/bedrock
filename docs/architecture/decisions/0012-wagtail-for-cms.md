# 12. Use Wagtail as Bedrock's CMS

Date: 2024-04-15

## Status

Accepted

## Context

As Bedrock evolves, expanding the number of content-managed pages will give us greater agility. We needed to evaluate our options and pick a best-fit solution.

## Decision

We previously used Contentful as a headless CMS, but have decided
(<https://docs.google.com/document/d/1icqCOtCIMhducdrlKKYRBfGsbwsyrFTUH1wvjVldbKo/edit>) to move to Wagtail CMS (wagtail.org), which we'll integrate with the Bedrock codebase (<https://docs.google.com/document/d/1aQc-FRhI69XQwoaXmvbp9s7zy8UaCVQhZyF6RGTt4Lk/edit>)

## Consequences

* There is a significant amount of engineering work needed, including:
  * We'll need to integrate Wagtail into Bedrock, which first necessitates  refactoring away our bespoke i18n mechanism and using Django's own i18n logic.
  * We'll need to develop workflows around adding Wagtail-managed pages that the whole team understands
  * We'll need to integrate Wagtail with our chosen localization vendor, which requires a custom integration
  * Because we have stopped using Contentful as a source of data, we have the last exported state of the data in our DB, and will need to migrate pages that previously used Contentful to the new CMS
