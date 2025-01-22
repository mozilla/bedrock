/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../scripts/open-page');
const url = '/en-US/firefox/?geo=de&mozcb=y';

test.describe(
    `${url} page`,
    {
        tag: '@mozorg'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Accept cookies', async ({ page }) => {
            const banner = page.getByTestId('consent-banner');
            const acceptButton = page.getByTestId(
                'consent-banner-accept-button'
            );

            await expect(banner).toBeVisible();
            await acceptButton.click();
            await expect(banner).not.toBeVisible();
        });

        test('Reject cookies', async ({ page }) => {
            const banner = page.getByTestId('consent-banner');
            const acceptButton = page.getByTestId(
                'consent-banner-reject-button'
            );

            await expect(banner).toBeVisible();
            await acceptButton.click();
            await expect(banner).not.toBeVisible();
        });
    }
);
