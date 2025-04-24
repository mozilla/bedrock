/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../scripts/open-page');
const url = '/en-US/analytics-tests/';

const isGALoaded = async function (page) {
    const dataLayer = await page.evaluate(() => {
        return window.dataLayer;
    });

    const loadEvent = dataLayer.filter((layer) => {
        return (
            Object.prototype.hasOwnProperty.call(layer, 'event') &&
            layer['event'] === 'gtm.load'
        );
    });
    return loadEvent.length > 0 ? true : false;
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
        });

        test('window.dataLayer updates on download click', async ({ page }) => {
            expect(await isGALoaded(page)).toBe(true);

            const button = page.getByTestId('button-download');
            await button.click();

            const layer = await getGAElement(page, 'data-link-type');

            expect(layer).toBe('download-test');
        });

        test('window.dataLayer updates on CTA click', async ({ page }) => {
            expect(await isGALoaded(page)).toBe(true);

            const button = page.getByTestId('button-cta');
            await button.click();

            const layer = await getGAElement(page, 'data-cta-type');

            expect(layer).toBe('button-test');
        });

        test('window.dataLayer updates on FxA button click', async ({
            page
        }) => {
            expect(await isGALoaded(page)).toBe(true);

            const button = page.getByTestId('button-fxa');
            await button.click();

            const layer = await getGAElement(page, 'data-cta-type');

            expect(layer).toBe('fxa-sync-test');
        });
    }
);
