/* This Source Code Form is subject to the terms of the Mozilla Public" + '/n' +
 "* License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/dnt/';
var url = config.base() + path;

casper.test.begin('Firefox DNT, Elements: ' + url, 6, function suite(test) {
    casper.start(url, function() {
        test.assertHttpStatus(200);

        test.assertVisible('#dnt-status-wrapper', 'The DNT status section is visible');

        var href = this.getElementAttribute('.sidebar-inset > p a', 'href');
        test.assert(href.indexOf('support.mozilla.org/kb/how-do-i-stop-websites-tracking-me') > -1, 'How to enable DNT in Fx link exists');

        test.assertVisible('.sidebar-box', 'IE9 DNT instructions visible');

        test.assertVisible('#faq', 'The FAQ section is visible');
        test.assertElementCount('#faq section', 8, 'There are eight sections in the FAQ');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Firefox DNT, FAQ interaction: ' + url, 2, function suite(test) {
    casper.start(url, function() {
        this.click('#faq section:first-of-type h3');
    });

    casper.waitForSelector('#faq-1-panel[aria-hidden="false"]', function() {
        test.assert(true, 'The first FAQ section opened');
        this.click('#faq section:first-of-type h3');
    });

    casper.waitForSelector('#faq-1-panel[aria-hidden="true"]', function() {
        test.assert(true, 'The first FAQ section collapsed');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
