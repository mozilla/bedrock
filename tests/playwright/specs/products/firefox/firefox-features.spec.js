/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/features/';
const slugs = [
    'adblocker',
    'add-ons',
    'picture-in-picture',
    'private-browsing',
    'private',
    'sync',
    'translate'
];

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        for (const slug of slugs) {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(url + `${slug}/`, page, browserName);
            });

            test(`Feature page: /${slug}/`, async ({ page, browserName }) => {
                const downloadButton = page.getByTestId(
                    'features-footer-download'
                );

                if (browserName === 'firefox') {
                    await expect(downloadButton).not.toBeVisible();
                } else {
                    await expect(downloadButton).toBeVisible();
                }
            });
        }
    }
);
