/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/facebookcontainer/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Get extension link displayed', async ({ page, browserName }) => {
            const getExtensionLink = page.getByTestId('get-extension-link');
            const downloadButtonMac = page.getByTestId(
                'download-firefox-cta-osx'
            );
            const downloadButtonWin = page.getByTestId(
                'download-firefox-cta-win'
            );

            if (browserName === 'firefox') {
                await expect(getExtensionLink).toBeVisible();
                await expect(downloadButtonMac).not.toBeVisible();
                await expect(downloadButtonWin).not.toBeVisible();
            } else if (browserName === 'webkit') {
                await expect(getExtensionLink).not.toBeVisible();
                await expect(downloadButtonMac).toBeVisible();
                await expect(downloadButtonWin).not.toBeVisible();
            } else {
                await expect(getExtensionLink).not.toBeVisible();
                await expect(downloadButtonMac).not.toBeVisible();
                await expect(downloadButtonWin).toBeVisible();
            }
        });
    }
);
