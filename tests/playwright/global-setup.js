/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const fs = require('fs');

/**
 * Clean up /a11y-report/ directory before running tests.
 */
function cleanA11yReportDir() {
    const dir = 'a11y-report/';
    if (fs.existsSync(dir)) {
        fs.rmdirSync(dir, {
            recursive: true
        });
    }

    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir);
    }
}

function globalSetup() {
    cleanA11yReportDir();
}

module.exports = globalSetup;
