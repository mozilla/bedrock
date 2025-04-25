/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../scripts/open-page');
const url = '/locales/';

test.describe(
    `${url} page`,
    {
        tag: '@mozorg'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Locale links are displayed', async ({ page }) => {
            const americas = page.locator('#americas ul > li > a');
            const asia = page.locator('#asia-pacific ul > li > a');
            const europe = page.locator('#europe ul > li > a');
            const middleEast = page.locator(
                '#middle-east-and-africa ul > li > a'
            );

            expect(await americas.count()).toBeGreaterThan(1);
            expect(await asia.count()).toBeGreaterThan(1);
            expect(await europe.count()).toBeGreaterThan(1);
            expect(await middleEast.count()).toBeGreaterThan(1);
        });
    }
);
