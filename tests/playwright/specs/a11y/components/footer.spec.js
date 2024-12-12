/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const openPage = require('../../../scripts/open-page');
const { createReport, scanPageElement } = require('../includes/helpers');
const { footerLocator } = require('../includes/locators');
const { test, expect } = require('@playwright/test');
const testURL = '/en-US/';

test.describe(
    'Footer (desktop)',
    {
        tag: '@a11y'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(testURL, page, browserName);
        });

        test('should not have any detectable a11y issues', async ({ page }) => {
            const results = await scanPageElement(page, footerLocator);
            createReport('component', 'footer-desktop', results);
            expect(results.violations.length).toEqual(0);
        });
    }
);

test.describe(
    'Footer (mobile)',
    {
        tag: '@a11y'
    },
    () => {
        test.use({ viewport: { width: 360, height: 780 } });

        test.beforeEach(async ({ page, browserName }) => {
            await openPage(testURL, page, browserName);
        });

        test('should not have any detectable a11y issues', async ({ page }) => {
            const results = await scanPageElement(page, footerLocator);
            createReport('component', 'footer-mobile', results);
            expect(results.violations.length).toEqual(0);
        });
    }
);
