/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/products/vpn/download/';
const excludedCountries = ['cn'];

test.describe(
    `${url} page`,
    {
        tag: '@vpn'
    },
    () => {
        test.describe('VPN download', () => {
            test.beforeEach(async ({ page, browserName }) => {
                await openPage(url + '?geo=us', page, browserName);
            });

            test('Windows download click', async ({ page, browserName }) => {
                // Click Windows download link
                let downloadLink;

                if (browserName === 'webkit') {
                    downloadLink = page.getByTestId(
                        'vpn-download-link-secondary-windows'
                    );
                } else {
                    downloadLink = page.getByTestId(
                        'vpn-download-link-primary-windows'
                    );
                }

                await expect(downloadLink).toBeVisible();
                await downloadLink.click();
                await page.waitForURL(
                    '**/products/vpn/download/windows/thanks/'
                );

                // Assert /thanks/ page triggers file download.
                const download = await page.waitForEvent('download');
                const downloadURL = download.url();

                expect(downloadURL).toEqual(
                    expect.stringContaining(
                        'https://archive.mozilla.org/pub/vpn/releases/'
                    )
                );

                // Cancel download if not finished.
                await download.cancel();
            });

            test('Mac download click', async ({ page, browserName }) => {
                // Click Windows download link
                let downloadLink;

                if (browserName === 'webkit') {
                    downloadLink = page.getByTestId(
                        'vpn-download-link-primary-mac'
                    );
                } else {
                    downloadLink = page.getByTestId(
                        'vpn-download-link-secondary-mac'
                    );
                }

                await expect(downloadLink).toBeVisible();
                await downloadLink.click();
                await page.waitForURL('**/products/vpn/download/mac/thanks/');

                // Assert /thanks/ page triggers file download.
                const download = await page.waitForEvent('download');
                const downloadURL = download.url();

                expect(downloadURL).toEqual(
                    expect.stringContaining(
                        'https://archive.mozilla.org/pub/vpn/releases/'
                    )
                );

                // Cancel download if not finished.
                await download.cancel();
            });
        });

        for (const country of excludedCountries) {
            test.describe('VPN download blocked in country', () => {
                test.beforeEach(async ({ page, browserName }) => {
                    await openPage(url + `?geo=${country}`, page, browserName);
                });

                test(`Country code: ${country}`, async ({ page }) => {
                    const downloadOptions = page.getByTestId(
                        'vpn-download-options'
                    );
                    const downloadBlockedMessage = page.getByTestId(
                        'vpn-download-blocked-message'
                    );
                    await expect(downloadBlockedMessage).toBeVisible();
                    await expect(downloadOptions).not.toBeVisible();
                });
            });
        }
    }
);
