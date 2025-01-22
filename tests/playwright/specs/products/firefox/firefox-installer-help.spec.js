/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/installer-help/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test('Download Firefox (Windows)', async ({ page, browserName }) => {
            const downloadButtonRelease = page.getByTestId(
                'download-button-desktop-release-win'
            );
            const downloadButtonBeta = page.getByTestId(
                'download-button-desktop-beta-win64'
            );
            const downloadButtonDeveloper = page.getByTestId(
                'download-button-desktop-alpha-win'
            );
            const downloadButtonNightly = page.getByTestId(
                'download-button-desktop-nightly-win'
            );

            test.skip(
                browserName === 'webkit',
                'Safari not available on Windows'
            );

            await openPage(url + '?channel=release', page, browserName);

            // Assert Windows release channel download button is displayed.
            await expect(downloadButtonRelease).toBeVisible();
            await expect(downloadButtonRelease).toHaveAttribute(
                'href',
                /\?product=firefox-latest-ssl&os=win/
            );

            // Assert download buttons for other channels are not displayed.
            await expect(downloadButtonBeta).not.toBeVisible();
            await expect(downloadButtonDeveloper).not.toBeVisible();
            await expect(downloadButtonNightly).not.toBeVisible();
        });

        test('Download Firefox Beta (Windows)', async ({
            page,
            browserName
        }) => {
            const downloadButtonRelease = page.getByTestId(
                'download-button-desktop-release-win'
            );
            const downloadButtonBeta = page.getByTestId(
                'download-button-desktop-beta-win64'
            );
            const downloadButtonDeveloper = page.getByTestId(
                'download-button-desktop-alpha-win'
            );
            const downloadButtonNightly = page.getByTestId(
                'download-button-desktop-nightly-win'
            );

            test.skip(
                browserName === 'webkit',
                'Safari not available on Windows'
            );

            await openPage(url + '?channel=beta', page, browserName);

            // Assert Windows beta channel download button is displayed.
            await expect(downloadButtonBeta).toBeVisible();
            await expect(downloadButtonBeta).toHaveAttribute(
                'href',
                /\?product=firefox-beta-latest-ssl&os=win/
            );

            // Assert download buttons for other channels are not displayed.
            await expect(downloadButtonRelease).not.toBeVisible();
            await expect(downloadButtonDeveloper).not.toBeVisible();
            await expect(downloadButtonNightly).not.toBeVisible();
        });

        test('Download Firefox Developer (Windows)', async ({
            page,
            browserName
        }) => {
            const downloadButtonRelease = page.getByTestId(
                'download-button-desktop-release-win'
            );
            const downloadButtonBeta = page.getByTestId(
                'download-button-desktop-beta-win64'
            );
            const downloadButtonDeveloper = page.getByTestId(
                'download-button-desktop-alpha-win'
            );
            const downloadButtonNightly = page.getByTestId(
                'download-button-desktop-nightly-win'
            );

            test.skip(
                browserName === 'webkit',
                'Safari not available on Windows'
            );

            await openPage(url + '?channel=aurora', page, browserName);

            // Assert Windows developer channel download button is displayed.
            await expect(downloadButtonDeveloper).toBeVisible();
            await expect(downloadButtonDeveloper).toHaveAttribute(
                'href',
                /\?product=firefox-devedition-latest-ssl&os=win/
            );

            // Assert download buttons for other channels are not displayed.
            await expect(downloadButtonRelease).not.toBeVisible();
            await expect(downloadButtonBeta).not.toBeVisible();
            await expect(downloadButtonNightly).not.toBeVisible();
        });

        test('Download Firefox Nightly (Windows)', async ({
            page,
            browserName
        }) => {
            const downloadButtonRelease = page.getByTestId(
                'download-button-desktop-release-win'
            );
            const downloadButtonBeta = page.getByTestId(
                'download-button-desktop-beta-win64'
            );
            const downloadButtonDeveloper = page.getByTestId(
                'download-button-desktop-alpha-win'
            );
            const downloadButtonNightly = page.getByTestId(
                'download-button-desktop-nightly-win'
            );

            test.skip(
                browserName === 'webkit',
                'Safari not available on Windows'
            );

            await openPage(url + '?channel=nightly', page, browserName);

            // Assert Windows nightly channel download button is displayed.
            await expect(downloadButtonNightly).toBeVisible();
            await expect(downloadButtonNightly).toHaveAttribute(
                'href',
                /\?product=firefox-nightly-latest-ssl&os=win/
            );

            // Assert download buttons for other channels are not displayed.
            await expect(downloadButtonRelease).not.toBeVisible();
            await expect(downloadButtonBeta).not.toBeVisible();
            await expect(downloadButtonDeveloper).not.toBeVisible();
        });
    }
);
