/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/channel/desktop/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test('Download Firefox Beta / DevEdition / Nightly (Windows, macOS)', async ({
            page,
            browserName
        }) => {
            const win64BetaDownload = page.getByTestId(
                'desktop-beta-download-win64'
            );
            const winDevDownload = page.getByTestId(
                'desktop-developer-download-win'
            );
            const winNightlyDownload = page.getByTestId(
                'desktop-nightly-download-win'
            );
            const osxBetaDownload = page.getByTestId(
                'desktop-beta-download-osx'
            );
            const osxDevDownload = page.getByTestId(
                'desktop-developer-download-osx'
            );
            const osxNightlyDownload = page.getByTestId(
                'desktop-nightly-download-osx'
            );

            await openPage(url, page, browserName);

            if (browserName === 'webkit') {
                // Assert macOS download buttons are displayed.
                await expect(osxBetaDownload).toBeVisible();
                await expect(osxBetaDownload).toHaveAttribute(
                    'href',
                    /\?product=firefox-beta-latest-ssl&os=osx/
                );
                await expect(osxDevDownload).toBeVisible();
                await expect(osxDevDownload).toHaveAttribute(
                    'href',
                    /\?product=firefox-devedition-latest-ssl&os=osx/
                );
                await expect(osxNightlyDownload).toBeVisible();
                await expect(osxNightlyDownload).toHaveAttribute(
                    'href',
                    /\?product=firefox-nightly-latest-ssl&os=osx/
                );

                // Assert Windows download buttons are not displayed.
                await expect(win64BetaDownload).not.toBeVisible();
                await expect(winDevDownload).not.toBeVisible();
                await expect(winNightlyDownload).not.toBeVisible();
            } else {
                /**
                 * Assert Windows download buttons are displayed.
                 * Note: we serve the full installer for Firefox Beta on Windows.
                 * See https://github.com/mozilla/bedrock/issues/9836
                 * and https://github.com/mozilla/bedrock/issues/10194
                 */
                await expect(win64BetaDownload).toBeVisible();
                await expect(win64BetaDownload).toHaveAttribute(
                    'href',
                    /\?product=firefox-beta-latest-ssl&os=win64/
                );
                await expect(winDevDownload).toBeVisible();
                await expect(winDevDownload).toHaveAttribute(
                    'href',
                    /\?product=firefox-devedition-stub&os=win/
                );
                await expect(winNightlyDownload).toBeVisible();
                await expect(winNightlyDownload).toHaveAttribute(
                    'href',
                    /\?product=firefox-nightly-stub&os=win/
                );

                // Assert macOS download buttons are not displayed.
                await expect(osxBetaDownload).not.toBeVisible();
                await expect(osxDevDownload).not.toBeVisible();
                await expect(osxNightlyDownload).not.toBeVisible();
            }
        });

        test('Download Firefox Beta / DevEdition / Nightly (Linux)', async ({
            page,
            browserName
        }) => {
            const linuxBetaDownload = page.getByTestId(
                'desktop-beta-download-linux'
            );
            const linux64BetaDownload = page.getByTestId(
                'desktop-beta-download-linux64'
            );
            const linuxDevDownload = page.getByTestId(
                'desktop-developer-download-linux'
            );
            const linux64DevDownload = page.getByTestId(
                'desktop-developer-download-linux64'
            );
            const linuxNightlyDownload = page.getByTestId(
                'desktop-nightly-download-linux'
            );
            const linux64NightlyDownload = page.getByTestId(
                'desktop-nightly-download-linux64'
            );

            const win64BetaDownload = page.getByTestId(
                'desktop-beta-download-win64'
            );
            const winDevDownload = page.getByTestId(
                'desktop-developer-download-win'
            );
            const winNightlyDownload = page.getByTestId(
                'desktop-nightly-download-win'
            );
            const osxBetaDownload = page.getByTestId(
                'desktop-beta-download-osx'
            );
            const osxDevDownload = page.getByTestId(
                'desktop-developer-download-osx'
            );
            const osxNightlyDownload = page.getByTestId(
                'desktop-nightly-download-osx'
            );

            test.skip(
                browserName === 'webkit',
                'Safari not available on Linux'
            );

            // Set Linux UA strings.
            await page.addInitScript({
                path: `./scripts/useragent/linux/${browserName}.js`
            });
            await page.goto(url + '?automation=true');

            // Assert Linux download buttons are displayed.
            await expect(linuxBetaDownload).toBeVisible();
            await expect(linuxBetaDownload).toHaveAttribute(
                'href',
                /\?product=firefox-beta-latest-ssl&os=linux/
            );
            await expect(linux64BetaDownload).toBeVisible();
            await expect(linux64BetaDownload).toHaveAttribute(
                'href',
                /\?product=firefox-beta-latest-ssl&os=linux64/
            );
            await expect(linuxDevDownload).toBeVisible();
            await expect(linuxDevDownload).toHaveAttribute(
                'href',
                /\?product=firefox-devedition-latest-ssl&os=linux/
            );
            await expect(linux64DevDownload).toBeVisible();
            await expect(linux64DevDownload).toHaveAttribute(
                'href',
                /\?product=firefox-devedition-latest-ssl&os=linux64/
            );
            await expect(linuxNightlyDownload).toBeVisible();
            await expect(linuxNightlyDownload).toHaveAttribute(
                'href',
                /\?product=firefox-nightly-latest-ssl&os=linux/
            );
            await expect(linux64NightlyDownload).toBeVisible();
            await expect(linux64NightlyDownload).toHaveAttribute(
                'href',
                /\?product=firefox-nightly-latest-ssl&os=linux64/
            );

            // Assert Windows / macOS download buttons are not displayed.
            await expect(win64BetaDownload).not.toBeVisible();
            await expect(winDevDownload).not.toBeVisible();
            await expect(winNightlyDownload).not.toBeVisible();
            await expect(osxBetaDownload).not.toBeVisible();
            await expect(osxDevDownload).not.toBeVisible();
            await expect(osxNightlyDownload).not.toBeVisible();
        });

        test('Firefox unsupported OS version messaging (Win / Mac)', async ({
            page,
            browserName
        }) => {
            const win64BetaDownload = page.getByTestId(
                'desktop-beta-download-win64'
            );
            const winDevDownload = page.getByTestId(
                'desktop-developer-download-win'
            );
            const winNightlyDownload = page.getByTestId(
                'desktop-nightly-download-win'
            );
            const osxBetaDownload = page.getByTestId(
                'desktop-beta-download-osx'
            );
            const osxDevDownload = page.getByTestId(
                'desktop-developer-download-osx'
            );
            const osxNightlyDownload = page.getByTestId(
                'desktop-nightly-download-osx'
            );

            const betaDownloadOsxUnsupported = page.locator(
                'css=.download-button-beta .fx-unsupported-message.mac .download-link'
            );
            const devDownloadOsxUnsupported = page.locator(
                'css=.download-button-alpha .fx-unsupported-message.mac .download-link'
            );
            const nightlyDownloadOsxUnsupported = page.locator(
                'css=.download-button-nightly .fx-unsupported-message.mac .download-link'
            );
            const betaDownloadWinUnsupported = page.locator(
                'css=.download-button-beta .fx-unsupported-message.win .download-link.os_win64'
            );
            const devDownloadWinUnsupported = page.locator(
                'css=.download-button-alpha .fx-unsupported-message.win .download-link.os_win64'
            );
            const nightlyDownloadWinUnsupported = page.locator(
                'css=.download-button-nightly .fx-unsupported-message.win .download-link.os_win64'
            );

            if (browserName === 'webkit') {
                // Set macOS 10.14 UA strings.
                await page.addInitScript({
                    path: `./scripts/useragent/mac-old/${browserName}.js`
                });
                await page.goto(url + '?automation=true');

                // Assert ESR button is displayed instead of Firefox Beta button.
                await expect(betaDownloadOsxUnsupported).toBeVisible();
                await expect(betaDownloadOsxUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=osx/
                );
                await expect(osxBetaDownload).not.toBeVisible();

                // Assert ESR button is displayed instead of Firefox Developer Edition button.
                await expect(devDownloadOsxUnsupported).toBeVisible();
                await expect(devDownloadOsxUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=osx/
                );
                await expect(osxDevDownload).not.toBeVisible();

                // Assert ESR button is displayed instead of Firefox Nightly button.
                await expect(nightlyDownloadOsxUnsupported).toBeVisible();
                await expect(nightlyDownloadOsxUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=osx/
                );
                await expect(osxNightlyDownload).not.toBeVisible();
            } else {
                // Set Windows 8.1 UA string (64-bit).
                await page.addInitScript({
                    path: `./scripts/useragent/win-old/${browserName}.js`
                });
                await page.goto(url + '?automation=true');

                // Assert ESR button is displayed instead of Firefox Beta 64-bit button.
                await expect(betaDownloadWinUnsupported).toBeVisible();
                await expect(betaDownloadWinUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=win64/
                );
                await expect(win64BetaDownload).not.toBeVisible();

                // Assert ESR button is displayed instead of Firefox Developer Edition button.
                await expect(devDownloadWinUnsupported).toBeVisible();
                await expect(devDownloadWinUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=win64/
                );
                await expect(winDevDownload).not.toBeVisible();

                // Assert ESR button is displayed instead of Firefox Nightly button.
                await expect(nightlyDownloadWinUnsupported).toBeVisible();
                await expect(nightlyDownloadWinUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=win64/
                );
                await expect(winNightlyDownload).not.toBeVisible();
            }
        });

        test('Newsletter submit success', async ({ page, browserName }) => {
            const newsletterForm = page.getByTestId('newsletter-form');
            const newsletterSubmitButton = page.getByTestId(
                'newsletter-submit-button'
            );
            const newsletterEmailInput = page.getByTestId(
                'newsletter-email-input'
            );
            const newsletterPrivacyCheckbox = page.getByTestId(
                'newsletter-privacy-checkbox'
            );
            const newsletterThanksMessage = page.getByTestId(
                'newsletter-thanks-message'
            );

            await openPage(url, page, browserName);

            // expand form before running test
            await newsletterSubmitButton.click();

            await newsletterEmailInput.fill('success@example.com');
            await newsletterPrivacyCheckbox.click();
            await newsletterSubmitButton.click();
            await expect(newsletterForm).not.toBeVisible();
            await expect(newsletterThanksMessage).toBeVisible();
        });

        test('Newsletter submit failure', async ({ page, browserName }) => {
            const newsletterSubmitButton = page.getByTestId(
                'newsletter-submit-button'
            );
            const newsletterEmailInput = page.getByTestId(
                'newsletter-email-input'
            );
            const newsletterPrivacyCheckbox = page.getByTestId(
                'newsletter-privacy-checkbox'
            );
            const newsletterThanksMessage = page.getByTestId(
                'newsletter-thanks-message'
            );
            const newsletterErrorMessage = page.getByTestId(
                'newsletter-error-message'
            );

            await openPage(url, page, browserName);

            // expand form before running test
            await newsletterSubmitButton.click();

            await newsletterEmailInput.fill('failure@example.com');
            await newsletterPrivacyCheckbox.click();
            await newsletterSubmitButton.click();
            await expect(newsletterErrorMessage).toBeVisible();
            await expect(newsletterThanksMessage).not.toBeVisible();
        });
    }
);
