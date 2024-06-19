/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/developer/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test('Download DevEdition (Windows, macOS)', async ({
            page,
            browserName
        }) => {
            const introDownloadWin = page.getByTestId('intro-download-win');
            const introDownloadOsx = page.getByTestId('intro-download-osx');
            const footerDownloadWin = page.getByTestId('footer-download-win');
            const footerDownloadOsx = page.getByTestId('footer-download-osx');

            await openPage(url, page, browserName);

            if (browserName === 'webkit') {
                // Assert macOS download button is displayed.
                await expect(introDownloadOsx).toBeVisible();
                await expect(introDownloadOsx).toHaveAttribute(
                    'href',
                    /\?product=firefox-devedition-latest-ssl&os=osx/
                );
                await expect(footerDownloadOsx).toBeVisible();
                await expect(footerDownloadOsx).toHaveAttribute(
                    'href',
                    /\?product=firefox-devedition-latest-ssl&os=osx/
                );

                // Assert Windows download button is not displayed.
                await expect(introDownloadWin).not.toBeVisible();
                await expect(footerDownloadWin).not.toBeVisible();
            } else {
                // Assert Windows download button is displayed.
                await expect(introDownloadWin).toBeVisible();
                await expect(introDownloadWin).toHaveAttribute(
                    'href',
                    /\?product=firefox-devedition-stub&os=win/
                );
                await expect(footerDownloadWin).toBeVisible();
                await expect(footerDownloadWin).toHaveAttribute(
                    'href',
                    /\?product=firefox-devedition-stub&os=win/
                );

                // Assert macOS download button is not displayed.
                await expect(introDownloadOsx).not.toBeVisible();
                await expect(footerDownloadOsx).not.toBeVisible();
            }
        });

        test('Download Firefox (Linux)', async ({ page, browserName }) => {
            const introDownloadWin = page.getByTestId('intro-download-win');
            const introDownloadOsx = page.getByTestId('intro-download-osx');
            const footerDownloadWin = page.getByTestId('footer-download-win');
            const footerDownloadOsx = page.getByTestId('footer-download-osx');
            const introDownloadLinux = page.getByTestId('intro-download-linux');
            const introDownloadLinux64 = page.getByTestId(
                'intro-download-linux64'
            );
            const footerDownloadLinux = page.getByTestId(
                'footer-download-linux'
            );
            const footerDownloadLinux64 = page.getByTestId(
                'footer-download-linux64'
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
            await expect(introDownloadLinux).toBeVisible();
            await expect(introDownloadLinux).toHaveAttribute(
                'href',
                /\?product=firefox-devedition-latest-ssl&os=linux/
            );
            await expect(introDownloadLinux64).toBeVisible();
            await expect(introDownloadLinux64).toHaveAttribute(
                'href',
                /\?product=firefox-devedition-latest-ssl&os=linux64/
            );
            await expect(footerDownloadLinux).toBeVisible();
            await expect(footerDownloadLinux).toHaveAttribute(
                'href',
                /\?product=firefox-devedition-latest-ssl&os=linux/
            );
            await expect(footerDownloadLinux64).toBeVisible();
            await expect(footerDownloadLinux64).toHaveAttribute(
                'href',
                /\?product=firefox-devedition-latest-ssl&os=linux64/
            );

            // Assert Windows / macOS download buttons are not displayed.
            await expect(introDownloadWin).not.toBeVisible();
            await expect(introDownloadOsx).not.toBeVisible();
            await expect(footerDownloadWin).not.toBeVisible();
            await expect(footerDownloadOsx).not.toBeVisible();
        });

        test('Firefox unsupported OS version messaging (Win / Mac)', async ({
            page,
            browserName
        }) => {
            const introDownloadWin = page.getByTestId('intro-download-win');
            const introDownloadOsx = page.getByTestId('intro-download-osx');
            const footerDownloadWin = page.getByTestId('footer-download-win');
            const footerDownloadOsx = page.getByTestId('footer-download-osx');

            const introDownloadWinUnsupported = page.locator(
                'css=#intro-download .fx-unsupported-message.win .download-link.os_win64'
            );

            const introDownloadOsxUnsupported = page.locator(
                'css=#intro-download .fx-unsupported-message.mac .download-link'
            );

            const footerDownloadWinUnsupported = page.locator(
                'css=#footer-download .fx-unsupported-message.win .download-link.os_win64'
            );

            const footerDownloadOsxUnsupported = page.locator(
                'css=#footer-download .fx-unsupported-message.mac .download-link'
            );

            if (browserName === 'webkit') {
                // Set macOS 10.14 UA strings.
                await page.addInitScript({
                    path: `./scripts/useragent/mac-old/${browserName}.js`
                });
                await page.goto(url + '?automation=true');

                // Assert ESR buttons are displayed instead of Firefox Dev buttons.
                await expect(introDownloadOsxUnsupported).toBeVisible();
                await expect(introDownloadOsxUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=osx/
                );
                await expect(footerDownloadOsxUnsupported).toBeVisible();
                await expect(footerDownloadOsxUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=osx/
                );

                // Assert regular download buttons are not displayed.
                await expect(introDownloadOsx).not.toBeVisible();
                await expect(footerDownloadOsx).not.toBeVisible();
            } else {
                // Set Windows 8.1 UA string (64-bit).
                await page.addInitScript({
                    path: `./scripts/useragent/win-old/${browserName}.js`
                });
                await page.goto(url + '?automation=true');

                // Assert ESR buttons are displayed instead of Firefox Dev buttons.
                await expect(introDownloadWinUnsupported).toBeVisible();
                await expect(introDownloadWinUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=win64/
                );
                await expect(footerDownloadWinUnsupported).toBeVisible();
                await expect(footerDownloadWinUnsupported).toHaveAttribute(
                    'href',
                    /\?product=firefox-esr-latest-ssl&os=win64/
                );

                // Assert regular download buttons are not displayed.
                await expect(introDownloadWin).not.toBeVisible();
                await expect(footerDownloadWin).not.toBeVisible();
            }
        });

        test('Newsletter submit success', async ({ page, browserName }) => {
            const newsletterForm = page.getByTestId('newsletter-form');
            const newsletterThanksMessage = page.getByTestId(
                'newsletter-thanks-message'
            );
            const newsletterEmailInput = page.getByTestId(
                'newsletter-email-input'
            );
            const newsletterPrivacyCheckbox = page.getByTestId(
                'newsletter-privacy-checkbox'
            );
            const newsletterSubmitButton = page.getByTestId(
                'newsletter-submit-button'
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
            const newsletterThanksMessage = page.getByTestId(
                'newsletter-thanks-message'
            );
            const newsletterErrorMessage = page.getByTestId(
                'newsletter-error-message'
            );
            const newsletterEmailInput = page.getByTestId(
                'newsletter-email-input'
            );
            const newsletterPrivacyCheckbox = page.getByTestId(
                'newsletter-privacy-checkbox'
            );
            const newsletterSubmitButton = page.getByTestId(
                'newsletter-submit-button'
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
