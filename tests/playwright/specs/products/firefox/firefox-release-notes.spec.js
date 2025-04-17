/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');

test.describe(
    '/en-US/firefox/releasenotes/ page',
    {
        tag: '@firefox'
    },
    () => {
        test.describe('Firefox release channel notes', () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(
                    '/en-US/firefox/137.0/releasenotes/',
                    page,
                    browserName
                );
            });

            test('Release download button is displayed', async ({
                page,
                browserName
            }) => {
                const downloadButtonPrimaryMac = page.getByTestId(
                    'download-release-primary-osx'
                );
                const downloadButtonSecondaryMac = page.getByTestId(
                    'download-release-secondary-osx'
                );
                const downloadButtonPrimaryWin = page.getByTestId(
                    'download-release-primary-win'
                );
                const downloadButtonSecondaryWin = page.getByTestId(
                    'download-release-secondary-win'
                );

                if (browserName === 'firefox') {
                    await expect(downloadButtonPrimaryWin).not.toBeVisible();
                    await expect(downloadButtonSecondaryWin).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                } else if (browserName === 'webkit') {
                    await expect(downloadButtonPrimaryMac).toBeVisible();
                    await expect(downloadButtonSecondaryMac).toBeVisible();
                    await expect(downloadButtonPrimaryWin).not.toBeVisible();
                    await expect(downloadButtonSecondaryWin).not.toBeVisible();
                } else {
                    await expect(downloadButtonPrimaryWin).toBeVisible();
                    await expect(downloadButtonSecondaryWin).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                }
            });
        });

        test.describe('Firefox Beta release notes', () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(
                    '/en-US/firefox/138.0beta/releasenotes/',
                    page,
                    browserName
                );
            });

            test('Beta download button is displayed', async ({
                page,
                browserName
            }) => {
                const downloadButtonPrimaryMac = page.getByTestId(
                    'download-beta-primary-osx'
                );
                const downloadButtonSecondaryMac = page.getByTestId(
                    'download-beta-secondary-osx'
                );
                const downloadButtonPrimaryWin64 = page.getByTestId(
                    'download-beta-primary-win64'
                );
                const downloadButtonSecondaryWin64 = page.getByTestId(
                    'download-beta-secondary-win64'
                );

                if (browserName === 'firefox') {
                    await expect(downloadButtonPrimaryWin64).not.toBeVisible();
                    await expect(downloadButtonSecondaryWin64).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                } else if (browserName === 'webkit') {
                    await expect(downloadButtonPrimaryMac).toBeVisible();
                    await expect(downloadButtonSecondaryMac).toBeVisible();
                    await expect(downloadButtonPrimaryWin64).not.toBeVisible();
                    await expect(
                        downloadButtonSecondaryWin64
                    ).not.toBeVisible();
                } else {
                    await expect(downloadButtonPrimaryWin64).toBeVisible();
                    await expect(downloadButtonSecondaryWin64).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                }
            });
        });

        test.describe('Firefox Nightly release notes', () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(
                    '/en-US/firefox/139.0a1/releasenotes/',
                    page,
                    browserName
                );
            });

            test('Nightly download button is displayed', async ({
                page,
                browserName
            }) => {
                const downloadButtonPrimaryMac = page.getByTestId(
                    'download-nightly-primary-osx'
                );
                const downloadButtonSecondaryMac = page.getByTestId(
                    'download-nightly-secondary-osx'
                );
                const downloadButtonPrimaryWin = page.getByTestId(
                    'download-nightly-primary-win'
                );
                const downloadButtonSecondaryWin = page.getByTestId(
                    'download-nightly-secondary-win'
                );

                if (browserName === 'firefox') {
                    await expect(downloadButtonPrimaryWin).not.toBeVisible();
                    await expect(downloadButtonSecondaryWin).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                } else if (browserName === 'webkit') {
                    await expect(downloadButtonPrimaryMac).toBeVisible();
                    await expect(downloadButtonSecondaryMac).toBeVisible();
                    await expect(downloadButtonPrimaryWin).not.toBeVisible();
                    await expect(downloadButtonSecondaryWin).not.toBeVisible();
                } else {
                    await expect(downloadButtonPrimaryWin).toBeVisible();
                    await expect(downloadButtonSecondaryWin).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                }
            });
        });

        test.describe('Firefox ESR release notes', () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(
                    '/en-US/firefox/128.9.0/releasenotes/',
                    page,
                    browserName
                );
            });

            test('ESR download button is displayed', async ({
                page,
                browserName
            }) => {
                const downloadButtonPrimaryMac = page.getByTestId(
                    'download-esr-primary-osx'
                );
                const downloadButtonSecondaryMac = page.getByTestId(
                    'download-esr-secondary-osx'
                );
                const downloadButtonPrimaryWin = page.getByTestId(
                    'download-esr-primary-win'
                );
                const downloadButtonSecondaryWin = page.getByTestId(
                    'download-esr-secondary-win'
                );

                if (browserName === 'firefox') {
                    await expect(downloadButtonPrimaryWin).not.toBeVisible();
                    await expect(downloadButtonSecondaryWin).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                } else if (browserName === 'webkit') {
                    await expect(downloadButtonPrimaryMac).toBeVisible();
                    await expect(downloadButtonSecondaryMac).toBeVisible();
                    await expect(downloadButtonPrimaryWin).not.toBeVisible();
                    await expect(downloadButtonSecondaryWin).not.toBeVisible();
                } else {
                    await expect(downloadButtonPrimaryWin).toBeVisible();
                    await expect(downloadButtonSecondaryWin).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                }
            });
        });

        test.describe('Firefox Aurora release notes', () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(
                    '/en-US/firefox/34.0a2/releasenotes/',
                    page,
                    browserName
                );
            });

            test('Firefox Developer Edition download button is displayed', async ({
                page,
                browserName
            }) => {
                const downloadButtonPrimaryMac = page.getByTestId(
                    'download-dev-edition-primary-osx'
                );
                const downloadButtonSecondaryMac = page.getByTestId(
                    'download-dev-edition-secondary-osx'
                );
                const downloadButtonPrimaryWin = page.getByTestId(
                    'download-dev-edition-primary-win'
                );
                const downloadButtonSecondaryWin = page.getByTestId(
                    'download-dev-edition-secondary-win'
                );

                if (browserName === 'firefox') {
                    await expect(downloadButtonPrimaryWin).not.toBeVisible();
                    await expect(downloadButtonSecondaryWin).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                } else if (browserName === 'webkit') {
                    await expect(downloadButtonPrimaryMac).toBeVisible();
                    await expect(downloadButtonSecondaryMac).toBeVisible();
                    await expect(downloadButtonPrimaryWin).not.toBeVisible();
                    await expect(downloadButtonSecondaryWin).not.toBeVisible();
                } else {
                    await expect(downloadButtonPrimaryWin).toBeVisible();
                    await expect(downloadButtonSecondaryWin).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                }
            });
        });

        test.describe('Firefox Developer Edition release notes', () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(
                    '/en-US/firefox/54.0a2/releasenotes/',
                    page,
                    browserName
                );
            });

            test('Firefox Developer Edition download button is displayed', async ({
                page,
                browserName
            }) => {
                const downloadButtonPrimaryMac = page.getByTestId(
                    'download-dev-edition-primary-osx'
                );
                const downloadButtonSecondaryMac = page.getByTestId(
                    'download-dev-edition-secondary-osx'
                );
                const downloadButtonPrimaryWin = page.getByTestId(
                    'download-dev-edition-primary-win'
                );
                const downloadButtonSecondaryWin = page.getByTestId(
                    'download-dev-edition-secondary-win'
                );

                if (browserName === 'firefox') {
                    await expect(downloadButtonPrimaryWin).not.toBeVisible();
                    await expect(downloadButtonSecondaryWin).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                } else if (browserName === 'webkit') {
                    await expect(downloadButtonPrimaryMac).toBeVisible();
                    await expect(downloadButtonSecondaryMac).toBeVisible();
                    await expect(downloadButtonPrimaryWin).not.toBeVisible();
                    await expect(downloadButtonSecondaryWin).not.toBeVisible();
                } else {
                    await expect(downloadButtonPrimaryWin).toBeVisible();
                    await expect(downloadButtonSecondaryWin).toBeVisible();
                    await expect(downloadButtonPrimaryMac).not.toBeVisible();
                    await expect(downloadButtonSecondaryMac).not.toBeVisible();
                }
            });
        });

        test.describe('Firefox Android release notes', () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(
                    '/en-US/firefox/android/137.0.2/releasenotes/',
                    page,
                    browserName
                );
            });

            test('Google Play Store button is displayed', async ({
                page,
                browserName
            }) => {
                const downloadButtonPrimary = page.getByTestId(
                    'download-android-primary'
                );
                const downloadButtonSecondary = page.getByTestId(
                    'download-android-secondary'
                );

                if (browserName === 'firefox') {
                    await expect(downloadButtonPrimary).not.toBeVisible();
                    await expect(downloadButtonSecondary).toBeVisible();
                } else {
                    await expect(downloadButtonPrimary).toBeVisible();
                    await expect(downloadButtonSecondary).toBeVisible();
                }
            });
        });

        test.describe('Firefox Android Beta release notes', () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(
                    '/en-US/firefox/android/68.7beta/releasenotes/',
                    page,
                    browserName
                );
            });

            test('Google Play Store button is displayed', async ({
                page,
                browserName
            }) => {
                const downloadButtonPrimary = page.getByTestId(
                    'download-android-beta-primary-android'
                );
                const downloadButtonSecondary = page.getByTestId(
                    'download-android-beta-secondary-android'
                );

                if (browserName === 'firefox') {
                    await expect(downloadButtonPrimary).not.toBeVisible();
                    await expect(downloadButtonSecondary).toBeVisible();
                } else if (browserName === 'webkit') {
                    await expect(downloadButtonPrimary).toBeVisible();
                    await expect(downloadButtonSecondary).toBeVisible();
                } else {
                    await expect(downloadButtonPrimary).toBeVisible();
                    await expect(downloadButtonSecondary).toBeVisible();
                }
            });
        });

        test.describe('Firefox Android Nightly release notes', () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(
                    '/en-US/firefox/android/54.0a2/releasenotes/',
                    page,
                    browserName
                );
            });

            test('Google Play Store button is displayed', async ({
                page,
                browserName
            }) => {
                const downloadButtonPrimary = page.getByTestId(
                    'download-android-nightly-primary-android'
                );
                const downloadButtonSecondary = page.getByTestId(
                    'download-android-nightly-secondary-android'
                );

                if (browserName === 'firefox') {
                    await expect(downloadButtonPrimary).not.toBeVisible();
                    await expect(downloadButtonSecondary).toBeVisible();
                } else if (browserName === 'webkit') {
                    await expect(downloadButtonPrimary).toBeVisible();
                    await expect(downloadButtonSecondary).toBeVisible();
                } else {
                    await expect(downloadButtonPrimary).toBeVisible();
                    await expect(downloadButtonSecondary).toBeVisible();
                }
            });
        });

        test.describe('Firefox iOS release notes', () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(
                    '/en-US/firefox/ios/25.0/releasenotes/',
                    page,
                    browserName
                );
            });

            test('Google Play Store button is displayed', async ({
                page,
                browserName
            }) => {
                const downloadButtonPrimary = page.getByTestId(
                    'download-ios-primary'
                );
                const downloadButtonSecondary = page.getByTestId(
                    'download-ios-secondary'
                );

                if (browserName === 'firefox') {
                    await expect(downloadButtonPrimary).not.toBeVisible();
                    await expect(downloadButtonSecondary).toBeVisible();
                } else if (browserName === 'webkit') {
                    await expect(downloadButtonPrimary).toBeVisible();
                    await expect(downloadButtonSecondary).toBeVisible();
                } else {
                    await expect(downloadButtonPrimary).toBeVisible();
                    await expect(downloadButtonSecondary).toBeVisible();
                }
            });
        });
    }
);
