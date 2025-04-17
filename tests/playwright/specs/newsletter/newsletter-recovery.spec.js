/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../scripts/open-page');
const url = '/en-US/newsletter/';
const slugs = ['opt-out-confirmation', 'recovery'];

test.describe(
    `${url} page`,
    {
        tag: '@newsletter'
    },
    () => {
        for (const slug of slugs) {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(url + `${slug}/`, page, browserName);
            });

            test(`Recovery submit success /${slug}/`, async ({ page }) => {
                const emailField = page.getByTestId('newsletter-email-input');
                const submitButton = page.getByTestId(
                    'newsletter-recovery-submit'
                );
                const thanksMessage = page.getByTestId(
                    'newsletter-recovery-thanks'
                );

                // expand form before running test
                await submitButton.click();

                await expect(thanksMessage).not.toBeVisible();
                await emailField.fill('success@example.com');
                await submitButton.click();
                await expect(thanksMessage).toBeVisible();
            });

            test(`Recovery submit failure /${slug}/`, async ({ page }) => {
                const emailField = page.getByTestId('newsletter-email-input');
                const submitButton = page.getByTestId(
                    'newsletter-recovery-submit'
                );
                const thanksMessage = page.getByTestId(
                    'newsletter-recovery-thanks'
                );
                const errorMessage = page.getByTestId(
                    'newsletter-recovery-error-message'
                );

                // expand form before running test
                await submitButton.click();

                await expect(errorMessage).not.toBeVisible();
                await emailField.fill('failure@example.com');
                await submitButton.click();
                await expect(errorMessage).toBeVisible();
                await expect(thanksMessage).not.toBeVisible();
            });
        }
    }
);
