/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/new/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test('Download Firefox (Windows, macOS)', async ({
            page,
            browserName
        }) => {
            const downloadButton = page.getByTestId('download-button-thanks');
            const downloadFeaturesButton =
                page.getByTestId('download-features');
            const downloadDiscoverButton =
                page.getByTestId('download-discover');

            await openPage(url, page, browserName);

            // Assert download buttons are visible.
            await expect(downloadButton).toBeVisible();
            await expect(downloadFeaturesButton).toBeVisible();
            await expect(downloadDiscoverButton).toBeVisible();

            // Click primary download button.
            await downloadButton.click();
            await page.waitForURL('**/firefox/download/thanks/', {
                waitUntil: 'commit'
            });

            // Assert /thanks/ page triggers file download.
            const download = await page.waitForEvent('download');
            const downloadURL = download.url();

            expect(downloadURL).toEqual(
                expect.stringMatching(
                    /https:\/\/download-installer.cdn.mozilla.net\/|https:\/\/cdn-stage.stubattribution.nonprod.cloudops.mozgcp.net\/|https:\/\/cdn.stubdownloader.services.mozilla.com\//
                )
            );

            // Cancel download if not finished.
            await download.cancel();
        });

        test('Download Firefox (Linux)', async ({ page, browserName }) => {
            const downloadButton = page.getByTestId('download-button-thanks');
            const downloadFeaturesButton =
                page.getByTestId('download-features');
            const downloadDiscoverButton =
                page.getByTestId('download-discover');

            test.skip(
                browserName === 'webkit',
                'Safari not available on Linux'
            );

            // Set Linux UA strings.
            await page.addInitScript({
                path: `./scripts/useragent/linux/${browserName}.js`
            });
            await page.goto(url + '?automation=true');

            // Assert download buttons are visible.
            await expect(downloadButton).toBeVisible();
            await expect(downloadFeaturesButton).toBeVisible();
            await expect(downloadDiscoverButton).toBeVisible();

            // Click primary download button.
            await downloadButton.click();
            await page.waitForURL('**/firefox/download/thanks/', {
                waitUntil: 'commit'
            });

            // Assert Linux 32-bit / 64-bit choices are displayed.
            const downloadButtonLinux32 = page.getByTestId(
                'thanks-download-button-linux-32'
            );
            const downloadButtonLinux64 = page.getByTestId(
                'thanks-download-button-linux-64'
            );
            await expect(downloadButtonLinux32).toBeVisible();
            await expect(downloadButtonLinux32).toHaveAttribute(
                'href',
                /\?product=firefox-latest-ssl&os=linux/
            );
            await expect(downloadButtonLinux64).toBeVisible();
            await expect(downloadButtonLinux64).toHaveAttribute(
                'href',
                /\?product=firefox-latest-ssl&os=linux64/
            );
        });

        test('Firefox unsupported OS version messaging (Win / Mac)', async ({
            page,
            browserName
        }) => {
            const downloadButton = page.getByTestId('download-button-thanks');
            const downloadFeaturesButton =
                page.getByTestId('download-features');
            const downloadDiscoverButton =
                page.getByTestId('download-discover');

            const downloadOsxUnsupported = page.locator(
                'css=#download-button-thanks .fx-unsupported-message.mac .download-link'
            );

            const downloadWinUnsupported = page.locator(
                'css=#download-button-thanks .fx-unsupported-message.win .download-link.os_win64'
            );

            const downloadFeaturesOsxUnsupported = page.locator(
                'css=#download-features .fx-unsupported-message.mac .download-link'
            );

            const downloadFeaturesWinUnsupported = page.locator(
                'css=#download-features .fx-unsupported-message.win .download-link.os_win64'
            );

            const downloadDiscoverOsxUnsupported = page.locator(
                'css=#download-discover .fx-unsupported-message.mac .download-link'
            );

            const downloadDiscoverWinUnsupported = page.locator(
                'css=#download-discover .fx-unsupported-message.win .download-link.os_win64'
            );

            if (browserName === 'webkit') {
                // Set macOS 10.14 UA strings.
                await page.addInitScript({
                    path: `./scripts/useragent/mac-old/${browserName}.js`
                });
                await page.goto(url + '?automation=true');

                // Assert regular download buttons are not displayed.
                await expect(downloadButton).not.toBeVisible();
                await expect(downloadFeaturesButton).not.toBeVisible();
                await expect(downloadDiscoverButton).not.toBeVisible();

                // Assert Firefox ESR mac download button is displayed.
                await expect(downloadOsxUnsupported).toBeVisible();
                await expect(downloadOsxUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=osx/
                );
                await expect(downloadFeaturesOsxUnsupported).toBeVisible();
                await expect(downloadFeaturesOsxUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=osx/
                );
                await expect(downloadDiscoverOsxUnsupported).toBeVisible();
                await expect(downloadDiscoverOsxUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=osx/
                );
            } else {
                // Set Windows 8.1 UA strings (64-bit).
                await page.addInitScript({
                    path: `./scripts/useragent/win-old/${browserName}.js`
                });
                await page.goto(url + '?automation=true');

                // Assert regular download buttons are not displayed.
                await expect(downloadButton).not.toBeVisible();
                await expect(downloadFeaturesButton).not.toBeVisible();
                await expect(downloadDiscoverButton).not.toBeVisible();

                // Assert Firefox ESR windows download button is displayed.
                await expect(downloadWinUnsupported).toBeVisible();
                await expect(downloadWinUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=win/
                );
                await expect(downloadFeaturesWinUnsupported).toBeVisible();
                await expect(downloadFeaturesWinUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=win/
                );
                await expect(downloadDiscoverWinUnsupported).toBeVisible();
                await expect(downloadDiscoverWinUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=win/
                );
            }
        });
    }
);
