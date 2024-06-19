/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/products/vpn/download/mac/thanks/';
const blockedCountries = ['cn'];

test.describe(
    `${url} page`,
    {
        tag: '@vpn'
    },
    () => {
        for (const country of blockedCountries) {
            test.describe('VPN download blocked in country', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(url + `?geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const downloadInstructions = page.getByTestId(
                        'vpn-download-instructions'
                    );
                    const downloadBlockedMessage = page.getByTestId(
                        'vpn-download-blocked-message'
                    );
                    await expect(downloadBlockedMessage).toBeVisible();
                    await expect(downloadInstructions).not.toBeVisible();
                });
            });
        }
    }
);
