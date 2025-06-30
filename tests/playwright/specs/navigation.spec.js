/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../scripts/open-page');
const url = '/en-US/';

test.describe(
    `${url} navigation (desktop)`,
    {
        tag: '@mozorg'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Navigation menu hover', async ({ page }) => {
            const productsLink = page.getByTestId(
                'm24-navigation-link-products'
            );
            const productsMenu = page.getByTestId(
                'm24-navigation-menu-products'
            );
            const aboutUsLink = page.getByTestId(
                'm24-navigation-link-about-us'
            );
            const aboutUsMenu = page.getByTestId(
                'm24-navigation-menu-about-us'
            );

            // Hover over products link
            await productsLink.hover();
            await expect(productsMenu).toBeVisible();

            // Hover over about us link
            await aboutUsLink.hover();
            await expect(aboutUsMenu).toBeVisible();
            await expect(productsMenu).not.toBeVisible();
        });

        test('Navigation link click', async ({ page }) => {
            const productsLink = page.getByTestId(
                'm24-navigation-link-products'
            );
            const productsMenu = page.getByTestId(
                'm24-navigation-menu-products'
            );
            const productsMenuLink = page.getByTestId(
                'm24-navigation-menu-link-products-vpn'
            );

            // Hover over Products VPN link
            await productsLink.hover();
            await expect(productsMenu).toBeVisible();

            // Click Products VPN link
            await productsMenuLink.click();
            await page.waitForURL('**/products/vpn/', {
                waitUntil: 'commit'
            });

            // Assert Products menu is closed after navigation
            await expect(productsMenu).not.toBeVisible();
        });
    }
);

test.describe(
    `${url} navigation (mobile)`,
    {
        tag: '@mozorg'
    },
    () => {
        test.use({ viewport: { width: 360, height: 780 } });

        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Navigation open / close click', async ({ page }) => {
            const navigationMenuButton = page.getByTestId(
                'm24-navigation-menu-button'
            );
            const navigationMenuItems = page.getByTestId(
                'm24-navigation-menu-items'
            );
            const productsLink = page.getByTestId(
                'm24-navigation-link-products'
            );
            const productsMenu = page.getByTestId(
                'm24-navigation-menu-products'
            );
            const aboutUsLink = page.getByTestId(
                'm24-navigation-link-about-us'
            );
            const aboutUsMenu = page.getByTestId(
                'm24-navigation-menu-about-us'
            );

            // Open navigation menu
            await navigationMenuButton.click();
            await expect(navigationMenuItems).toBeVisible();

            // Open and close products menu
            await productsLink.click();
            await expect(productsMenu).toBeVisible();
            await productsLink.click();
            await expect(productsMenu).not.toBeVisible();

            // Open and close about us menu
            await aboutUsLink.click();
            await expect(aboutUsMenu).toBeVisible();
            await aboutUsLink.click();
            await expect(aboutUsMenu).not.toBeVisible();

            // Close navigation menu
            await navigationMenuButton.click();
            await expect(navigationMenuItems).not.toBeVisible();
        });

        test('Navigation link click', async ({ page }) => {
            const navigationMenuButton = page.getByTestId(
                'm24-navigation-menu-button'
            );
            const navigationMenuItems = page.getByTestId(
                'm24-navigation-menu-items'
            );
            const productsLink = page.getByTestId(
                'm24-navigation-link-products'
            );
            const productsMenu = page.getByTestId(
                'm24-navigation-menu-products'
            );
            const productsMenuLink = page.getByTestId(
                'm24-navigation-menu-link-products-vpn'
            );

            // Open navigation menu
            await navigationMenuButton.click();
            await expect(navigationMenuItems).toBeVisible();

            // Open Products menu
            await productsLink.click();
            await expect(productsMenu).toBeVisible();

            // Click products vpn link
            await productsMenuLink.click();
            await page.waitForURL('**/products/vpn/', {
                waitUntil: 'commit'
            });

            // Assert nav menu is closed again after navigation
            await expect(navigationMenuItems).not.toBeVisible();
        });
    }
);
