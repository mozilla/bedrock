/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/products/vpn/';
const availableCountries = ['us', 'ca', 'gb', 'de', 'fr'];
const mobileOnlyCountries = ['au', 'in', 'mx', 'ua'];
const androidOnlyCountries = ['br', 'ma'];
const unavailableCountries = ['cn'];
const vpnBundleAvailableCountry = ['us'];
const experimentVariant =
    '&entrypoint_experiment=vpn-landing-bundle-promo&entrypoint_variation=c';
const experimenControltVariant =
    '&entrypoint_experiment=vpn-landing-bundle-promo&entrypoint_variation=a';

test.describe(
    `${url} page`,
    {
        tag: '@vpn'
    },
    () => {
        for (const country of availableCountries) {
            test.describe('VPN available', () => {
                if (country === 'us') {
                    test.beforeEach(async ({ page, browserName }) => {
                        await openPage(
                            url + `?geo=${country}${experimenControltVariant}`,
                            page,
                            browserName
                        );
                    });
                } else {
                    test.beforeEach(async ({ page, browserName }) => {
                        await openPage(
                            url + `?geo=${country}`,
                            page,
                            browserName
                        );
                    });
                }

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnHeroButton = page.getByTestId(
                        'get-mozilla-vpn-hero-button'
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
                    const getVpnTertiaryButton = page.getByTestId(
                        'get-mozilla-vpn-tertiary-button'
                    );
                    const getVpnFooterButton = page.getByTestId(
                        'get-mozilla-vpn-footer-button'
                    );
                    const getVpnAppStorebutton = page.getByTestId(
                        'get-vpn-ios-app-store'
                    );
                    const getVpnPlayStorebutton = page.getByTestId(
                        'get-vpn-google-play-store'
                    );
                    const getVpnQrCode = page.getByTestId('get-vpn-qr-code');
                    const waitlistHeroButton = page.getByTestId(
                        'join-waitlist-hero-button'
                    );
                    const waitlistNotAvailableButton = page.getByTestId(
                        'join-waitlist-not-available-button'
                    );
                    const waitlistSecondaryButton = page.getByTestId(
                        'join-waitlist-secondary-button'
                    );
                    const waitlistTertiaryButton = page.getByTestId(
                        'join-waitlist-tertiary-button'
                    );
                    const waitlistFooterButton = page.getByTestId(
                        'join-waitlist-footer-button'
                    );

                    // Assert Get Mozilla VPN buttons are displayed.
                    await expect(getVpnHeroButton).toBeVisible();
                    await expect(getVpnTwelveMonthButton).toBeVisible();
                    await expect(getVpnMonthlyButton).toBeVisible();
                    await expect(getVpnSecondaryButton).toBeVisible();
                    await expect(getVpnTertiaryButton).toBeVisible();
                    await expect(getVpnFooterButton).toBeVisible();

                    // Assert mobile only CTAs are not displayed.
                    await expect(getVpnAppStorebutton).not.toBeVisible();
                    await expect(getVpnPlayStorebutton).not.toBeVisible();
                    await expect(getVpnQrCode).not.toBeVisible();

                    // Assert Join Waitlist buttons are not displayed.
                    await expect(waitlistHeroButton).not.toBeVisible();
                    await expect(waitlistNotAvailableButton).not.toBeVisible();
                    await expect(waitlistSecondaryButton).not.toBeVisible();
                    await expect(waitlistTertiaryButton).not.toBeVisible();
                    await expect(waitlistFooterButton).not.toBeVisible();
                });
            });
        }

        for (const country of mobileOnlyCountries) {
            test.describe('VPN available via mobile subscription only', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(url + `?geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnHeroButton = page.getByTestId(
                        'get-mozilla-vpn-hero-button'
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
                    const getVpnTertiaryButton = page.getByTestId(
                        'get-mozilla-vpn-tertiary-button'
                    );
                    const getVpnFooterButton = page.getByTestId(
                        'get-mozilla-vpn-footer-button'
                    );
                    const getVpnAppStorebutton = page.getByTestId(
                        'get-vpn-ios-app-store'
                    );
                    const getVpnPlayStorebutton = page.getByTestId(
                        'get-vpn-google-play-store'
                    );
                    const getVpnQrCode = page.getByTestId('get-vpn-qr-code');
                    const waitlistHeroButton = page.getByTestId(
                        'join-waitlist-hero-button'
                    );
                    const waitlistNotAvailableButton = page.getByTestId(
                        'join-waitlist-not-available-button'
                    );
                    const waitlistSecondaryButton = page.getByTestId(
                        'join-waitlist-secondary-button'
                    );
                    const waitlistTertiaryButton = page.getByTestId(
                        'join-waitlist-tertiary-button'
                    );
                    const waitlistFooterButton = page.getByTestId(
                        'join-waitlist-footer-button'
                    );

                    // Assert Get Mozilla VPN buttons are displayed.
                    await expect(getVpnHeroButton).toBeVisible();
                    await expect(getVpnSecondaryButton).toBeVisible();
                    await expect(getVpnTertiaryButton).toBeVisible();
                    await expect(getVpnFooterButton).toBeVisible();

                    // Assert mobile only CTAs are displayed.
                    await expect(getVpnAppStorebutton).toBeVisible();
                    await expect(getVpnPlayStorebutton).toBeVisible();
                    await expect(getVpnQrCode).toBeVisible();

                    // Assert desktop FxA links are not displayed.
                    await expect(getVpnTwelveMonthButton).not.toBeVisible();
                    await expect(getVpnMonthlyButton).not.toBeVisible();

                    // Assert Join Waitlist buttons are not displayed.
                    await expect(waitlistHeroButton).not.toBeVisible();
                    await expect(waitlistNotAvailableButton).not.toBeVisible();
                    await expect(waitlistSecondaryButton).not.toBeVisible();
                    await expect(waitlistTertiaryButton).not.toBeVisible();
                    await expect(waitlistFooterButton).not.toBeVisible();
                });
            });
        }

        for (const country of androidOnlyCountries) {
            test.describe('VPN available via android subscription only', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(url + `?geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnHeroButton = page.getByTestId(
                        'get-mozilla-vpn-hero-button'
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
                    const getVpnTertiaryButton = page.getByTestId(
                        'get-mozilla-vpn-tertiary-button'
                    );
                    const getVpnFooterButton = page.getByTestId(
                        'get-mozilla-vpn-footer-button'
                    );
                    const getVpnAppStorebutton = page.getByTestId(
                        'get-vpn-ios-app-store'
                    );
                    const getVpnPlayStorebutton = page.getByTestId(
                        'get-vpn-google-play-store'
                    );
                    const getVpnQrCode = page.getByTestId('get-vpn-qr-code');
                    const waitlistHeroButton = page.getByTestId(
                        'join-waitlist-hero-button'
                    );
                    const waitlistNotAvailableButton = page.getByTestId(
                        'join-waitlist-not-available-button'
                    );
                    const waitlistSecondaryButton = page.getByTestId(
                        'join-waitlist-secondary-button'
                    );
                    const waitlistTertiaryButton = page.getByTestId(
                        'join-waitlist-tertiary-button'
                    );
                    const waitlistFooterButton = page.getByTestId(
                        'join-waitlist-footer-button'
                    );

                    // Assert Get Mozilla VPN buttons are displayed.
                    await expect(getVpnHeroButton).toBeVisible();
                    await expect(getVpnSecondaryButton).toBeVisible();
                    await expect(getVpnTertiaryButton).toBeVisible();
                    await expect(getVpnFooterButton).toBeVisible();

                    // Assert only android CTAs are displayed.
                    await expect(getVpnAppStorebutton).not.toBeVisible();
                    await expect(getVpnPlayStorebutton).toBeVisible();
                    await expect(getVpnQrCode).toBeVisible();

                    // Assert desktop FxA links are not displayed.
                    await expect(getVpnTwelveMonthButton).not.toBeVisible();
                    await expect(getVpnMonthlyButton).not.toBeVisible();

                    // Assert Join Waitlist buttons are not displayed.
                    await expect(waitlistHeroButton).not.toBeVisible();
                    await expect(waitlistNotAvailableButton).not.toBeVisible();
                    await expect(waitlistSecondaryButton).not.toBeVisible();
                    await expect(waitlistTertiaryButton).not.toBeVisible();
                    await expect(waitlistFooterButton).not.toBeVisible();
                });
            });
        }

        for (const country of unavailableCountries) {
            test.describe('VPN not available', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(url + `?geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnHeroButton = page.getByTestId(
                        'get-mozilla-vpn-hero-button'
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
                    const getVpnTertiaryButton = page.getByTestId(
                        'get-mozilla-vpn-tertiary-button'
                    );
                    const getVpnFooterButton = page.getByTestId(
                        'get-mozilla-vpn-footer-button'
                    );
                    const getVpnAppStorebutton = page.getByTestId(
                        'get-vpn-ios-app-store'
                    );
                    const getVpnPlayStorebutton = page.getByTestId(
                        'get-vpn-google-play-store'
                    );
                    const getVpnQrCode = page.getByTestId('get-vpn-qr-code');
                    const waitlistHeroButton = page.getByTestId(
                        'join-waitlist-hero-button'
                    );
                    const waitlistNotAvailableButton = page.getByTestId(
                        'join-waitlist-not-available-button'
                    );
                    const waitlistSecondaryButton = page.getByTestId(
                        'join-waitlist-secondary-button'
                    );
                    const waitlistTertiaryButton = page.getByTestId(
                        'join-waitlist-tertiary-button'
                    );
                    const waitlistFooterButton = page.getByTestId(
                        'join-waitlist-footer-button'
                    );

                    // Assert Join Waitlist buttons are displayed.
                    await expect(waitlistHeroButton).toBeVisible();
                    await expect(waitlistNotAvailableButton).toBeVisible();
                    await expect(waitlistSecondaryButton).toBeVisible();
                    await expect(waitlistTertiaryButton).toBeVisible();
                    await expect(waitlistFooterButton).toBeVisible();

                    // Assert Get Mozilla VPN buttons are not displayed.
                    await expect(getVpnHeroButton).not.toBeVisible();
                    await expect(getVpnTwelveMonthButton).not.toBeVisible();
                    await expect(getVpnMonthlyButton).not.toBeVisible();
                    await expect(getVpnSecondaryButton).not.toBeVisible();
                    await expect(getVpnTertiaryButton).not.toBeVisible();
                    await expect(getVpnFooterButton).not.toBeVisible();

                    // Assert mobile only CTAs are not displayed.
                    await expect(getVpnAppStorebutton).not.toBeVisible();
                    await expect(getVpnPlayStorebutton).not.toBeVisible();
                    await expect(getVpnQrCode).not.toBeVisible();
                });
            });
        }
    }
);

test.describe(
    `${url} page`,
    {
        tag: '@vpn'
    },
    () => {
        for (const country of vpnBundleAvailableCountry) {
            test.describe('VPN bundle available', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(
                        url +
                            `?geo=${vpnBundleAvailableCountry}${experimentVariant}`,
                        page,
                        browserName
                    );
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const getVpnHeroButton = page.getByTestId(
                        'get-mozilla-vpn-hero-button'
                    );

                    // tab yearly
                    const getVpnTwelveMonthButton = page.getByTestId(
                        'vpn-pricing-grid-12-month-button'
                    );

                    // tab monthly
                    const getVpnMonthlyButton = page.getByTestId(
                        'vpn-pricing-grid-monthly-button'
                    );

                    // banner bundle button
                    const privacyProductBundleBannerButton = page.getByTestId(
                        'privacy-product-bundle-banner-button'
                    );
                    // pricing grid bundle button
                    const privacyProductBundlePricingGridButton =
                        page.getByTestId(
                            'privacy-product-bundle-pricing-grid-button'
                        );

                    const getVpnFooterButton = page.getByTestId(
                        'get-mozilla-vpn-footer-button'
                    );
                    const getVpnAppStorebutton = page.getByTestId(
                        'get-vpn-ios-app-store'
                    );
                    const getVpnPlayStorebutton = page.getByTestId(
                        'get-vpn-google-play-store'
                    );
                    const getVpnQrCode = page.getByTestId('get-vpn-qr-code');
                    const waitlistHeroButton = page.getByTestId(
                        'join-waitlist-hero-button'
                    );
                    const waitlistNotAvailableButton = page.getByTestId(
                        'join-waitlist-not-available-button'
                    );
                    const waitlistSecondaryButton = page.getByTestId(
                        'join-waitlist-secondary-button'
                    );
                    const waitlistTertiaryButton = page.getByTestId(
                        'join-waitlist-tertiary-button'
                    );
                    const waitlistFooterButton = page.getByTestId(
                        'join-waitlist-footer-button'
                    );

                    // Assert Get Mozilla VPN buttons are displayed.
                    await expect(getVpnHeroButton).toBeVisible();
                    await expect(getVpnTwelveMonthButton).toBeVisible();
                    await expect(
                        privacyProductBundleBannerButton
                    ).toBeVisible();
                    await expect(
                        privacyProductBundlePricingGridButton
                    ).toBeVisible();
                    await expect(getVpnFooterButton).toBeVisible();

                    // tab monthly is hidden by default
                    await expect(getVpnMonthlyButton).not.toBeVisible();

                    // Assert mobile only CTAs are not displayed.
                    await expect(getVpnAppStorebutton).not.toBeVisible();
                    await expect(getVpnPlayStorebutton).not.toBeVisible();
                    await expect(getVpnQrCode).not.toBeVisible();

                    // Assert Join Waitlist buttons are not displayed.
                    await expect(waitlistHeroButton).not.toBeVisible();
                    await expect(waitlistNotAvailableButton).not.toBeVisible();
                    await expect(waitlistSecondaryButton).not.toBeVisible();
                    await expect(waitlistTertiaryButton).not.toBeVisible();
                    await expect(waitlistFooterButton).not.toBeVisible();
                });
            });
        }
    }
);
