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

            if (browserName === 'webkit') {
                const downloadButtonMac = page.getByTestId(
                    'download-button-desktop-release-osx'
                );
                await expect(downloadButtonMac).toBeVisible();
            } else if (browserName === 'chromium') {
                const downloadButtonWin = page.getByTestId(
                    'download-button-desktop-release-win'
                );
                await expect(downloadButtonWin).toBeVisible();
            } else if (browserName === 'firefox') {
                const defaultMessaging = page.getByTestId(
                    'firefox-not-default-message'
                );
                await expect(defaultMessaging).toBeVisible();
            }
        });
    }
);
