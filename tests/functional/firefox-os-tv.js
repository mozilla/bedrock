/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/os/devices/tv/';
var url = config.base() + path;

casper.test.begin('Firefox OS TV, Elements: ' + url, 7, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertExists('#main-content > .pager', 'Pager Exists');
    });

    casper.waitForSelector('.pager.pager-initialized', function() {
        test.assert(true, 'Pager initialized');
        test.assertExists('.pager-nav .pager-next', 'Pager next button exists');
        test.assertExists('.pager-nav .pager-prev', 'Pager prev button exists');
        test.assertElementCount('.pager-tabs > li > a', 4, 'Pager tabs exist');
        test.assertVisible('#page-tv1', 'First page is visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox OS TV, Click next: ' + url, 4, function suite(test) {

    casper.open(url);

    casper.waitUntilVisible('.pager.pager-initialized', function() {
        test.assertVisible('#page-tv1', 'First page is visible');
        test.assertNotVisible('#page-tv2', 'Second page is not visible');
        this.click('.pager-nav .pager-next');
    });

    casper.waitUntilVisible('#page-tv2', function() {
        test.assert(true, 'Second page is visible after clicking next');
        test.assertNotVisible('#page-tv1', 'First page is no longer visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox OS TV, Click tab: ' + url, 4, function suite(test) {

    casper.open(url);

    casper.waitUntilVisible('.pager.pager-initialized', function() {
        test.assertVisible('#page-tv1', 'First page is visible');
        test.assertNotVisible('#page-tv3', 'Third page is not visible');
        this.click('#tv3-tab');
    });

    casper.waitUntilVisible('#page-tv3', function() {
        test.assert(true, 'Third page is visible after clicking next');
        test.assertNotVisible('#page-tv1', 'First page is no longer visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
