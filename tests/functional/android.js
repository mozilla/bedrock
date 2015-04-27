/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/android/';
var url = config.base() + path;

casper.test.begin('Android, Elements: ' + url, 6, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertElementCount('.send-to', 3, '3 modal buttons exist');
        test.assertElementCount('.dl-button', 3, '3 Google Play Store buttons exist');
        test.assertExists('#customize-accordion', 'Customize accordion exists');
        test.assertElementCount('#privacy ul li > a', 4, 'Privacy links exist');
        test.assertExists('#newsletter-form', 'Newsletter form exists');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Android, Expand accordion: ' + url, 2, function suite(test) {

    casper.start(url, function() {
        test.assertNotVisible('#addons-panel', 'Addons accordion panel is closed initially');
        this.click('#addons-header');
    });

    casper.waitUntilVisible('#addons-panel', function() {
        test.assert(true, 'Addons accordion panel opened successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Android, Accordion navigation: ' + url, 4, function suite(test) {

    casper.start(url, function() {
        test.assertNotVisible('#addons-panel', 'Addons accordion panel is closed initially');
        this.click('#customize-next');
    });

    casper.waitUntilVisible('#addons-panel', function() {
        test.assert(true, 'Addons accordion panel opened successfully');
        this.wait(1000, function() {
            this.click('#customize-prev');
        });
    });

    casper.waitUntilVisible('#broadcast-panel', function() {
        test.assert(true, 'Broadcast accordion panel opened successfully');
        test.assertNotVisible('#addons-panel', 'Addons accordion panel closed again');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Android, Send to device modal: ' + url, 3, function suite(test) {

    casper.start(url, function() {
        this.click('#intro .send-to');
    });

    casper.waitUntilVisible('#modal', function() {
        test.assert(true, 'Modal opened successfully');
        test.assertExists('#modal #send-to-device-form', 'Send to device form is displayed in modal');
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

casper.test.begin('Android, Send to device form submission: ' + url, 2, function suite(test) {

    casper.start(url, function() {
        this.click('#intro .send-to');
    });

    casper.waitUntilVisible('#modal #send-to-device-form', function() {
        test.assertNotVisible('#modal #send-to-device-form .thank-you', 'Thank you message is not visible initially');
        this.fillSelectors('#modal #send-to-device-form', {
            '#id-input': 'noreply@mozilla.com'
        }, true);
    });

    casper.waitUntilVisible('#modal #send-to-device-form .thank-you', function() {
        test.assert(true, 'Send to device form submitted successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
