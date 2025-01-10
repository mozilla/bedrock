/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const fs = require('fs');
const { AxeBuilder } = require('@axe-core/playwright');
const { createHtmlReport } = require('axe-html-reporter');
const {
    navigationLocator,
    footerLocator,
    sideMenuLocator,
    subNavigationLocator
} = require('./locators');

/**
 * Create an a11y report file.
 * Report will be saved in `./tests/playwright/test-results-a11y/`.
 * @param {string} slug
 * @param {string} type
 * @param {Object} results JSON object
 */
function createReport(slug, type, results) {
    // Only create a report if there were violations.
    if (results.violations.length === 0) {
        return;
    }

    const fileName = `results-${slug.replaceAll('/', '-').toLowerCase()}-${type}.html`;
    const reportHTML = createHtmlReport({
        results: results,
        options: {
            projectKey: `${slug} (${type})`,
            doNotCreateReportFile: true
        }
    });

    fs.writeFileSync(`test-results-a11y/${fileName}`, reportHTML);
}

/**
 * Scan a whole page for a11y issues.
 * Exclude global elements such as navigation and footer.
 * @param {Object} page
 * @returns {Promise} results
 */
async function scanPage(page) {
    return await new AxeBuilder({ page })
        .exclude(navigationLocator)
        .exclude(footerLocator)
        .exclude(sideMenuLocator)
        .exclude(subNavigationLocator)
        .analyze();
}

/**
 * Scan a specific element on the page for a11y issues.
 * @param {Object} page
 * @returns {Promise} results
 */
async function scanPageElement(page, locator, disabledRules) {
    if (disabledRules) {
        return new AxeBuilder({ page })
            .include(locator)
            .disableRules(disabledRules)
            .analyze();
    }
    return new AxeBuilder({ page }).include(locator).analyze();
}

module.exports = { createReport, scanPage, scanPageElement };
