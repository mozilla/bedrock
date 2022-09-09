/* eslint-env node */
const { withHelpers } = require('@jungvonmatt/contentful-migrations');

// Improve the UI layout to help the developer experience.

/**
 * Contentful migration
 * API: https://github.com/contentful/contentful-migration
 * Editor Interfaces: https://www.contentful.com/developers/docs/extensibility/app-framework/editor-interfaces/
 */

const RESOURCE_CENTER_PAGE = 'pagePageResourceCenter';

module.exports = withHelpers(async function (migration, context, helpers) {
    const resourceCenterPage = migration.editContentType(RESOURCE_CENTER_PAGE);
    resourceCenterPage.moveField('title').afterField('name');
    resourceCenterPage.moveField('slug').afterField('title');
    resourceCenterPage.moveField('seo').afterField('slug');
});
