/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { test, expect } = require('@playwright/test');
const openPage = require('../../../scripts/open-page');
const url = '/en-US/firefox/enterprise/';

test.describe(
    `${url} page`,
    {
        tag: '@firefox'
    },
    () => {
        test.beforeEach(async ({ page, browserName }) => {
            await openPage(url, page, browserName);
        });

        test('Firefox ESR Windows 64bit menu open / close', async ({
            page
        }) => {
            const win64MenuButton = page.getByTestId(
                'firefox-enterprise-win64-menu-button'
            );
            const win64MenuLink = page.getByTestId(
                'firefox-enterprise-win64-menu-link'
            );
            const win64MsiMenuLink = page.getByTestId(
                'firefox-enterprise-win64-msi-menu-link'
            );
            const win64EsrMenuLink = page.getByTestId(
                'firefox-enterprise-win64-esr-menu-link'
            );
            const win64EsrMsiMenuLink = page.getByTestId(
                'firefox-enterprise-win64-esr-msi-menu-link'
            );

            await expect(win64MenuLink).not.toBeVisible();
            await expect(win64MsiMenuLink).not.toBeVisible();
            await expect(win64EsrMenuLink).not.toBeVisible();
            await expect(win64EsrMsiMenuLink).not.toBeVisible();

            // open menu
            await win64MenuButton.click();

            // Assert Windows 64-bit menu links are displayed.
            await expect(win64MenuLink).toBeVisible();
            await expect(win64MenuLink).toHaveAttribute(
                'href',
                /\?product=firefox-latest-ssl&os=win64/
            );
            await expect(win64MsiMenuLink).toBeVisible();
            await expect(win64MsiMenuLink).toHaveAttribute(
                'href',
                /\?product=firefox-msi-latest-ssl&os=win64/
            );
            await expect(win64EsrMenuLink).toBeVisible();
            await expect(win64EsrMenuLink).toHaveAttribute(
                'href',
                /\?product=firefox-esr-latest-ssl&os=win64/
            );
            await expect(win64EsrMsiMenuLink).toBeVisible();
            await expect(win64EsrMsiMenuLink).toHaveAttribute(
                'href',
                /\?product=firefox-esr-msi-latest-ssl&os=win64/
            );

            // close menu
            await win64MenuButton.click();

            // Assert Windows 64-bit menu links are hidden.
            await expect(win64MenuLink).not.toBeVisible();
            await expect(win64MsiMenuLink).not.toBeVisible();
            await expect(win64EsrMenuLink).not.toBeVisible();
            await expect(win64EsrMsiMenuLink).not.toBeVisible();
        });

        test('Firefox ESR macOS menu open / close', async ({ page }) => {
            const macMenuButton = page.getByTestId(
                'firefox-enterprise-mac-menu-button'
            );
            const macMenuLink = page.getByTestId(
                'firefox-enterprise-mac-menu-link'
            );
            const macEsrMenuLink = page.getByTestId(
                'firefox-enterprise-mac-esr-menu-link'
            );

            await expect(macMenuLink).not.toBeVisible();
            await expect(macEsrMenuLink).not.toBeVisible();

            // open menu
            await macMenuButton.click();

            // Assert macOS menu links are displayed.
            await expect(macMenuLink).toBeVisible();
            await expect(macMenuLink).toHaveAttribute(
                'href',
                /\?product=firefox-latest-ssl&os=osx/
            );
            await expect(macEsrMenuLink).toBeVisible();
            await expect(macEsrMenuLink).toHaveAttribute(
                'href',
                /\?product=firefox-esr-latest-ssl&os=osx/
            );

            // close menu
            await macMenuButton.click();

            // Assert macOS menu links are hidden.
            await expect(macMenuLink).not.toBeVisible();
            await expect(macEsrMenuLink).not.toBeVisible();
        });

        test('Firefox ESR Windows 32bit menu open / close', async ({
            page
        }) => {
            const win32MenuButton = page.getByTestId(
                'firefox-enterprise-win64-menu-button'
            );
            const win32MenuLink = page.getByTestId(
                'firefox-enterprise-win64-menu-link'
            );
            const win32MsiMenuLink = page.getByTestId(
                'firefox-enterprise-win64-msi-menu-link'
            );
            const win32EsrMenuLink = page.getByTestId(
                'firefox-enterprise-win64-esr-menu-link'
            );
            const win32EsrMsiMenuLink = page.getByTestId(
                'firefox-enterprise-win64-esr-msi-menu-link'
            );

            await expect(win32MenuLink).not.toBeVisible();
            await expect(win32MsiMenuLink).not.toBeVisible();
            await expect(win32EsrMenuLink).not.toBeVisible();
            await expect(win32EsrMsiMenuLink).not.toBeVisible();

            // open menu
            await win32MenuButton.click();

            // Assert Windows 32-bit menu links are displayed.
            await expect(win32MenuLink).toBeVisible();
            await expect(win32MenuLink).toHaveAttribute(
                'href',
                /\?product=firefox-latest-ssl&os=win64/
            );
            await expect(win32MsiMenuLink).toBeVisible();
            await expect(win32MsiMenuLink).toHaveAttribute(
                'href',
                /\?product=firefox-msi-latest-ssl&os=win64/
            );
            await expect(win32EsrMenuLink).toBeVisible();
            await expect(win32EsrMenuLink).toHaveAttribute(
                'href',
                /\?product=firefox-esr-latest-ssl&os=win64/
            );
            await expect(win32EsrMsiMenuLink).toBeVisible();
            await expect(win32EsrMsiMenuLink).toHaveAttribute(
                'href',
                /\?product=firefox-esr-msi-latest-ssl&os=win64/
            );

            // close menu
            await win32MenuButton.click();

            // Assert Windows 32-bit menu links are hidden.
            await expect(win32MenuLink).not.toBeVisible();
            await expect(win32MsiMenuLink).not.toBeVisible();
            await expect(win32EsrMenuLink).not.toBeVisible();
            await expect(win32EsrMsiMenuLink).not.toBeVisible();
        });
    }
);
