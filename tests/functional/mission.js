/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/mission/';
var url = config.base() + path;

casper.test.begin('Mission, Elements: ' + url, 7, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);

        test.assertVisible('#mosaic', 'The hero area mosiac is visible');
        test.assertExists('#main-content > h1', 'The main page heading exists');
        test.assertVisible('#welcome-video', 'The welcome video is visible');
        test.assertVisible('#welcome-video a', 'The video overlay/click target is visible');
        test.assertElementCount('#main-content .links li', 4, 'List of four links to additional content');
        test.assertVisible('#mozorg-newsletter-form', 'Newsletter form is visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
