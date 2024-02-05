/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../scripts/open-page');
const url = '/en-US/about/leadership/';

test.describe(
    `${url} page`,
    {
        tag: '@mozorg'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Open / close biography', async ({ page }) => {
            const leader = page.locator(
                '#executive .vcard.has-bio:first-child'
            );
            const bio = page.locator('.mzp-c-modal .vcard.has-bio .person-bio');
            const modal = page.locator('.mzp-c-modal');
            const modalCloseButton = page.locator('.mzp-c-modal-button-close');

            await expect(modal).not.toBeVisible();
            await expect(bio).not.toBeVisible();

            // Open biography modal
            await leader.click();

            // Assert modal and bio are visible
            await expect(modal).toBeVisible();
            await expect(bio).toBeVisible();

            // Close biography modal
            await modalCloseButton.click();

            // Assert modal and bio are not visible
            await expect(modal).not.toBeVisible();
            await expect(bio).not.toBeVisible();
        });
    }
);
