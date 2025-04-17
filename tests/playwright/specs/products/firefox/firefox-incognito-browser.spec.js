/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/browsers/incognito-browser/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Download button is displayed', async ({ page, browserName }) => {
            const downloadButtonPrimary = page.getByTestId(
                'download-button-primary'
            );
            const downloadButtonSecondary = page.getByTestId(
                'download-button-secondary'
            );

            if (browserName === 'firefox') {
                await expect(downloadButtonPrimary).not.toBeVisible();
                await expect(downloadButtonSecondary).toBeVisible();
            } else {
                await expect(downloadButtonPrimary).toBeVisible();
                await expect(downloadButtonSecondary).toBeVisible();
            }
        });
    }
);
