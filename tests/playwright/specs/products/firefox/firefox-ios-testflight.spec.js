/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/ios/testflight/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Signup success', async ({ page, browserName }) => {
            const newsletterForm = page.getByTestId('newsletter-form');
            const emailInput = page.getByTestId('newsletter-email-input');
            const termsCheckbox = page.getByTestId('newsletter-terms-checkbox');
            const privacyCheckbox = page.getByTestId(
                'newsletter-privacy-checkbox'
            );
            const submitButton = page.getByTestId('newsletter-submit-button');
            const thanksMessage = page.getByTestId('newsletter-thanks-message');

            await openPage(url, page, browserName);

            await expect(thanksMessage).not.toBeVisible();

            // expand form before running test
            await submitButton.click();

            await emailInput.fill('success@example.com');
            await termsCheckbox.click();
            await privacyCheckbox.click();
            await submitButton.click();
            await expect(newsletterForm).not.toBeVisible();
            await expect(thanksMessage).toBeVisible();
        });

        test('Signup failure', async ({ page, browserName }) => {
            const newsletterErrorMessage = page.getByTestId(
                'newsletter-error-message'
            );
            const emailInput = page.getByTestId('newsletter-email-input');
            const termsCheckbox = page.getByTestId('newsletter-terms-checkbox');
            const privacyCheckbox = page.getByTestId(
                'newsletter-privacy-checkbox'
            );
            const submitButton = page.getByTestId('newsletter-submit-button');
            const thanksMessage = page.getByTestId('newsletter-thanks-message');

            await openPage(url, page, browserName);

            // expand form before running test
            await submitButton.click();

            await emailInput.fill('failure@example.com');
            await termsCheckbox.click();
            await privacyCheckbox.click();
            await submitButton.click();
            await expect(newsletterErrorMessage).toBeVisible();
            await expect(thanksMessage).not.toBeVisible();
        });
    }
);
