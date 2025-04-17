/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/set-as-default/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Click set Firefox as default', async ({ page, browserName }) => {
            const defaultButton = page.getByTestId('button-set-as-default');
            await expect(defaultButton).toBeVisible();
            await defaultButton.click();
            await page.waitForURL('**/firefox/set-as-default/thanks/', {
                waitUntil: 'commit'
            });

            const downloadButtonMac = page.getByTestId(
                'download-button-desktop-release-osx'
            );
            const downloadButtonWin = page.getByTestId(
                'download-button-desktop-release-win'
            );
            const defaultMessaging = page.getByTestId(
                'firefox-not-default-message'
            );

            if (browserName === 'webkit') {
                await expect(downloadButtonMac).toBeVisible();
                await expect(downloadButtonWin).not.toBeVisible();
                await expect(defaultMessaging).not.toBeVisible();
            } else if (browserName === 'chromium') {
                await expect(downloadButtonWin).toBeVisible();
                await expect(downloadButtonMac).not.toBeVisible();
                await expect(defaultMessaging).not.toBeVisible();
            } else if (browserName === 'firefox') {
                await expect(defaultMessaging).toBeVisible();
                await expect(downloadButtonWin).not.toBeVisible();
                await expect(downloadButtonMac).not.toBeVisible();
            }
        });
    }
);
