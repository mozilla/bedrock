/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/developer/';
var url = config.base() + path;

casper.test.begin('Firefox Developer, Elements: ' + url, 7, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertElementCount('.download-button', 2, '2 download buttons exist');
        test.assertExists('.screenshot', 'Browser screenshot exists');
        test.assertExists('.intro-features li', 'Intro features exist');
        test.assertExists('.feature-overview .features .feature', 'Features overview exists');
        test.assertExists('#newsletter-form', 'Newsletter form exists');
        test.assertExists('.mozilla-share-cta', 'Share CTA exists');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Developer, Click download button: ' + url, 1, function suite(test) {

    casper.start(url, function() {
        this.click('.intro .download-button .os_win .download-link');
    });

    casper.waitForResource(/https:\/\/download\.mozilla\.org\//, function() {
        test.assert(true, 'Download started successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Developer, Open video modal: ' + url, 3, function suite(test) {

    casper.start(url, function() {
        this.click('.video-play:nth-of-type(1)');
    });

    casper.waitUntilVisible('#modal', function() {
        test.assert(true, 'Modal opened successfully');
        test.assertExists('#modal .responsive-video-container', 'Video is displayed in modal');
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
