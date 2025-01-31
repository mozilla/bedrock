/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

/**
 * URL paths for inclusion in page-level a11y scans.
 * Pages will be scanned at both desktop and mobile resolutions.
 */
const desktopTestURLs = [
    '/en-US/firefox/',
    '/en-US/firefox/channel/android/',
    '/en-US/firefox/channel/desktop/',
    '/en-US/firefox/developer/',
    '/en-US/firefox/download/',
    '/en-US/firefox/download/all/',
    '/en-US/firefox/download/thanks/',
    '/en-US/firefox/enterprise/',
    '/en-US/firefox/releasenotes/',
    '/en-US/privacy/websites/cookie-settings/'
];

const mobileTestURLs = [
    '/en-US/firefox/',
    '/en-US/firefox/channel/android/',
    '/en-US/firefox/download/'
];

module.exports = { desktopTestURLs, mobileTestURLs };
