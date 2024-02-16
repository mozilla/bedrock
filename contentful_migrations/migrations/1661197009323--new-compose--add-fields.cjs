/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

const { withHelpers } = require('@jungvonmatt/contentful-migrations');

/**
 * Contentful migration
 * API: https://github.com/contentful/contentful-migration
 * Editor Interfaces: https://www.contentful.com/developers/docs/extensibility/app-framework/editor-interfaces/
 */

const RESOURCE_CENTER_PAGE = 'pagePageResourceCenter';
const LEGACY_COMPOSE_PAGE = 'page';
module.exports = withHelpers(async function (migration, context, helpers) {
    const pagePageResourceCenterMigration =
        migration.editContentType(RESOURCE_CENTER_PAGE);

    // 1. Add fields to our custom page that were previously on the Compose: Page model
    pagePageResourceCenterMigration
        .createField('title')
        .name('Page title')
        .type('Symbol')
        .localized(true)
        .required(false) // change this to True later on, after population
        .validations([])
        .disabled(false)
        .omitted(false);
    pagePageResourceCenterMigration
        .createField('slug')
        .name('Slug')
        .type('Symbol')
        .localized(true)
        .required(false) // change this to True later on, after population
        .validations([])
        .disabled(false)
        .omitted(false);
    pagePageResourceCenterMigration
        .createField('seo')
        .name('SEO metadata')
        .type('Link')
        .linkType('Entry')
        .localized(true)
        .required(false)
        .validations([])
        .disabled(false)
        .omitted(false);

    // 2. Add the “Aggregate Root” annotation to the page type so it can work
    // as a page without needing Compose:Page to parent it
    pagePageResourceCenterMigration.setAnnotations([
        'Contentful:AggregateRoot'
    ]);

    // 3. Activate the page type
    // DISABLED because we get a HTTP 409: Conflict, but with no details, so am
    // assuming it's because the page is _already_ live. Will see...
    // const resp = await context.makeRequest({
    //     method: 'PUT',
    //     url: `/content_types/${RESOURCE_CENTER_PAGE}/published`
    // });
});
