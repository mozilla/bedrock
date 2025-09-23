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
    '/en-US/',
    '/en-US/about/',
    '/en-US/about/governance/policies/participation/',
    '/en-US/about/leadership/',
    '/en-US/about/manifesto/',
    '/en-US/advertising/',
    '/en-US/careers/',
    '/en-US/careers/benefits/',
    '/en-US/careers/diversity/',
    '/en-US/careers/listings/',
    '/en-US/careers/locations/',
    '/en-US/careers/teams/',
    '/en-US/contact/',
    '/en-US/contribute/',
    '/en-US/firefox/download/thanks/',
    '/en-US/privacy/',
    '/en-US/privacy/websites/cookie-settings/',
    '/en-US/products/',
    '/en-US/products/vpn/',
    '/en-US/products/vpn/download/',
    '/en-US/products/vpn/features/',
    '/en-US/products/vpn/pricing/'
];

const mobileTestURLs = ['/en-US/'];

module.exports = { desktopTestURLs, mobileTestURLs };
