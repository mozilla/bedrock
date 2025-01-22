/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../scripts/open-page');
const url = '/en-US/firefox/';

test.describe(
    `${url} footer (mobile)`,
    {
        tag: '@mozorg'
    },
    () => {
        test.use({ viewport: { width: 360, height: 780 } });

        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Footer language change', async ({ page }) => {
            const languageSelect = page.getByTestId('footer-language-select');

            // Assert default language is English
            await expect(languageSelect).toHaveValue('en-US');

            // Change page language from /en-US/ to /de/
            await languageSelect.selectOption('de');
            await page.waitForURL('**/de/firefox/?automation=true', {
                waitUntil: 'commit'
            });

            // Assert page language is now German
            await expect(
                page.getByTestId('footer-language-select')
            ).toHaveValue('de');
        });
    }
);
