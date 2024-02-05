/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

/**
 * Opens a page with a given URL, page, and browser name.
 * @param {String} url - The URL to open.
 * @param {Object} page - The Playwright page object.
 * @param {String} browserName  - The Playwright browser name.
 */
const openPage = async (url, page, browserName) => {
    /**
     * Add user agent override script based on the browser name.
     * This enables tests to mock the user agent strings for testing purposes.
     * @see https://playwright.dev/docs/api/class-page#page-add-init-script
     */
    if (browserName === 'webkit') {
        await page.addInitScript({
            path: `./scripts/useragent/mac/${browserName}.js`
        });
    } else {
        await page.addInitScript({
            path: `./scripts/useragent/win/${browserName}.js`
        });
    }

    // Add query parameter to the URL to filter out automation traffic.
    const separator = url.includes('?') ? '&' : '?';
    await page.goto(url + separator + 'automation=true');
};

module.exports = openPage;
