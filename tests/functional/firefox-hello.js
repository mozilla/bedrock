/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/hello/';
var url = config.base() + path;

casper.test.begin('Firefox Hello, Elements: ' + url, 6, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertExists('#fxfamilynav-header', 'Family navigation exists');
        test.assertElementCount('.try-hello', 3, 'Try Hello buttons exist');
        test.assertExists('#features ul li', 'Hello features exist');
        test.assertExists('#video-link', 'Hello Video exists');
        test.assertExists('.download-button', 'Download button exists');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Hello, Video modal: ' + url, 3, function suite(test) {

    casper.start(url, function() {
        this.click('#video-link');
    });

    casper.waitUntilVisible('#modal', function() {
        test.assert(true, 'Modal opened successfully');
        test.assertExists('#modal #hello-video', 'Video is displayed in modal');
        this.click('#modal-close');
    });

    casper.waitWhileVisible('#modal', function() {
        test.assert(true, 'Modal closed successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Hello, Firefox users: ' + url, 4, function suite(test) {

    casper.start();

    casper.userAgent(config.userAgent.fx);

    casper.thenOpen(url, function() {
        test.assertExists('#feature-account', 'Fx Accounts feature visible');
        test.assertNotVisible('#feature-getfx', 'Get Firefox feature not visible');
        test.assertNotVisible('.download-button', 'Download button not visible');
        test.assertVisible('#try-hello-footer', 'Try Hello button visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Hello, non-Firefox users: ' + url, 3, function suite(test) {

    casper.start();

    casper.userAgent(config.userAgent.chrome);

    casper.thenOpen(url, function() {
        test.assertNotExists('#feature-account', 'Fx Accounts feature not visible');
        test.assertVisible('#feature-getfx', 'Get Firefox feature visible');
        test.assertVisible('.download-button', 'Download button visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Hello, old-Firefox users: ' + url, 2, function suite(test) {

    casper.start();

    casper.userAgent(config.userAgent.fxOutdated);

    casper.thenOpen(url, function() {
        test.assertVisible('#ctacopy-oldfx', 'Outdated messaging visible');
        test.assertVisible('.download-button', 'Download button visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
