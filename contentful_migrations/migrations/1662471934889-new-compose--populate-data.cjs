/* eslint-env node */
const { withHelpers } = require('@jungvonmatt/contentful-migrations');

// DEPENDS on 1661197009323--new-compose--add-fields.cjs

/**
 * Contentful migration
 * API: https://github.com/contentful/contentful-migration
 * Editor Interfaces: https://www.contentful.com/developers/docs/extensibility/app-framework/editor-interfaces/
 */
module.exports = withHelpers(async function (migration, context, helpers) {
    // Copy field data from Compose:Page parent to now-standalone child

    const RESOURCE_CENTER_PAGE = 'pagePageResourceCenter';
    const LEGACY_COMPOSE_PAGE = 'page';

    migration.transformEntries({
        contentType: LEGACY_COMPOSE_PAGE,
        from: ['content', 'seo', 'title', 'slug'],
        to: ['content', 'seo', 'title', 'slug'],
        transformEntryForLocale: async (fromFields, currentLocale) => {
            if (currentLocale != 'en-US') {
                return;
            }
            console.log(
                'IMPORTANT: handling en-US locale ONLY and skipping all other locales'
            );

            // Moving data across entries doesn't appear supported via helpers, so
            // let's patch the relevant pagePageResourceCenter Entry
            // via the API manually:
            // https://www.contentful.com/developers/docs/references/content-management-api/#/reference/entries/entry/patch-an-entry/console/js

            if (
                !fromFields['content'][currentLocale].sys ||
                !fromFields['seo'][currentLocale].sys
            ) {
                console.log(
                    'Missing data, so skipping entry for ',
                    currentLocale
                );
                return;
            }

            const contentPageEntryId =
                fromFields['content'][currentLocale].sys.id;
            const seoObjectEntryId = fromFields['seo'][currentLocale].sys.id;

            // Get the actual content entry to get the data we need to fill in,
            // so we can check if it's a pagePageResourceCenter
            const contentPageEntry = await context.makeRequest({
                method: 'get',
                url: `/entries/${contentPageEntryId}`
            });
            if (
                contentPageEntry.sys.contentType.sys.id == RESOURCE_CENTER_PAGE
            ) {
                const payload = [
                    {
                        op: 'add',
                        path: '/fields/title',
                        value: {
                            [currentLocale]: fromFields['title'][currentLocale]
                        }
                    },
                    {
                        op: 'add',
                        path: '/fields/slug',
                        value: {
                            [currentLocale]: fromFields['slug'][currentLocale]
                        }
                    },
                    {
                        op: 'add',
                        path: '/fields/seo',
                        value: {
                            [currentLocale]: {
                                sys: {
                                    type: 'Link',
                                    linkType: 'Entry',
                                    id: seoObjectEntryId
                                }
                            }
                        }
                    }
                ];
                result = await context.makeRequest({
                    method: 'patch',
                    url: `/entries/${contentPageEntryId}`,
                    headers: {
                        'Content-Type': 'application/json-patch+json',
                        'X-Contentful-Version': contentPageEntry.sys.version
                    },
                    data: payload
                });
                console.log('Result of data migration =>', result);
            }
            // Returning no data signals no change to the Compose:Page (from where we get fromFields),
            // but we'll have executed the Contentful Management API calls to update data in
            // the target page anyway.
            return;
        }
    });
});
