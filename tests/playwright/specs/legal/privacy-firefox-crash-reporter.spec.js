/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../scripts/open-page');
const url = '/legal/privacy/firefox.html#crash-reporter';

test.describe(
    `${url} page`,
    {
        tag: '@mozorg'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('health report redirect', async ({ page }) => {
            // Expected redirect URL
            const expectedRedirectUrl =
                'https://support.mozilla.org/en-US/kb/crash-report';

            // Wait for the redirect to happen
            await page.waitForURL(expectedRedirectUrl, {
                waitUntil: 'commit'
            });

            // Get the current URL
            const currentUrl = page.url();

            // Assert that the current URL is the expected redirect URL
            expect(currentUrl).toBe(expectedRedirectUrl);
        });
    }
);
