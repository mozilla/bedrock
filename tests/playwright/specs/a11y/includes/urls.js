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
const desktopTestURLs = ['/en-US/firefox/', '/en-US/firefox/new/'];

const mobileTestURLs = ['/en-US/firefox/', '/en-US/firefox/new/'];

module.exports = { desktopTestURLs, mobileTestURLs };
