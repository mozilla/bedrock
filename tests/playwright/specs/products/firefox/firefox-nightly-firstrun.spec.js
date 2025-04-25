/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/nightly/firstrun/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Calls to action are displayed', async ({ page }) => {
            const testingButton = page.getByTestId('start-testing');
            const codingButton = page.getByTestId('start-coding');
            const localizingButton = page.getByTestId('start-localizing');

            await expect(testingButton).toBeVisible();
            await expect(codingButton).toBeVisible();
            await expect(localizingButton).toBeVisible();
        });
    }
);
