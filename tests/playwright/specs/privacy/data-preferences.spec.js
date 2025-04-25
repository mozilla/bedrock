/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../scripts/open-page');
const url = '/en-US/privacy/websites/data-preferences/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Test opt-out', async ({ page }) => {
            const status = page.getByTestId('data-preference-status');
            const optOutButton = page.getByTestId('button-opt-out');
            const optInButton = page.getByTestId('button-opt-in');

            await expect(status).toContainText(
                'You are opted in to first-party data collection'
            );
            await optOutButton.click();
            await expect(status).toContainText(
                'You are opted out of first-party data collection'
            );
            await optInButton.click();
            await expect(status).toContainText(
                'You are opted in to first-party data collection'
            );
        });
    }
);
