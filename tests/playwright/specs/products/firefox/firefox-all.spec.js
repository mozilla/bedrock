/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/all/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Firefox download button', async ({ page }) => {
            const downloadButton = page.getByTestId(
                'firefox-all-download-button'
            );
            const productSelect = page.getByTestId(
                'firefox-all-product-select'
            );
            const platformSelect = page.getByTestId(
                'firefox-all-platform-select (select_desktop_release_platform)'
            );
            const langSelect = page.getByTestId(
                'firefox-all-language-select (select_desktop_release_language)'
            );

            await productSelect.selectOption({ label: 'Firefox' });
            await platformSelect.selectOption({ label: 'Windows 64-bit' });
            await langSelect.selectOption({ label: 'English (US)' });

            // Assert download button is set to release channel / Windows 64-bit English (US).
            await expect(downloadButton).toBeVisible();
            await expect(downloadButton).toHaveAttribute(
                'href',
                /\?product=firefox-latest-ssl&os=win64&lang=en-US/
            );
        });

        test('Firefox Beta download button', async ({ page }) => {
            const downloadButton = page.getByTestId(
                'firefox-all-download-button'
            );
            const productSelect = page.getByTestId(
                'firefox-all-product-select'
            );
            const platformSelect = page.getByTestId(
                'firefox-all-platform-select (select_desktop_beta_platform)'
            );
            const langSelect = page.getByTestId(
                'firefox-all-language-select (select_desktop_beta_language)'
            );

            await productSelect.selectOption({ label: 'Firefox Beta' });
            await platformSelect.selectOption({ label: 'macOS' });
            await langSelect.selectOption({ label: 'German — Deutsch' });

            // Assert download button is set to release channel / macOS German.
            await expect(downloadButton).toBeVisible();
            await expect(downloadButton).toHaveAttribute(
                'href',
                /\?product=firefox-beta-latest-ssl&os=osx&lang=de/
            );
        });

        test('Firefox Developer download button', async ({ page }) => {
            const downloadButton = page.getByTestId(
                'firefox-all-download-button'
            );
            const productSelect = page.getByTestId(
                'firefox-all-product-select'
            );
            const platformSelect = page.getByTestId(
                'firefox-all-platform-select (select_desktop_developer_platform)'
            );
            const langSelect = page.getByTestId(
                'firefox-all-language-select (select_desktop_developer_language)'
            );

            await productSelect.selectOption({
                label: 'Firefox Developer Edition'
            });
            await platformSelect.selectOption({ label: 'Linux 64-bit' });
            await langSelect.selectOption({ label: 'English (US)' });

            // Assert download button is set to Dev Edition / Linux 64-bit English (US).
            await expect(downloadButton).toBeVisible();
            await expect(downloadButton).toHaveAttribute(
                'href',
                /\?product=firefox-devedition-latest-ssl&os=linux64&lang=en-US/
            );
        });

        test('Firefox Nightly download button', async ({ page }) => {
            const downloadButton = page.getByTestId(
                'firefox-all-download-button'
            );
            const productSelect = page.getByTestId(
                'firefox-all-product-select'
            );
            const platformSelect = page.getByTestId(
                'firefox-all-platform-select (select_desktop_nightly_platform)'
            );
            const langSelect = page.getByTestId(
                'firefox-all-language-select (select_desktop_nightly_language)'
            );

            await productSelect.selectOption({ label: 'Firefox Nightly' });
            await platformSelect.selectOption({ label: 'Windows 32-bit' });
            await langSelect.selectOption({ label: 'German — Deutsch' });

            // Assert download button is set to Nightly / Windows 32-bit German.
            await expect(downloadButton).toBeVisible();
            await expect(downloadButton).toHaveAttribute(
                'href',
                /\?product=firefox-nightly-latest-l10n-ssl&os=win&lang=de/
            );
        });

        test('Firefox ESR download button', async ({ page }) => {
            const downloadButton = page.getByTestId(
                'firefox-all-download-button'
            );
            const productSelect = page.getByTestId(
                'firefox-all-product-select'
            );
            const platformSelect = page.getByTestId(
                'firefox-all-platform-select (select_desktop_esr_platform)'
            );
            const langSelect = page.getByTestId(
                'firefox-all-language-select (select_desktop_esr_language)'
            );

            await productSelect.selectOption({
                label: 'Firefox Extended Support Release'
            });
            await platformSelect.selectOption({ label: 'Linux 32-bit' });
            await langSelect.selectOption({ label: 'English (US)' });

            // Assert download button is set to ESR / Linux 32-bit English (US).
            await expect(downloadButton).toBeVisible();
            await expect(downloadButton).toHaveAttribute(
                'href',
                /\?product=firefox-esr-latest-ssl&os=linux&lang=en-US/
            );
        });

        test('Firefox Android download button', async ({ page }) => {
            const downloadButton = page.getByTestId(
                'firefox-all-android-download-button'
            );
            const productSelect = page.getByTestId(
                'firefox-all-product-select'
            );

            await productSelect.selectOption({ label: 'Firefox Android' });

            // Assert download button is set to release channel / Android Play Store.
            await expect(downloadButton).toBeVisible();
            await expect(downloadButton).toHaveAttribute(
                'href',
                /^https:\/\/play.google.com\/store\/apps\/details\?id=org.mozilla.firefox/
            );
        });

        test('Firefox Android Beta download button', async ({ page }) => {
            const downloadButton = page.getByTestId(
                'firefox-all-android-beta-download-button'
            );
            const productSelect = page.getByTestId(
                'firefox-all-product-select'
            );

            await productSelect.selectOption({ label: 'Firefox Android Beta' });

            // Assert download button is set to Beta channel / Android Play Store.
            await expect(downloadButton).toBeVisible();
            await expect(downloadButton).toHaveAttribute(
                'href',
                /^https:\/\/play.google.com\/store\/apps\/details\?id=org.mozilla.firefox_beta/
            );
        });

        test('Firefox Android Nightly download button', async ({ page }) => {
            const downloadButton = page.getByTestId(
                'firefox-all-android-nightly-download-button'
            );
            const productSelect = page.getByTestId(
                'firefox-all-product-select'
            );

            await productSelect.selectOption({
                label: 'Firefox Android Nightly'
            });

            // Assert download button is set to Nightly channel / Android Play Store.
            await expect(downloadButton).toBeVisible();
            await expect(downloadButton).toHaveAttribute(
                'href',
                /^https:\/\/play.google.com\/store\/apps\/details\?id=org.mozilla.fenix/
            );
        });

        test('Firefox iOS download button', async ({ page }) => {
            const downloadButton = page.getByTestId(
                'firefox-all-ios-download-button'
            );
            const productSelect = page.getByTestId(
                'firefox-all-product-select'
            );

            await productSelect.selectOption({ label: 'Firefox iOS' });

            // Assert download button is set to iOS App Store.
            await expect(downloadButton).toBeVisible();
            await expect(downloadButton).toHaveAttribute(
                'href',
                /^https:\/\/apps.apple.com\/app\/apple-store\/id989804926/
            );
        });
    }
);
