/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/channel/android/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Download Firefox Beta / Nightly (Android)', async ({ page }) => {
            const androidBetaDownload = page.getByTestId(
                'android-beta-download-android'
            );
            const androidNightlyDownload = page.getByTestId(
                'android-nightly-download-android'
            );

            // Assert Android Beta download button is displayed.
            await expect(androidBetaDownload).toBeVisible();
            await expect(androidBetaDownload).toHaveAttribute(
                'href',
                /^https:\/\/play.google.com\/store\/apps\/details\?id=org.mozilla.firefox_beta/
            );

            // Assert Android Nightly download button is displayed.
            await expect(androidNightlyDownload).toBeVisible();
            await expect(androidNightlyDownload).toHaveAttribute(
                'href',
                /^https:\/\/play.google.com\/store\/apps\/details\?id=org.mozilla.fenix/
            );
        });
    }
);
