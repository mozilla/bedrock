/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/products/vpn/invite/';

test.describe(
    `${url} page`,
    {
        tag: '@vpn'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Wait list form submit success', async ({ page }) => {
            const form = page.getByTestId('vpn-invite-form');
            const emailField = page.getByTestId('vpn-invite-email-input');
            const submitButton = page.getByTestId('vpn-invite-submit-button');
            const thanksMessage = page.getByTestId('vpn-invite-thanks-message');

            await expect(thanksMessage).not.toBeVisible();
            await emailField.fill('success@example.com');
            await submitButton.click();
            await expect(form).not.toBeVisible();
            await expect(thanksMessage).toBeVisible();
        });

        test('Wait list form submit failure', async ({ page }) => {
            const emailField = page.getByTestId('vpn-invite-email-input');
            const submitButton = page.getByTestId('vpn-invite-submit-button');
            const thanksMessage = page.getByTestId('vpn-invite-thanks-message');
            const errorMessage = page.getByTestId('vpn-invite-error-message');

            await expect(errorMessage).not.toBeVisible();
            await emailField.fill('failure@example.com');
            await submitButton.click();
            await expect(errorMessage).toBeVisible();
            await expect(thanksMessage).not.toBeVisible();
        });
    }
);
