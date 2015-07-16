/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/windows-10/welcome/';
var url = config.base() + path;

casper.test.begin('Win 10 Welcome, Elements: ' + url, 4, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertVisible('.main-header', 'Heading is visible');
        test.assertExists('.firefox-default-cta', 'Default CTA exists');
        test.assertElementCount('.firefox-learn-links > ul > li > a', 3, '3 Learn more links exist');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Win 10 Welcome, Non Firefox: ' + url, 2, function suite(test) {

    casper.userAgent(config.userAgent.chrome);

    casper.start();

    casper.thenOpen(url, function() {
        test.assertNotVisible('.firefox-default-cta', 'Default CTA is not visible');
        test.assertVisible('.firefox-learn-links', 'Learn more links are visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
