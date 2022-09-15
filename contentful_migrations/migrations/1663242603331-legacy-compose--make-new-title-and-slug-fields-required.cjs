/* eslint-env node */
const { withHelpers } = require('@jungvonmatt/contentful-migrations');

/**
 * Contentful migration
 * API: https://github.com/contentful/contentful-migration
 * Editor Interfaces: https://www.contentful.com/developers/docs/extensibility/app-framework/editor-interfaces/
 */

const RESOURCE_CENTER_PAGE = 'pagePageResourceCenter';

module.exports = withHelpers(async function (migration, context, helpers) {
    const resourceCenterPage = migration.editContentType(RESOURCE_CENTER_PAGE);
    resourceCenterPage.editField('title').required(true);
    resourceCenterPage.editField('slug').required(true);
});
