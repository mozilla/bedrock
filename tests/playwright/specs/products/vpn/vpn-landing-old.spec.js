/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/de/products/vpn/?xv=legacy';
const availableCountries = ['us', 'ca', 'gb', 'de', 'fr'];
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
                    await openPage(url + `&geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnNavButton = page.getByTestId(
                        'get-mozilla-vpn-nav-button'
                    );
                    const getVpnPrimaryButton = page.getByTestId(
                        'get-mozilla-vpn-primary-button'
                    );
                    const getVpnTwelveMonthButton = page.getByTestId(
                        'get-mozilla-vpn-12-month-button'
                    );
                    const getVpnMonthlyButton = page.getByTestId(
                        'get-mozilla-vpn-monthly-button'
                    );
                    const getVpnSecondaryButton = page.getByTestId(
                        'get-mozilla-vpn-secondary-button'
                    );
                    const getVpnFooterButton = page.getByTestId(
                        'get-mozilla-vpn-footer-button'
                    );

                    const waitlistNavButton = page.getByTestId(
                        'join-waitlist-nav-button'
                    );
                    const waitlistPrimaryButton = page.getByTestId(
                        'join-waitlist-primary-button'
                    );
                    const waitlistSecondaryButton = page.getByTestId(
                        'join-waitlist-secondary-button'
                    );
                    const waitlistFooterButton = page.getByTestId(
                        'join-waitlist-footer-button'
                    );

                    // Assert Get Mozilla VPN buttons are displayed.
                    await expect(getVpnNavButton).toBeVisible();
                    await expect(getVpnPrimaryButton).toBeVisible();
                    await expect(getVpnTwelveMonthButton).toBeVisible();
                    await expect(getVpnMonthlyButton).toBeVisible();
                    await expect(getVpnSecondaryButton).toBeVisible();
                    await expect(getVpnFooterButton).toBeVisible();

                    // Assert Join Waitlist buttons are not displayed.
                    await expect(waitlistPrimaryButton).not.toBeVisible();
                    await expect(waitlistNavButton).not.toBeVisible();
                    await expect(waitlistSecondaryButton).not.toBeVisible();
                    await expect(waitlistFooterButton).not.toBeVisible();
                });
            });
        }

        for (const country of unavailableCountries) {
            test.describe('VPN not available', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(url + `&geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnNavButton = page.getByTestId(
                        'get-mozilla-vpn-nav-button'
                    );
                    const getVpnPrimaryButton = page.getByTestId(
                        'get-mozilla-vpn-primary-button'
                    );
                    const getVpnTwelveMonthButton = page.getByTestId(
                        'get-mozilla-vpn-12-month-button'
                    );
                    const getVpnMonthlyButton = page.getByTestId(
                        'get-mozilla-vpn-monthly-button'
                    );
                    const getVpnSecondaryButton = page.getByTestId(
                        'get-mozilla-vpn-secondary-button'
                    );
                    const getVpnFooterButton = page.getByTestId(
                        'get-mozilla-vpn-footer-button'
                    );

                    const waitlistNavButton = page.getByTestId(
                        'join-waitlist-nav-button'
                    );
                    const waitlistPrimaryButton = page.getByTestId(
                        'join-waitlist-primary-button'
                    );
                    const waitlistSecondaryButton = page.getByTestId(
                        'join-waitlist-secondary-button'
                    );
                    const waitlistFooterButton = page.getByTestId(
                        'join-waitlist-footer-button'
                    );

                    // Assert Join Waitlist buttons are displayed.
                    await expect(waitlistNavButton).toBeVisible();
                    await expect(waitlistPrimaryButton).toBeVisible();
                    await expect(waitlistSecondaryButton).toBeVisible();
                    await expect(waitlistFooterButton).toBeVisible();

                    // Assert Get Mozilla VPN buttons are not displayed.
                    await expect(getVpnNavButton).not.toBeVisible();
                    await expect(getVpnPrimaryButton).not.toBeVisible();
                    await expect(getVpnTwelveMonthButton).not.toBeVisible();
                    await expect(getVpnMonthlyButton).not.toBeVisible();
                    await expect(getVpnSecondaryButton).not.toBeVisible();
                    await expect(getVpnFooterButton).not.toBeVisible();
                });
            });
        }
    }
);
