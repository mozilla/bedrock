/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const fs = require('fs').promises;

/**
 * Clean up /test-results-a11y/ directory before running tests.
 */
async function cleanA11yReportDir() {
    const dir = 'test-results-a11y/';
    try {
        const stats = await fs.stat(dir);
        if (stats.isDirectory()) {
            await fs.rm(dir, { recursive: true, force: true });
        }
    } catch (err) {
        if (err.code !== 'ENOENT') {
            throw err;
        }
    }

    await fs.mkdir(dir);
}

async function globalSetup() {
    await cleanA11yReportDir();
}

module.exports = globalSetup;
