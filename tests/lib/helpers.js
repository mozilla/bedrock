/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');

function done() {
    casper.options.pageSettings.userAgent = config.userAgent.phantomjs;
    casper.options.viewportSize = config.viewport.desktop;
    casper.options.waitTimeout = 5000;
}

module.exports = {
    done: done
};
