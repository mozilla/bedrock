/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var domain = casper.cli.get('domain') || 'http://localhost:8000';
var locale = casper.cli.get('locale') || 'en-US';

// common sandstone breakpoints for bedrock
var viewport = {
    desktopWide: { width: 1400, height: 840},
    desktop: { width: 1000, height: 600 },
    tablet: { width: 760, height: 456 },
    mobileLandscape: { width: 480, height: 300 },
    mobile: { width: 320, height: 460 }
};

// set default viewport size to desktop
casper.options.viewportSize = viewport.desktop;

/*
 * Returns the environment being tested
 * plus the specified locale.
 * e.g. 'http://localhost:8000/en-US'
 */
function base() {
    return domain + '/' + locale;
}

module.exports = {
    base: base,
    locale: locale,
    domain: domain,
    viewport: viewport
};
