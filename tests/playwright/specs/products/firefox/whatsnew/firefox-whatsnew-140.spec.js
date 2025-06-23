/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../../scripts/open-page');
const url = '/firefox/140.0/whatsnew';

test.describe(
    `EN ${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.use({ locale: 'en-US' });

        test('Displays variant 1', async ({ page, browserName }) => {
            test.skip(
                browserName !== 'firefox',
                'Page shown to Firefox browsers only'
            );

            await openPage(`${url}/?v=1`, page, browserName);

            const wnpFooter = page.getByTestId('wnp-footer');

            await expect(wnpFooter.getByTestId('variant-1')).toBeVisible();
            await expect(wnpFooter.getByTestId('variant-2')).not.toBeVisible();
            await expect(wnpFooter.getByTestId('variant-3')).not.toBeVisible();
            await expect(wnpFooter.getByTestId('default')).not.toBeVisible();

            await expect(wnpFooter.getByRole('link')).toHaveAttribute(
                'href',
                'https://foundation.mozilla.org/?form=25wnp07A'
            );
        });

        test('Displays variant 2', async ({ page, browserName }) => {
            test.skip(
                browserName !== 'firefox',
                'Page shown to Firefox browsers only'
            );

            await openPage(`${url}/?v=2`, page, browserName);

            const wnpFooter = page.getByTestId('wnp-footer');

            await expect(wnpFooter.getByTestId('variant-1')).not.toBeVisible();
            await expect(wnpFooter.getByTestId('variant-2')).toBeVisible();
            await expect(wnpFooter.getByTestId('variant-3')).not.toBeVisible();
            await expect(wnpFooter.getByTestId('default')).not.toBeVisible();

            await expect(wnpFooter.getByRole('link')).toHaveAttribute(
                'href',
                'https://foundation.mozilla.org/?form=25wnp07B'
            );
        });

        test('Displays variant 3', async ({ page, browserName }) => {
            test.skip(
                browserName !== 'firefox',
                'Page shown to Firefox browsers only'
            );

            await openPage(`${url}/?v=3`, page, browserName);

            const wnpFooter = page.getByTestId('wnp-footer');

            await expect(wnpFooter.getByTestId('variant-1')).not.toBeVisible();
            await expect(wnpFooter.getByTestId('variant-2')).not.toBeVisible();
            await expect(wnpFooter.getByTestId('variant-3')).toBeVisible();
            await expect(wnpFooter.getByTestId('default')).not.toBeVisible();

            await expect(wnpFooter.getByRole('link')).toHaveAttribute(
                'href',
                'https://foundation.mozilla.org/?form=25wnp07C'
            );
        });
    }
);

test.describe(
    `non-EN ${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.use({ locale: 'fr' });

        test('Displays default', async ({ page, browserName }) => {
            test.skip(
                browserName !== 'firefox',
                'Page shown to Firefox browsers only'
            );

            await openPage(`${url}/?v=1`, page, browserName);

            const wnpFooter = page.getByTestId('wnp-footer');

            await expect(wnpFooter.getByTestId('variant-1')).not.toBeVisible();
            await expect(wnpFooter.getByTestId('variant-2')).not.toBeVisible();
            await expect(wnpFooter.getByTestId('variant-3')).not.toBeVisible();
            await expect(wnpFooter.getByTestId('default')).toBeVisible();

            await expect(wnpFooter.getByRole('link')).toHaveAttribute(
                'href',
                'https://foundation.mozilla.org/?form=whats-new-product'
            );
        });
    }
);
