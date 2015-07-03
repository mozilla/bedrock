/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/about/history/';
var url = config.base() + path;

casper.test.begin('History, Elements: ' + url, 7, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertExists('#slideshow-stage', 'Slideshow stage exists');
        test.assertElementCount('.links li a', 6, 'Six content links exist');
        test.assertVisible('#mozorg-newsletter-form', 'Newsletter is visible');
    });

    casper.waitForSelector('#slideshow.on', function() {
        test.assert(true, 'Slideshow initialized');
        test.assertExists('#slideshow .slide-control > .prev', 'Prev button exists');
        test.assertExists('#slideshow .slide-control > .next', 'Next button exists');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
