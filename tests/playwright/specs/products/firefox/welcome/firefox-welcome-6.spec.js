/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../../scripts/open-page');
const url = 'firefox/welcome/6';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test('Set as default button displayed', async ({
            page,
            browserName
        }) => {
            test.skip(
                browserName !== 'firefox',
                'Page shown to Firefox browsers only'
            );

            await openPage(`/en-US/${url}/?default=false`, page, browserName);

            const defaultButton = page.getByTestId('button-firefox-default');

            await expect(defaultButton).toBeVisible();
        });

        test('Send to device form success', async ({ page, browserName }) => {
            test.skip(
                browserName !== 'firefox',
                'Page shown to Firefox browsers only'
            );

            await openPage(`/en-US/${url}/?default=true`, page, browserName);

            const getAppButton = page.getByTestId('button-firefox-get-app');
            const qrCode = page.getByTestId('firefox-qr-code');
            const emailField = page.getByTestId(
                'send-to-device-form-email-field'
            );
            const thanksMessage = page.getByTestId(
                'send-to-device-form-thanks'
            );
            const submitButton = page.getByTestId(
                'send-to-device-form-submit-button'
            );

            await getAppButton.click();
            await expect(qrCode).not.toBeVisible();
            await expect(thanksMessage).not.toBeVisible();
            await expect(submitButton).toBeVisible();
            await emailField.fill('success@example.com');
            await submitButton.click();
            await expect(submitButton).not.toBeVisible();
            await expect(thanksMessage).toBeVisible();
        });

        test('Send to device form failure', async ({ page, browserName }) => {
            test.skip(
                browserName !== 'firefox',
                'Page shown to Firefox browsers only'
            );

            await openPage(`/en-US/${url}/?default=true`, page, browserName);

            const getAppButton = page.getByTestId('button-firefox-get-app');
            const qrCode = page.getByTestId('firefox-qr-code');
            const emailField = page.getByTestId(
                'send-to-device-form-email-field'
            );
            const errorMessage = page.getByTestId('send-to-device-form-error');
            const submitButton = page.getByTestId(
                'send-to-device-form-submit-button'
            );

            await getAppButton.click();
            await expect(qrCode).not.toBeVisible();
            await expect(errorMessage).not.toBeVisible();
            await expect(submitButton).toBeVisible();
            await emailField.fill('failure@example.com');
            await submitButton.click();
            await expect(errorMessage).toBeVisible();
        });

        test('QR Code displayed', async ({ page, browserName }) => {
            test.skip(
                browserName !== 'firefox',
                'Page shown to Firefox browsers only'
            );

            await openPage(`/fy-NL/${url}/?default=true`, page, browserName);

            const getAppButton = page.getByTestId('button-firefox-get-app');
            const qrCode = page.getByTestId('firefox-qr-code');
            const emailField = page.getByTestId(
                'send-to-device-form-email-field'
            );

            await getAppButton.click();
            await expect(qrCode).toBeVisible();
            await expect(emailField).not.toBeVisible();
        });
    }
);
