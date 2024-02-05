/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Download Firefox desktop', async ({ page }) => {
            // Click download button.
            const downloadButton = page.getByTestId('firefox-desktop-download');
            await expect(downloadButton).toBeVisible();
            await downloadButton.click();
            await page.waitForURL('**/firefox/download/thanks/');

            // Assert /thanks/ page triggers file download.
            const download = await page.waitForEvent('download');
            const downloadURL = download.url();

            expect(downloadURL).toEqual(
                expect.stringContaining(
                    'https://download-installer.cdn.mozilla.net/pub/firefox/releases/'
                )
            );

            // Cancel download if not finished.
            await download.cancel();
        });

        test('Firefox mobile menu open / close', async ({ page }) => {
            const mobileMenuButton = page.getByTestId(
                'firefox-mobile-download-menu-button'
            );
            const androidMenuLink = page.getByTestId(
                'firefox-android-menu-link'
            );
            const iosMenuLink = page.getByTestId('firefox-ios-menu-link');

            await expect(iosMenuLink).not.toBeVisible();
            await expect(androidMenuLink).not.toBeVisible();

            // open menu
            await mobileMenuButton.click();

            // Assert Android and iOS download links are displayed.
            await expect(androidMenuLink).toBeVisible();
            await expect(androidMenuLink).toHaveAttribute(
                'href',
                /^https:\/\/play.google.com\/store\/apps\//
            );
            await expect(iosMenuLink).toBeVisible();
            await expect(iosMenuLink).toHaveAttribute(
                'href',
                /^https:\/\/apps.apple.com\/us\/app\/apple-store\//
            );

            // close menu
            await mobileMenuButton.click();

            // Assert Android and iOS download links are hidden.
            await expect(iosMenuLink).not.toBeVisible();
            await expect(androidMenuLink).not.toBeVisible();
        });

        test('Account form sign up', async ({ page }) => {
            const emailQueryString = /&email=success%40example.com/;
            const accountButton = page.getByTestId('fxa-form-submit-button');
            const emailField = page.getByTestId('fxa-form-email-field');

            await emailField.fill('success@example.com');
            await accountButton.click();
            await page.waitForURL(emailQueryString, {
                waitUntil: 'commit'
            });
            await expect(page).toHaveURL(emailQueryString);
        });
    }
);
