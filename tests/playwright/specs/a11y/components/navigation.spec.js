/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const openPage = require('../../../scripts/open-page');
const { createReport, scanPageElement } = require('../includes/helpers');
const { navigationLocator } = require('../includes/locators');
const { test, expect } = require('@playwright/test');
const testURL = '/en-US/';
const disabledRules = ['blink'];

test.describe(
    'Navigation (desktop)',
    {
        tag: '@a11y'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(testURL, page, browserName);
        });

        test('should not have any detectable a11y issues', async ({ page }) => {
            const productsLink = page.getByTestId(
                'm24-navigation-link-products'
            );
            const productsMenu = page.getByTestId(
                'm24-navigation-menu-products'
            );

            // Hover over Products link to open menu
            await expect(productsMenu).not.toBeVisible();
            await productsLink.hover();
            await expect(productsMenu).toBeVisible();

            const results = await scanPageElement(
                page,
                navigationLocator,
                disabledRules
            );
            createReport('component', 'navigation-desktop', results);
            expect(results.violations.length).toEqual(0);
        });
    }
);

test.describe(
    'Navigation (mobile)',
    {
        tag: '@a11y'
    },
    () => {
        test.use({ viewport: { width: 360, height: 780 } });

        test.beforeEach(async ({ page, browserName }) => {
            await openPage(testURL, page, browserName);
        });

        test('should not have any detectable a11y issues', async ({ page }) => {
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

            // Open navigation menu
            await expect(navigationMenuItems).not.toBeVisible();
            await navigationMenuButton.click();
            await expect(navigationMenuItems).toBeVisible();

            // Open Products menu
            await expect(productsMenu).not.toBeVisible();
            await productsLink.click();
            await expect(productsMenu).toBeVisible();

            const results = await scanPageElement(
                page,
                navigationLocator,
                disabledRules
            );
            createReport('component', 'navigation-mobile', results);
            expect(results.violations.length).toEqual(0);
        });
    }
);
