/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/products/vpn/pricing/';
const availableCountries = ['us', 'ca', 'gb', 'de', 'fr'];
const mobileOnlyCountries = ['au', 'in', 'mx', 'ua'];
const androidOnlyCountries = ['br', 'ma'];
const unavailableCountries = ['cn'];

test.describe(
    `${url} page`,
    {
        tag: '@vpn'
    },
    () => {
        for (const country of availableCountries) {
            test.describe('VPN available', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(url + `?geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnTwelveMonthButton = page.getByTestId(
                        'get-mozilla-vpn-12-month-button'
                    );
                    const getVpnMonthlyButton = page.getByTestId(
                        'get-mozilla-vpn-monthly-button'
                    );
                    const getVpnAppStorebutton = page.getByTestId(
                        'get-vpn-ios-app-store'
                    );
                    const getVpnPlayStorebutton = page.getByTestId(
                        'get-vpn-google-play-store'
                    );
                    const getVpnQrCode = page.getByTestId('get-vpn-qr-code');
                    const waitlistButton = page.getByTestId(
                        'join-waitlist-button'
                    );

                    // Assert Get Mozilla VPN buttons are displayed.
                    await expect(getVpnTwelveMonthButton).toBeVisible();
                    await expect(getVpnMonthlyButton).toBeVisible();

                    // Assert mobile only CTAs are not displayed.
                    await expect(getVpnAppStorebutton).not.toBeVisible();
                    await expect(getVpnPlayStorebutton).not.toBeVisible();
                    await expect(getVpnQrCode).not.toBeVisible();

                    // Assert Join Waitlist button is not displayed.
                    await expect(waitlistButton).not.toBeVisible();
                });
            });
        }

        for (const country of mobileOnlyCountries) {
            test.describe('VPN available via mobile subscription only', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(url + `?geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnTwelveMonthButton = page.getByTestId(
                        'get-mozilla-vpn-12-month-button'
                    );
                    const getVpnMonthlyButton = page.getByTestId(
                        'get-mozilla-vpn-monthly-button'
                    );
                    const getVpnAppStorebutton = page.getByTestId(
                        'get-vpn-ios-app-store'
                    );
                    const getVpnPlayStorebutton = page.getByTestId(
                        'get-vpn-google-play-store'
                    );
                    const getVpnQrCode = page.getByTestId('get-vpn-qr-code');
                    const waitlistButton = page.getByTestId(
                        'join-waitlist-button'
                    );

                    // Assert mobile only CTAs are displayed.
                    await expect(getVpnAppStorebutton).toBeVisible();
                    await expect(getVpnPlayStorebutton).toBeVisible();
                    await expect(getVpnQrCode).toBeVisible();

                    // Assert desktop FxA links are not displayed.
                    await expect(getVpnTwelveMonthButton).not.toBeVisible();
                    await expect(getVpnMonthlyButton).not.toBeVisible();

                    // Assert Join Waitlist button is not displayed.
                    await expect(waitlistButton).not.toBeVisible();
                });
            });
        }

        for (const country of androidOnlyCountries) {
            test.describe('VPN available via android subscription only', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(url + `?geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnTwelveMonthButton = page.getByTestId(
                        'get-mozilla-vpn-12-month-button'
                    );
                    const getVpnMonthlyButton = page.getByTestId(
                        'get-mozilla-vpn-monthly-button'
                    );
                    const getVpnAppStorebutton = page.getByTestId(
                        'get-vpn-ios-app-store'
                    );
                    const getVpnPlayStorebutton = page.getByTestId(
                        'get-vpn-google-play-store'
                    );
                    const getVpnQrCode = page.getByTestId('get-vpn-qr-code');
                    const waitlistButton = page.getByTestId(
                        'join-waitlist-button'
                    );

                    // Assert only android CTAs are displayed.
                    await expect(getVpnAppStorebutton).not.toBeVisible();
                    await expect(getVpnPlayStorebutton).toBeVisible();
                    await expect(getVpnQrCode).toBeVisible();

                    // Assert desktop FxA links are not displayed.
                    await expect(getVpnTwelveMonthButton).not.toBeVisible();
                    await expect(getVpnMonthlyButton).not.toBeVisible();

                    // Assert Join Waitlist button is not displayed.
                    await expect(waitlistButton).not.toBeVisible();
                });
            });
        }

        for (const country of unavailableCountries) {
            test.describe('VPN not available', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(url + `?geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnTwelveMonthButton = page.getByTestId(
                        'get-mozilla-vpn-12-month-button'
                    );
                    const getVpnMonthlyButton = page.getByTestId(
                        'get-mozilla-vpn-monthly-button'
                    );
                    const getVpnAppStorebutton = page.getByTestId(
                        'get-vpn-ios-app-store'
                    );
                    const getVpnPlayStorebutton = page.getByTestId(
                        'get-vpn-google-play-store'
                    );
                    const getVpnQrCode = page.getByTestId('get-vpn-qr-code');
                    const waitlistButton = page.getByTestId(
                        'join-waitlist-button'
                    );

                    // Assert Join Waitlist button is displayed.
                    await expect(waitlistButton).toBeVisible();

                    // Assert mobile only CTAs are not displayed.
                    await expect(getVpnAppStorebutton).not.toBeVisible();
                    await expect(getVpnPlayStorebutton).not.toBeVisible();
                    await expect(getVpnQrCode).not.toBeVisible();

                    // Assert Get Mozilla VPN buttons are not displayed.
                    await expect(getVpnTwelveMonthButton).not.toBeVisible();
                    await expect(getVpnMonthlyButton).not.toBeVisible();
                });
            });
        }
    }
);
