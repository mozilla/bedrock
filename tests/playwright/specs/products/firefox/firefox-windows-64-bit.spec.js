/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/browsers/windows-64-bit/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Download button is displayed', async ({ page }) => {
            const downloadButtonPrimary = page.getByTestId(
                'win64-hero-download'
            );
            const downloadButtonSecondary = page.getByTestId(
                'win64-bottom-download'
            );

            await expect(downloadButtonPrimary).toBeVisible();
            await expect(downloadButtonSecondary).toBeVisible();
        });
    }
);
