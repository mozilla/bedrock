/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/products/';
var url = config.base() + path;

casper.test.begin('Firefox Products, Elements: ' + url, 4, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertElementCount('#products-primary .product-list li', 3, 'There are three products in the list');
        test.assertVisible('#product-android .btn-google-play', 'The Google play download button is visible');
        // there will always be some secondary products but, they will not always be the same
        // products nor always the same number so, just check that a list of products exist.
        test.assertExists('#products-secondary .product-list', 'List of secondary products exist');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });

});

casper.test.begin('Firefox Products, Outdated Fx: ' + url, 2, function suite(test) {

    casper.start();

    casper.userAgent(config.userAgent.fxOutdated);

    casper.thenOpen(url, function() {
        test.assertVisible('#dlbar-oldfx-desktop', 'Old Firefox message shown');
        test.assertVisible('#dlbar-oldfx-desktop .btn-download', 'Download button exists.');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });

});

casper.test.begin('Firefox Products, Non-Fx: ' + url, 2, function suite(test) {

    casper.start();

    casper.userAgent(config.userAgent.chrome);

    casper.thenOpen(url, function() {
        test.assertVisible('#dlbar-nonfx', 'NonFx message shown');
        test.assertVisible('#dlbar-nonfx .btn-download', 'Download button exists.');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });

});

casper.test.begin('Firefox Products, Android: ' + url, 1, function suite(test) {

    casper.start();

    casper.userAgent(config.userAgent.android);

    casper.thenOpen(url, function() {
        test.assertVisible('#dlbar-nonfx-android', 'Firefox for Android message shown');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });

});

casper.test.begin('Firefox Products, iOS: ' + url, 1, function suite(test) {

    casper.start(url).thenEvaluate(function() {
        document.documentElement.className = 'ios js loaded';
    });

    casper.waitUntilVisible('#dlbar-ios', function() {
        test.assert(true, 'iOS messaging shown');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });

});

casper.test.begin('Firefox Products, Download bar close: ' + url, 2, function suite(test) {

    casper.start();

    casper.userAgent(config.userAgent.android);

    casper.thenOpen(url, function() {
        test.assertVisible('#conditional-download-bar .btn-close', 'Close button visible');
        this.click('#conditional-download-bar .btn-close');
    });

    casper.waitWhileVisible('#conditional-download-bar', function() {
        test.assert(true, 'Conditional download bar removed');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });

});
