/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../scripts/open-page');
const url = '/en-US/analytics-tests/';

const waitForGAToLoad = async function (page) {
    try {
        await page.waitForFunction(() => {
            return (
                typeof window.dataLayer !== 'undefined' &&
                window.dataLayer.some((entry) => entry.event === 'gtm.load')
            );
        });
    } catch (error) {
        // eslint-disable-next-line no-console
        console.error(
            'These tests require Google Analytics to be configured. Please ensure you have set a GTM_CONTAINER_ID environment variable in your .env and you are not blocking GA in your browser.'
        );
        throw error; // rethrow to fail the test, or handle it differently
    }
};

const getGAElement = async function (page, name) {
    return await page.evaluate((name) => {
        const element = window.dataLayer.find((layer) => {
            return Object.prototype.hasOwnProperty.call(layer, 'gtm.element');
        });
        return element['gtm.element'].getAttribute(name);
    }, name);
};

test.describe(
    `${url} Google analytics`,
    {
        tag: '@mozorg'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
            await waitForGAToLoad(page);
        });

        test('window.dataLayer updates on link-text click', async ({
            page
        }) => {
            const button = page.getByTestId('button-link');
            await button.click();

            const layer = await getGAElement(page, 'data-link-text');

            expect(layer).toBe('link-test');
        });

        test('window.dataLayer updates on CTA click', async ({ page }) => {
            const button = page.getByTestId('button-cta');
            await button.click();

            const layer = await getGAElement(page, 'data-cta-type');

            expect(layer).toBe('button-test');
        });

        test('window.dataLayer updates on FxA button click', async ({
            page
        }) => {
            const button = page.getByTestId('button-fxa');
            await button.click();

            const layer = await getGAElement(page, 'data-cta-type');

            expect(layer).toBe('fxa-sync-test');
        });
    }
);
