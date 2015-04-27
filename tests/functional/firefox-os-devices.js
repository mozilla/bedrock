/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/os/devices/';
var url = config.base() + path;

casper.test.begin('Firefox OS Devices, Elements: ' + url, 7, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertExists('#location', 'Location picker exists');
        test.assertExists('#device-nav', 'Device navigation exists');
        test.assertExists('#smartphones', 'Smartphone section exists');
        test.assertExists('#tvs', 'Television section exists');
        test.assertExists('#provider-links', 'Provider links exist');
        test.assertElementCount('.purchase-button', 2, 'Purchase buttons exist');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox OS Devices, Click phone: ' + url, 2, function suite(test) {

    casper.start(url, function() {
        this.click('a[href="#alcatel_onetouchfire"]');
    });

    casper.waitUntilVisible('#alcatel_onetouchfire', function() {
        test.assert(true, 'Phone detail expanded successfully');
        this.click('#alcatel_onetouchfire .device-detail-close');
    });

    casper.waitWhileVisible('#alcatel_onetouchfire', function() {
        test.assert(true, 'Phone detail collapsed successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox OS Devices, Click tab navigation: ' + url, 1, function suite(test) {

    casper.start(url, function() {
        this.click('a[href="#alcatel_onetouchfire"]');
    });

    casper.waitUntilVisible('#alcatel_onetouchfire-specifications-tab', function() {
        this.click('#alcatel_onetouchfire-specifications-tab');
    });

    casper.waitUntilVisible('#page-alcatel_onetouchfire-specifications', function() {
        test.assert(true, 'Phone specs shown successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox OS Devices, Purchase modal: ' + url, 3, function suite(test) {

    casper.start(url, function() {
        this.fillSelectors('#form-locations', {
            '#location': 'ar'
        });
        this.click('.purchase-button');
    });

    casper.waitUntilVisible('#modal', function() {
        test.assert(true, 'Purchase modal opened successfully');
        test.assertExists('#modal #get-device');
        this.click('#modal-close');
    });

    casper.waitWhileVisible('#modal', function() {
        test.assert(true, 'Purchase modal closed successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
