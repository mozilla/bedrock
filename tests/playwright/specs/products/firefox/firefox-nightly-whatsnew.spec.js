/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/139.0a1/whatsnew/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Up-to-date message is displayed', async ({
            page,
            browserName
        }) => {
            test.skip(
                browserName !== 'firefox',
                'Page shown to Firefox browsers only'
            );

            const updateMessage = page.getByTestId(
                'nightly-whatsnew-update-message'
            );
            await expect(updateMessage).toBeVisible();
        });
    }
);
