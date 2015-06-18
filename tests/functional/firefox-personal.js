/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/personal/';
var url = config.base() + path;

casper.test.begin('Firefox Personal, Elements: ' + url, 5, function suite(test) {
    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertVisible('#download-button-desktop-release');
        test.assertElementCount('main .mission', 3, 'There are three mission items');

        test.assertNotVisible('#masthead .android-download', 'Android download button not visible');
        test.assertNotVisible('section.android-download', 'Second Android download button not visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Personal, Android', 4, function suite(test) {

    casper.start();

    casper.userAgent(config.userAgent.android);
    casper.options.viewportSize = config.viewport.mobileLandscape;

    casper.thenOpen(url, function() {
        test.assertVisible('#masthead .android-download', 'Android download button visible in masthead');
        test.assertVisible('section.android-download', 'Android download button visible above footer');
        test.assertNotVisible('#download-button-desktop-release', 'Firefox desktop download button not visible');
        test.assertExists('section.android-download p', 'Android download messaging exists');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });

});
