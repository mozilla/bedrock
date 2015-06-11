/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

 /* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/os/2.0/';
var url = config.base() + path;

casper.test.begin('Family Navigation, Elements: ' + url, 6, function suite(test) {

    casper.start(url, function() {
        test.assertVisible('#fxfamilynav-primary > li > a', 'Primary navigation links are visible');
        test.assertVisible('.primary-link.selected[data-id="os"]', 'Firefox OS primary link is set as default');
        test.assertVisible('#os-subnav a.selected[data-id="os-index"]', 'Firefox OS secondary links are visible');
        test.assertNotVisible('#fxfamilynav-tertiarynav', 'Tertiary navigation is not visible');
        test.assertVisible('#fxfamilynav-tertiarynav-trigger', 'Tertiary trigger is not visible');
        test.assertExists('#fxfamilynav-cta-wrapper .primary-cta-phone', 'CTA button is inserted into navigation');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Family Navigation, Open tertiary link menu: ' + url, 1, function suite(test) {

    casper.start(url, function() {
        this.mouse.click('#fxfamilynav-tertiarynav-trigger');
    });

    casper.waitUntilVisible('#fxfamilynav-tertiarynav', function() {
        test.assert(true, 'Tertiary links opened successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Family Navigation, Link hover: ' + url, 2, function suite(test) {

    casper.start(url, function() {
        this.mouse.move('#fxfamilynav-primary > li > a[data-id="android"]');
    });

    casper.waitUntilVisible('#android-subnav', function() {
        test.assert(true, 'Secondary nav shows on hover');
        this.mouse.move(0,0);
    });

    casper.waitWhileVisible('#android-subnav', function() {
        test.assert(true, 'Secondary nav hides on leave');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Family Navigation, Scroll down: ' + url, 2, function suite(test) {

    casper.start(url, function() {
        this.scrollToBottom();
    });

    casper.waitForSelector('#fxfamilynav-header.stuck', function() {
        test.assert(true, 'Navigation is sticky when scrolled');
        var buttonVisibility = this.evaluate(function() {
            return $('#fxfamilynav-cta-wrapper').css('visibility') === 'visible';
        });
        test.assertTrue(buttonVisibility, 'CTA button is visible when scrolled');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Family Navigation, Scroll up: ' + url, 2, function suite(test) {

    casper.start(url, function() {
        this.scrollToBottom();
    });

    casper.waitForSelector('#fxfamilynav-header.stuck', function() {
        this.scrollTo(0,0);
    });

    casper.waitWhileSelector('#fxfamilynav-header.stuck', function() {
        test.assert(true, 'Navigation is no longer sticky when scrolled back to top');
        var buttonVisibility = this.evaluate(function() {
            return $('#fxfamilynav-cta-wrapper').css('visibility') === 'visible';
        });
        test.assertFalsy(buttonVisibility, 'CTA button is no longer visible when scrolled up');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Family Navigation, Mobile interaction: ' + url, 4, function suite(test) {

    casper.options.viewportSize = config.viewport.mobile;

    casper.start(url, function() {
        this.scrollToBottom();
    });

    casper.then(function() {
        test.assertDoesntExist('#fxfamilynav-header.stuck', 'Navigation is not sticky when scrolled');
        test.assertNotVisible('#fxfamilynav-primary > li > .subnav', 'Sub navigation is not visible');
        test.assertNotVisible('#fxfamilynav-tertiarynav', 'Tertiary navigation is not visible');
        test.assertNotVisible('#fxfamilynav-tertiarynav-trigger', 'Tertiary trigger is not visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
