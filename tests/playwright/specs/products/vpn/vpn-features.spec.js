/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/products/vpn/features/';
const availableCountries = [
    'us',
    'ca',
    'gb',
    'de',
    'fr',
    'au',
    'in',
    'mx',
    'ua'
];
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
                    const getVpnPostConvenientButton = page.getByTestId(
                        'get-mozilla-vpn-post-convenient-button'
                    );
                    const getVpnPostSecureButton = page.getByTestId(
                        'get-mozilla-vpn-post-secure-button'
                    );
                    const getVpnPostFlexibleButton = page.getByTestId(
                        'get-mozilla-vpn-post-flexible-button'
                    );
                    const getVpnFooterButton = page.getByTestId(
                        'get-mozilla-vpn-footer-button'
                    );

                    const joinWaitlistConvenientButton = page.getByTestId(
                        'join-waitlist-post-convenient-button'
                    );
                    const joinWaitlistPostSecureButton = page.getByTestId(
                        'join-waitlist-post-secure-button'
                    );
                    const joinWaitlistPostFlexibleButton = page.getByTestId(
                        'join-waitlist-post-flexible-button'
                    );
                    const joinWaitlistFooterButton = page.getByTestId(
                        'join-waitlist-footer-button'
                    );

                    // Assert Get Mozilla VPN buttons are displayed.
                    await expect(getVpnPostConvenientButton).toBeVisible();
                    await expect(getVpnPostSecureButton).toBeVisible();
                    await expect(getVpnPostFlexibleButton).toBeVisible();
                    await expect(getVpnFooterButton).toBeVisible();

                    // Assert Join Waitlist buttons are not displayed.
                    await expect(
                        joinWaitlistConvenientButton
                    ).not.toBeVisible();
                    await expect(
                        joinWaitlistPostSecureButton
                    ).not.toBeVisible();
                    await expect(
                        joinWaitlistPostFlexibleButton
                    ).not.toBeVisible();
                    await expect(joinWaitlistFooterButton).not.toBeVisible();
                });
            });
        }

        for (const country of unavailableCountries) {
            test.describe('VPN not available', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(url + `?geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnPostConvenientButton = page.getByTestId(
                        'get-mozilla-vpn-post-convenient-button'
                    );
                    const getVpnPostSecureButton = page.getByTestId(
                        'get-mozilla-vpn-post-secure-button'
                    );
                    const getVpnPostFlexibleButton = page.getByTestId(
                        'get-mozilla-vpn-post-flexible-button'
                    );
                    const getVpnFooterButton = page.getByTestId(
                        'get-mozilla-vpn-footer-button'
                    );

                    const joinWaitlistConvenientButton = page.getByTestId(
                        'join-waitlist-post-convenient-button'
                    );
                    const joinWaitlistPostSecureButton = page.getByTestId(
                        'join-waitlist-post-secure-button'
                    );
                    const joinWaitlistPostFlexibleButton = page.getByTestId(
                        'join-waitlist-post-flexible-button'
                    );
                    const joinWaitlistFooterButton = page.getByTestId(
                        'join-waitlist-footer-button'
                    );

                    // Assert Join Waitlist buttons not displayed.
                    await expect(joinWaitlistConvenientButton).toBeVisible();
                    await expect(joinWaitlistPostSecureButton).toBeVisible();
                    await expect(joinWaitlistPostFlexibleButton).toBeVisible();
                    await expect(joinWaitlistFooterButton).toBeVisible();

                    // Assert Get Mozilla VPN buttons are not displayed.
                    await expect(getVpnPostConvenientButton).not.toBeVisible();
                    await expect(getVpnPostSecureButton).not.toBeVisible();
                    await expect(getVpnPostFlexibleButton).not.toBeVisible();
                    await expect(getVpnFooterButton).not.toBeVisible();
                });
            });
        }
    }
);
