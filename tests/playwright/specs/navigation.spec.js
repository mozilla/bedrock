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
            const firefoxLink = page.getByTestId('navigation-link-firefox');
            const firefoxMenu = page.getByTestId('navigation-menu-firefox');
            const productsLink = page.getByTestId('navigation-link-products');
            const productsMenu = page.getByTestId('navigation-menu-products');
            const whoWeAreLink = page.getByTestId('navigation-link-who-we-are');
            const whoWeAreMenu = page.getByTestId('navigation-menu-who-we-are');
            const innovationLink = page.getByTestId(
                'navigation-link-innovation'
            );
            const innovationMenu = page.getByTestId(
                'navigation-menu-innovation'
            );

            // Hover over Firefox link
            await firefoxLink.hover();
            await expect(firefoxMenu).toBeVisible();

            // Hover over products link
            await productsLink.hover();
            await expect(productsMenu).toBeVisible();
            await expect(firefoxMenu).not.toBeVisible();

            // Hover over who we are link
            await whoWeAreLink.hover();
            await expect(whoWeAreMenu).toBeVisible();
            await expect(productsMenu).not.toBeVisible();

            // Hover over innovation link
            await innovationLink.hover();
            await expect(innovationMenu).toBeVisible();
            await expect(whoWeAreMenu).not.toBeVisible();
        });

        test('Navigation link click', async ({ page }) => {
            const firefoxLink = page.getByTestId('navigation-link-firefox');
            const firefoxMenu = page.getByTestId('navigation-menu-firefox');
            const firefoxMenuLink = page.getByTestId(
                'navigation-menu-link-firefox-desktop'
            );

            // Hover over Firefox link
            await firefoxLink.hover();
            await expect(firefoxMenu).toBeVisible();

            // Click Firefox desktop link
            await firefoxMenuLink.click();
            await page.waitForURL('**/firefox/new/');

            // Assert Firefox menu is closed after navigation
            await expect(firefoxMenu).not.toBeVisible();
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
                'navigation-menu-button'
            );
            const navigationMenuItems = page.getByTestId(
                'navigation-menu-items'
            );
            const firefoxLink = page.getByTestId('navigation-link-firefox');
            const firefoxMenu = page.getByTestId('navigation-menu-firefox');
            const productsLink = page.getByTestId('navigation-link-products');
            const productsMenu = page.getByTestId('navigation-menu-products');
            const whoWeAreLink = page.getByTestId('navigation-link-who-we-are');
            const whoWeAreMenu = page.getByTestId('navigation-menu-who-we-are');
            const innovationLink = page.getByTestId(
                'navigation-link-innovation'
            );
            const innovationMenu = page.getByTestId(
                'navigation-menu-innovation'
            );

            // Open navigation menu
            await navigationMenuButton.click();
            await expect(navigationMenuItems).toBeVisible();

            // Open and close Firefox menu
            await firefoxLink.click();
            await expect(firefoxMenu).toBeVisible();
            await firefoxLink.click();
            await expect(firefoxMenu).not.toBeVisible();

            // Open and close products menu
            await productsLink.click();
            await expect(productsMenu).toBeVisible();
            await productsLink.click();
            await expect(productsMenu).not.toBeVisible();

            // Open and close who we are menu
            await whoWeAreLink.click();
            await expect(whoWeAreMenu).toBeVisible();
            await whoWeAreLink.click();
            await expect(whoWeAreMenu).not.toBeVisible();

            // Open and close innovation menu
            await innovationLink.click();
            await expect(innovationMenu).toBeVisible();
            await innovationLink.click();
            await expect(innovationMenu).not.toBeVisible();

            // Close navigation menu
            await navigationMenuButton.click();
            await expect(navigationMenuItems).not.toBeVisible();
        });

        test('Navigation link click', async ({ page }) => {
            const navigationMenuButton = page.getByTestId(
                'navigation-menu-button'
            );
            const navigationMenuItems = page.getByTestId(
                'navigation-menu-items'
            );
            const firefoxLink = page.getByTestId('navigation-link-firefox');
            const firefoxMenu = page.getByTestId('navigation-menu-firefox');
            const firefoxMenuLink = page.getByTestId(
                'navigation-menu-link-firefox-desktop'
            );

            // Open navigation menu
            await navigationMenuButton.click();
            await expect(navigationMenuItems).toBeVisible();

            // Open and Firefox menu
            await firefoxLink.click();
            await expect(firefoxMenu).toBeVisible();

            // Click Firefox desktop link
            await firefoxMenuLink.click();
            await page.waitForURL('**/firefox/new/');

            // Assert nav menu is closed again after navigation
            await expect(navigationMenuItems).not.toBeVisible();
        });
    }
);
