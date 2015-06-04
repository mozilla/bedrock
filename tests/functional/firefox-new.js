/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/new/';
var url = config.base() + path;

casper.test.begin('Firefox New, Elements: ' + url, 4, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertVisible('#features-download .download-button', 'Download button exists');
        test.assertExists('#direct-download-link', 'Direct download link exists');
        test.assertVisible('#firefox-screenshot > img', 'Browser screenshot exists');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox New, Direct download link: ' + url, 1, function suite(test) {

    casper.start(url, function() {
        var href = this.getElementAttribute('#direct-download-link', 'href');
        test.assert(href.indexOf('https://download.mozilla.org/') !== -1, 'Download link has a valid URL');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox New, Click download button: ' + url, 1, function suite(test) {

    casper.start(url, function() {
        this.click('#features-download .download-link');
    });

    casper.waitForResource(/https:\/\/download\.mozilla\.org\//, function() {
        test.assert(true, 'Download started successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
