/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../scripts/open-page');
const url = '/en-US/';

test.describe(
    `${url} footer (mobile)`,
    {
        tag: '@mozorg'
    },
    () => {
        test.use({ viewport: { width: 360, height: 780 } });

        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Footer newsletter submit success', async ({ page }) => {
            const form = page.getByTestId('newsletter-form');
            const emailField = page.getByTestId('newsletter-email-input');
            const countryField = page.getByTestId('newsletter-country-select');
            const privacyCheckbox = page.getByTestId(
                'newsletter-privacy-checkbox'
            );
            const submitButton = page.getByTestId('newsletter-submit-button');
            const thanksMessage = page.getByTestId('newsletter-thanks-message');

            // expand form before running test
            await submitButton.click();

            await expect(thanksMessage).not.toBeVisible();
            await emailField.fill('success@example.com');
            await countryField.selectOption('us');
            await privacyCheckbox.click();
            await submitButton.click();
            await expect(form).not.toBeVisible();
            await expect(thanksMessage).toBeVisible();
        });

        test('Footer newsletter submit failure', async ({ page }) => {
            const emailField = page.getByTestId('newsletter-email-input');
            const countryField = page.getByTestId('newsletter-country-select');
            const privacyCheckbox = page.getByTestId(
                'newsletter-privacy-checkbox'
            );
            const submitButton = page.getByTestId('newsletter-submit-button');
            const thanksMessage = page.getByTestId('newsletter-thanks-message');
            const errorMessage = page.getByTestId('newsletter-error-message');

            // expand form before running test
            await page.getByTestId('newsletter-submit-button').click();

            await expect(errorMessage).not.toBeVisible();
            await emailField.fill('failure@example.com');
            await countryField.selectOption('us');
            await privacyCheckbox.click();
            await submitButton.click();
            await expect(errorMessage).toBeVisible();
            await expect(thanksMessage).not.toBeVisible();
        });

        test('Footer language change', async ({ page }) => {
            const languageSelect = page.getByTestId('footer-language-select');

            // Assert default language is English
            await expect(languageSelect).toHaveValue('en-US');

            // Change page language from /en-US/ to /de/
            await languageSelect.selectOption('de');
            await page.waitForURL('**/de/?automation=true', {
                waitUntil: 'commit'
            });

            // Assert page language is now German
            await expect(
                page.getByTestId('footer-language-select')
            ).toHaveValue('de');
        });
    }
);
