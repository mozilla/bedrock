/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

if (window.location.hash.indexOf('#health-report') === 0) {
    window.location.replace(
        'https://support.mozilla.org/kb/technical-and-interaction-data'
    );
}

if (window.location.hash.indexOf('#crash-reporter') === 0) {
    window.location.replace('https://support.mozilla.org/kb/crash-report');
}
