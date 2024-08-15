/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../scripts/open-page');
const url = '/de/';

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

        test('Footer open / close click', async ({ page }) => {
            const footerHeadingCompany = page.getByTestId(
                'footer-heading-company'
            );
            const footerListCompany = page.getByTestId('footer-list-company');
            const footerHeadingResources = page.getByTestId(
                'footer-heading-resources'
            );
            const footerListResources = page.getByTestId(
                'footer-list-resources'
            );
            const footerHeadingSupport = page.getByTestId(
                'footer-heading-support'
            );
            const footerListSupport = page.getByTestId('footer-list-support');
            const footerHeadingDevelopers = page.getByTestId(
                'footer-heading-developers'
            );
            const footerListDevelopers = page.getByTestId(
                'footer-list-developers'
            );

            // Open and close Company section
            await expect(footerListCompany).not.toBeVisible();
            await footerHeadingCompany.click();
            await expect(footerListCompany).toBeVisible();
            await footerHeadingCompany.click();
            await expect(footerListCompany).not.toBeVisible();

            // Open and close Resources section
            await expect(footerListResources).not.toBeVisible();
            await footerHeadingResources.click();
            await expect(footerListResources).toBeVisible();
            await footerHeadingResources.click();
            await expect(footerListResources).not.toBeVisible();

            // Open and close Support section
            await expect(footerListSupport).not.toBeVisible();
            await footerHeadingSupport.click();
            await expect(footerListSupport).toBeVisible();
            await footerHeadingSupport.click();
            await expect(footerListSupport).not.toBeVisible();

            // Open and close Developers section
            await expect(footerListDevelopers).not.toBeVisible();
            await footerHeadingDevelopers.click();
            await expect(footerListDevelopers).toBeVisible();
            await footerHeadingDevelopers.click();
            await expect(footerListDevelopers).not.toBeVisible();
        });

        test('Footer language change', async ({ page }) => {
            const languageSelect = page.getByTestId('footer-language-select');

            // Assert default language is German
            await expect(languageSelect).toHaveValue('de');

            // Change page language from /de/ to /fr/
            await languageSelect.selectOption('fr');
            await page.waitForURL('**/de/?automation=true', {
                waitUntil: 'commit'
            });

            // Assert page language is now French
            await expect(languageSelect).toHaveValue('fr');
        });
    }
);
