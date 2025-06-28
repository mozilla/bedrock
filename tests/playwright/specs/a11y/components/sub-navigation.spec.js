/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const openPage = require('../../../scripts/open-page');
const { createReport, scanPageElement } = require('../includes/helpers');
const { subNavigationLocator } = require('../includes/locators');
const { test, expect } = require('@playwright/test');
const testURL = '/en-US/products/vpn/';

test.describe(
    'Sub-navigation (desktop)',
    {
        tag: '@a11y'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(testURL, page, browserName);
        });

        test('should not have any detectable a11y issues', async ({ page }) => {
            const results = await scanPageElement(page, subNavigationLocator);
            createReport('component', 'sub-navigation-mobile', results);
            expect(results.violations.length).toEqual(0);
        });
    }
);

test.describe(
    'Sub-navigation (mobile)',
    {
        tag: '@a11y'
    },
    () => {
        test.use({ viewport: { width: 360, height: 780 } });

        test.beforeEach(async ({ page, browserName }) => {
            await openPage(testURL, page, browserName);
        });

        test('should not have any detectable a11y issues', async ({ page }) => {
            const subNavigationToggle = page.getByTestId(
                'sub-navigation-mobile-toggle'
            );
            const subNavigationMenu = page.getByTestId('sub-navigation-menu');

            // Open sub-navigation menu
            await expect(subNavigationMenu).not.toBeVisible();
            await subNavigationToggle.click();
            await expect(subNavigationMenu).toBeVisible();

            const results = await scanPageElement(page, subNavigationLocator);
            createReport('component', 'sub-navigation-mobile', results);
            expect(results.violations.length).toEqual(0);
        });
    }
);
