/* This Source Code Form is subject to the terms of the Mozilla Public" + '/n' +
 "* License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/partners/';
var url = config.base() + path;

casper.test.begin('Firefox Partners, Elements: ' + url, 11, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);
    });

    casper.waitUntilVisible('#article-wrapper', function() {

        test.assertVisible('#partner-menu', 'The partner menu is visible');
        test.assertVisible('#mwc-menu', 'The MWC menu is visible');
        test.assertVisible('#devices-menu', 'The devices menu is visible');

        var devicesHref = this.getElementAttribute('#menu-devices a', 'href');
        test.assert(devicesHref.indexOf('firefox/os/devices') > -1, 'Link to devices page is as expected');
        test.assertExist('.partner-logos', 'The partner logos exist');
        test.assertExists('.partner-button', 'The "Be a partner" button exists');

        var href = this.getElementAttribute('.partner-button a', 'href');
        test.assert(href.indexOf('mobilepartners.mozilla.org') > -1, 'The partner button links to the correct endpoint');

        test.assertElementCount('#article-wrapper article', 4, 'There are four content sections');
    });

    casper.waitUntilVisible('#screen-overview', function() {
        test.assert(true, 'The overview screen image is visible');
        test.assertNotVisible('#screen-os', 'The OS screen image is not visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Partners, OS Section: ' + url, 4, function suite(test) {

    casper.start(url);

    casper.waitUntilVisible('#article-wrapper', function() {
        this.click('#menu-os a');
    });

    casper.waitUntilVisible('#screen-os', function() {
        test.assert(true, 'The correct phone image is visible');
        test.assertElementCount('#os nav a', 2, 'There are two navigation elements');

        var current = this.getElementAttribute('#os-overview', 'data-current');
        test.assert(current === '1', 'The overview is visible by default');

        this.click('#os nav a:last-child');

        current = this.getElementAttribute('#os-operators', 'data-current');
        test.assert(current === '1', 'The operators section is visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Partners, Marketplace Section: ' + url, 8, function suite(test) {

    casper.start(url);

    casper.waitUntilVisible('#article-wrapper', function() {
        this.click('#menu-marketplace a');
    });

    casper.waitUntilVisible('#screen-marketplace', function() {
        test.assert(true, 'The correct phone image is visible');
        test.assertElementCount('#marketplace nav a', 3, 'There are three navigation elements');

        var current = this.getElementAttribute('#marketplace-overview', 'data-current');
        test.assert(current === '1', 'The overview is visible by default');

        test.assertExists('.promo-testimonials', 'The testimonials are exist');
        test.assertExists('.promo-conversation', 'The social links are exist');

        this.click('#marketplace nav a:nth-child(2)');

        current = this.getElementAttribute('#marketplace-operators', 'data-current');
        test.assert(current === '1', 'The operators section is visible');
        test.assertExists('.marketplace-logos', 'The marketplace logos exist');

        this.click('#marketplace nav a:last-child');

        current = this.getElementAttribute('#marketplace-developers', 'data-current');
        test.assert(current === '1', 'The developers section is visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Partners, Fx Android Section: ' + url, 4, function suite(test) {

    casper.start(url);

    casper.waitUntilVisible('#article-wrapper', function() {
        this.click('#menu-android a');
    });

    casper.waitForSelector('#android .android-phone-visible', function() {
        test.assert(true, 'Page scrolled Fx Android section into view');
        test.assertElementCount('#android nav a', 2, 'There are two navigation elements');

        var current = this.getElementAttribute('#android-overview', 'data-current');
        test.assert(current === '1', 'The overview is visible by default');

        this.click('#android nav a:last-child');

        current = this.getElementAttribute('#android-partner', 'data-current');
        test.assert(current === '1', 'The partner section is visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Partners, MWC Map Modal: ' + url, 2, function suite(test) {

    casper.start(url);

    casper.waitUntilVisible('#article-wrapper', function() {
        this.click('#menu-mwc-map a');
    });

    casper.waitUntilVisible('#modal #map', function() {
        test.assert(true, 'The modal with the MWC map opened');
        this.click('#modal-close button');
    });

    casper.waitWhileVisible('#modal', function() {
        test.assert(true, 'The map modal closed');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox Partners, MWC Schedule Modal: ' + url, 2, function suite(test) {

    casper.start(url);

    casper.waitUntilVisible('#article-wrapper', function() {
        this.click('#menu-mwc-schedule a');
    });

    casper.waitUntilVisible('#modal #schedule', function() {
        test.assert(true, 'The modal with the MWC schedule opened');
        this.click('#modal-close button');
    });

    casper.waitWhileVisible('#modal', function() {
        test.assert(true, 'The schedule modal closed');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
