/* eslint-env node */
const { withHelpers } = require('@jungvonmatt/contentful-migrations');

/**
 * Contentful migration
 * API: https://github.com/contentful/contentful-migration
 * Editor Interfaces: https://www.contentful.com/developers/docs/extensibility/app-framework/editor-interfaces/
 */

// Publish all Resource Center pages

const RESOURCE_CENTER_PAGE = 'pagePageResourceCenter';

module.exports = withHelpers(async function (migration, context, helpers) {
    allEntries = await context.makeRequest({
        method: 'get',
        url: '/entries'
    });
    const resourceCenterPageEntries = allEntries.items.filter(
        (entry) => entry.sys.contentType.sys.id == RESOURCE_CENTER_PAGE
    );

    await resourceCenterPageEntries.forEach((rcPageEntry) => {
        if (rcPageEntry.sys.publishedVersion < rcPageEntry.sys.version) {
            console.log(`Publishing changed page ${rcPageEntry.sys.id}`);
            const resp = context.makeRequest({
                method: 'put',
                url: `/entries/${rcPageEntry.sys.id}/published`,
                headers: {
                    'X-Contentful-Version': rcPageEntry.sys.version
                }
            });
        } else {
            console.log(
                `Page ${rcPageEntry.sys.id} was already Published, so skipping`
            );
        }
    });
});
