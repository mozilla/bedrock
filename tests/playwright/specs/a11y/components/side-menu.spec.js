/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const openPage = require('../../../scripts/open-page');
const { createReport, scanPageElement } = require('../includes/helpers');
const { sideMenuLocator } = require('../includes/locators');
const { test, expect } = require('@playwright/test');
const testURL = '/en-US/privacy/';

test.describe(
    'Side Menu (desktop)',
    {
        tag: '@a11y'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(testURL, page, browserName);
        });

        test('should not have any detectable a11y issues', async ({ page }) => {
            const results = await scanPageElement(page, sideMenuLocator);
            createReport('component', 'side-menu-desktop', results);
            expect(results.violations.length).toEqual(0);
        });
    }
);

test.describe(
    'Side Menu (mobile)',
    {
        tag: '@a11y'
    },
    () => {
        test.use({ viewport: { width: 360, height: 780 } });

        test.beforeEach(async ({ page, browserName }) => {
            await openPage(testURL, page, browserName);
        });

        test('should not have any detectable a11y issues', async ({ page }) => {
            const sidebarMenuToggle = page.getByTestId('sidebar-menu-toggle');
            const sidebarMenuMain = page.getByTestId('sidebar-menu-main');

            // Open side menu panel
            await expect(sidebarMenuMain).not.toBeVisible();
            await sidebarMenuToggle.click();
            await expect(sidebarMenuMain).toBeVisible();

            const results = await scanPageElement(page, sideMenuLocator);
            createReport('component', 'side-menu-mobile', results);
            expect(results.violations.length).toEqual(0);
        });
    }
);
