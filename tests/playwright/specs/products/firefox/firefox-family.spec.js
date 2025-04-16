/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/family/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Call to action is displayed', async ({ page, browserName }) => {
            const downloadButton = page.getByTestId('download-button-thanks');
            const setAsDefaultButton = page.getByTestId(
                'button-set-as-default'
            );
            const pdfButton = page.getByTestId('button-download-pdf');

            if (browserName === 'firefox') {
                await expect(downloadButton).not.toBeVisible();
                await expect(setAsDefaultButton).toBeVisible();
            } else {
                await expect(downloadButton).toBeVisible();
                await expect(setAsDefaultButton).not.toBeVisible();
            }

            await expect(pdfButton).toBeVisible();
        });

        // fixme() can be removed once https://github.com/mozilla/bedrock/issues/16193 is resolved.
        test.fixme('Dad jokes banner can be dismissed', async ({ page }) => {
            const dadJokesBanner = page.getByTestId('dad-jokes-banner');
            const bannerCloseButton = page.getByTestId('button-banner-close');

            await expect(dadJokesBanner).not.toBeVisible();
            await page.mouse.wheel(0, 10);
            await expect(dadJokesBanner).toBeVisible();
            await bannerCloseButton.click();
            await expect(dadJokesBanner).not.toBeVisible();
        });
    }
);
