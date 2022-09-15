/* eslint-env node */
const { withHelpers } = require('@jungvonmatt/contentful-migrations');

// DEPENDS on 1661197009323--new-compose--add-fields.cjs and its prerequisite migration

/**
 * Contentful migration
 * API: https://github.com/contentful/contentful-migration
 * Editor Interfaces: https://www.contentful.com/developers/docs/extensibility/app-framework/editor-interfaces/
 */

const sleep = (milliseconds) =>
    new Promise((res) => setTimeout(res, milliseconds));

module.exports = withHelpers(async function (migration, context, helpers) {
    const LEGACY_COMPOSE_PAGE = 'page';

    // // 0. Get all Compose:Page entries
    allEntries = await context.makeRequest({
        method: 'get',
        url: '/entries'
    });
    const legacyComposePageEntries = allEntries.items.filter(
        (entry) => entry.sys.contentType.sys.id == LEGACY_COMPOSE_PAGE
    );

    // 1. Unpublish all Compose:Page entries
    await legacyComposePageEntries.forEach((composePageEntry) => {
        if (composePageEntry.sys.publishedVersion) {
            console.log(`Unpublishing Compose:Page ${composePageEntry.sys.id}`);
            const resp = context.makeRequest({
                method: 'delete',
                url: `/entries/${composePageEntry.sys.id}/published`,
                headers: {
                    'X-Contentful-Version':
                        composePageEntry.sys.publishedVersion
                }
            });
            console.log('Compose:Page unpublishing response:', resp);
        } else {
            console.log(
                `Compose:Page ${composePageEntry.sys.id} was not Published, so skipping`
            );
        }
    });

    // Give Contentful a moment to breathe before moving on, to avoid race
    // conditions and/or rate limiting
    console.log('Sleeping for 2s...');
    await sleep(2000);

    // 2. Delete all Compose:Page entries
    await legacyComposePageEntries.forEach((composePageEntry) => {
        console.log(`Deleting Compose:Page ${composePageEntry.sys.id}`);
        const resp = context.makeRequest({
            method: 'delete',
            url: `/entries/${composePageEntry.sys.id}`,
            headers: {
                'X-Contentful-Version': composePageEntry.sys.version
            }
        });
        console.log('Compose:Page deletion response:', resp);
    });

    // Give Contentful another moment to breathe before moving on
    console.log('Sleeping for another 2s...');
    await sleep(2000);

    // 3. Delete Compose:Page ContentType
    result = await migration.deleteContentType(LEGACY_COMPOSE_PAGE);
    console.log('Deleted Compose:Page content type. Result:', result);
});
