/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../scripts/open-page');
const url = '/en-US/products/';

test.describe(
    `${url} page`,
    {
        tag: '@mozorg'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Account form sign up', async ({ page }) => {
            const emailQueryString = /&email=success%40example.com/;
            const emailField = page.getByTestId('fxa-form-email-field');
            const submitButton = page.getByTestId('fxa-form-submit-button');

            await emailField.fill('success@example.com');
            await submitButton.click();
            await page.waitForURL(emailQueryString, {
                waitUntil: 'commit'
            });
            await expect(page).toHaveURL(emailQueryString);
        });
    }
);
