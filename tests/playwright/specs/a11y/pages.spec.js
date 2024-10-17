/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const openPage = require('../../scripts/open-page');
const { createReport, scanPage } = require('./includes/helpers');
const { desktopTestURLs, mobileTestURLs } = require('./includes/urls');
const { test, expect } = require('@playwright/test');

for (const url of desktopTestURLs) {
    test.describe(
        `${url} page (desktop)`,
        {
            tag: '@a11y'
        },
        () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(url, page, browserName);
            });

            test('should not have any detectable a11y issues', async ({
                page
            }) => {
                const results = await scanPage(page);
                createReport(url, 'desktop', results);
                expect(results.violations.length).toEqual(0);
            });
        }
    );
}

for (const url of mobileTestURLs) {
    test.describe(
        `${url} page (mobile)`,
        {
            tag: '@a11y'
        },
        () => {
            test.use({ viewport: { width: 360, height: 780 } });

            test.beforeEach(async ({ page, browserName }) => {
                await openPage(url, page, browserName);
            });

            test('should not have any detectable a11y issues', async ({
                page
            }) => {
                const results = await scanPage(page);
                createReport(url, 'mobile', results);
                expect(results.violations.length).toEqual(0);
            });
        }
    );
}
