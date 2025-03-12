/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

if (window.location.hash === '#health-report') {
    window.location.replace(
        'https://support.mozilla.org/kb/technical-and-interaction-data'
    );
}

if (window.location.hash === '#crash-reporter') {
    window.location.replace(
        'https://support.mozilla.org/en-US/kb/crash-report'
    );
}
