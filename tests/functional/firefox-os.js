/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/os/2.0/';
var url = config.base() + path;

casper.test.begin('Firefox OS, Elements: ' + url, 11, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertExists('.fxos-cta > h1 > img', 'Firefox OS wordmark exists');
        test.assertExists('.phone-container > img', 'Firefox OS phone image exists');
        test.assertElementCount('.primary-cta-phone', 2, 'Get phone CTA buttons exist');
        test.assertElementCount('.primary-cta-signup', 2, 'Newsletter CTA buttons exist');
        test.assertExists('.cta-button.marketplace', 'Marketplace CTA button exists');
        test.assertElementCount('.fxos-news a', 4, 'Firefox OS news links exist');
        test.assertExists('.fxos-community .more', 'Community learn more links exist');
        test.assertElementCount('.fxos-help a', 7, 'Firefox OS help links exist');
        test.assertExists('#provider-links', 'Provider links exist');
        test.assertExists('#newsletter-form', 'Newsletter form exists');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox OS, Apps for all you do: ' + url, 3, function suite(test) {

    casper.start(url, function() {
        this.click('#connected');
    });

    casper.waitForSelector('#connected.active-state', function() {
        test.assert(true, 'Navigation state updated');
    });

    casper.waitForSelector('.fxos-apps .apps .organized.fade', function() {
        test.assert(true, 'Organized icons faded out');
    });

    casper.waitForSelector('.fxos-apps .apps .entertained.fade', function() {
        test.assert(true, 'Entertained icons faded out');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox OS, Newsletter modal: ' + url, 3, function suite(test) {

    casper.start(url, function() {
        this.click('.primary-cta-signup');
    });

    casper.waitUntilVisible('#modal', function() {
        test.assert(true, 'Modal opened successfully');
        test.assertExists('#modal #newsletter-form');
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

casper.test.begin('Firefox OS, Get phone modal: ' + url, 3, function suite(test) {

    casper.start(url, function() {
        this.click('.primary-cta-phone');
    });

    casper.waitUntilVisible('#modal', function() {
        test.assert(true, 'Modal opened successfully');
        test.assertExists('#modal #get-device');
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
