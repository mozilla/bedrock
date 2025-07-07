/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const { defineConfig, devices } = require('@playwright/test');

// Read environment variables from file.
require('dotenv').config({
    path: '../../.env',
    quiet: true
});

// Default desktop viewport size for tests.
const desktopViewportSize = {
    width: 1280,
    height: 720
};

/**
 * @see https://playwright.dev/docs/test-configuration
 */
module.exports = defineConfig({
    /* Global setup file to prepare the environment for the test run. */
    globalSetup: require.resolve('./global-setup'),
    testDir: './specs',
    /* Run tests in files in parallel */
    fullyParallel: true,
    /* Fail the build on CI if you accidentally left test.only in the source code. */
    forbidOnly: !!process.env.CI,
    /* Retry on CI only */
    retries: process.env.CI ? 2 : 0,
    /* Opt out of parallel tests on CI. */
    workers: process.env.CI ? 2 : undefined,
    /* Reporter to use. See https://playwright.dev/docs/test-reporters */
    reporter: process.env.CI ? 'github' : 'line',
    /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
    use: {
        /* Base URL to use in actions like `await page.goto('/')`. */
        baseURL: process.env.PLAYWRIGHT_BASE_URL
            ? process.env.PLAYWRIGHT_BASE_URL
            : 'http://localhost:8000',

        /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
        trace: 'on-first-retry'
    },

    /* Configure projects for major browsers */
    projects: [
        {
            name: 'chromium',
            use: {
                ...devices['Desktop Chrome'],
                viewport: desktopViewportSize
            }
        },

        {
            name: 'firefox',
            use: {
                ...devices['Desktop Firefox'],
                viewport: desktopViewportSize
            }
        },

        {
            name: 'webkit',
            use: {
                ...devices['Desktop Safari'],
                viewport: desktopViewportSize
            }
        }
    ]
});
