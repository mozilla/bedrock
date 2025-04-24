/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../scripts/open-page');
const url = '/en-US/about/';

test.describe(
    `${url} page`,
    {
        tag: '@mozorg'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('404 page back link', async ({ page }) => {
            await page.goto('/en-US/404/?automation=true');
            const goBackLink = page.getByTestId('link-go-back');
            await expect(goBackLink).toBeVisible();
            await goBackLink.click();
            await page.waitForURL('**/about/?automation=true', {
                waitUntil: 'commit'
            });
        });
    }
);
