/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/sync/';
var url = config.base() + path;

casper.test.begin('Firefox Sync, Elements: ' + url, 7, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);

        test.assertVisible('#newsletter-form', 'Newsletter form visible');
        test.assertVisible('.cta', 'The CTA is visible');
        test.assertVisible('#cta-android-footer', 'Download Fx for Android button visible');
        test.assertElementCount('.secondary .features div', 3, 'List of three feature exists');
    });

    casper.waitForSelector('.sync-anim.on', function() {
        test.assert(true, 'Sync animation visible and playing');
    });

    casper.waitForSelector('.sync-anim.on.complete', function() {
        test.assert(true, 'Sync animation completed');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Sync, Messaging Firefox: ' + url, 1, function suite(test) {

    casper.userAgent(config.userAgent.fx);

    casper.start();

    casper.thenOpen(url, function() {
        test.assertVisible('.primary .show-default.instructions', 'Default Sync instructions visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Sync, Messaging Fx28: ' + url, 2, function suite(test) {

    casper.userAgent(config.userAgent.fx28);

    casper.start();

    casper.thenOpen(url, function() {
        test.assertVisible('.primary .show-fx-28-older.warning', 'Fx < 28 messaging shown');
        test.assertVisible('.buttons .show-fx-28-older #cta-firefox', 'Firefox download button visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Sync, Firefox on Android: ' + url, 1, function suite(test) {

    casper.userAgent(config.userAgent.fxAndroid);

    casper.start();

    casper.thenOpen(url, function() {
        test.assertVisible('.primary .show-fx-android.instructions', 'Fx on Android instructions shown');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Sync, iOS: ' + url, 1, function suite(test) {

    casper.start(url).thenEvaluate(function() {
        document.documentElement.className = 'ios js loaded';
    }).then(function() {
        test.assertVisible('.primary .show-ios.warning', 'iOS messaging shown');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Sync, Not Fx: ' + url, 2, function suite(test) {

    casper.userAgent(config.userAgent.chrome);

    casper.start();

    casper.thenOpen(url, function() {
        test.assertVisible('.primary .show-not-fx.warning', 'Not Fx messaging shown');
        test.assertVisible('.primary .buttons #download-button-desktop-release', 'Download button visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
