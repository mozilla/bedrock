/* This Source Code Form is subject to the terms of the Mozilla Public" + '/n' +
 "* License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/styleguide/';
var url = config.base() + path;

casper.test.begin('Styleguide, Elements: ' + url, 2, function suite(test) {
    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertVisible('#sidebar', 'The sidebar navigation is visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Styleguide, Sidebar interaction: ' + url, 5, function suite(test) {

    casper.start(url, function() {
        this.click('nav > ul > li:nth-child(2) a');
    });

    casper.waitUntilVisible('nav > ul > li:nth-child(2) > ul', function() {
        test.assert(true, 'Secondary links revealed');
        this.click('nav > ul > li:nth-child(2) > ul > li:first-child a');
    });

    casper.waitUntilVisible('nav > ul > li:nth-child(2) > ul > li:first-child ul', function() {
        test.assert(true, 'Tertiary links revealed');
        var href = this.getElementAttribute('nav > ul > li:nth-child(2) > ul > li:first-child ul li:first-child a', 'href');
        test.assert(href.indexOf('/styleguide/identity/mozilla/branding/') !== -1, 'Link correctly points to branding page');
        this.click('nav > ul > li:nth-child(2) > ul > li:first-child a');
    });

    casper.waitWhileVisible('nav > ul > li:nth-child(2) > ul > li:first-child ul', function() {
        test.assert(true, 'Tertiary level items hidden');
        this.click('nav > ul > li:nth-child(2) a');
    });

    casper.waitWhileVisible('nav > ul > li:nth-child(2) > ul', function() {
        test.assert(true, 'Secondary level navigation elements hidden');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Styleguide, Firefox OS: ' + url + 'products/firefox-os/', 5, function suite(test) {
    casper.start(url + 'products/firefox-os/', function() {
        test.assertHttpStatus(200);

        test.assertVisible('#basics ol', 'The list of links are visible');
        test.assertExists('#list ol li:first-child img', 'Shape forms image exists');
        test.assertVisible('#examples', 'The example screen shots area is visible');
        test.assertElementCount('#examples figure', 3, 'There are three examples');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Styleguide, Firefox OS color pallette: ' + url + 'products/firefox-os/color/', 8, function suite(test) {
    casper.start(url + 'products/firefox-os/color/', function() {
        test.assertHttpStatus(200);

        test.assertVisible('#main_colors', 'Main colors section is visible');
        test.assertVisible('#all_colors', 'All colors section is visible');
        test.assertVisible('#recommended_gradients', 'Recommended gradients section is visible');

        test.assertVisible('#examples', 'Examples section is visible');
        test.assertElementCount('#examples figure', 13, 'There are thirteen examples in the section');

        test.assertVisible('#downloads', 'Download section visible');
        var href = this.getElementAttribute('#downloads a', 'href');
        test.assert(href.indexOf('https://mozilla.box.com/') !== -1, 'Download link points to the Mozilla Box account');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Styleguide, Branding page: ' + url + 'identity/firefox/branding/', 8, function suite(test) {
    casper.start(url + 'identity/firefox/branding/', function() {
        test.assertHttpStatus(200);

        test.assertVisible('#guidelines-logo', 'The logo guidelines are visible');
        test.assertExists('#guidelines-logo img', 'Main Fx logo exists');

        test.assertElementCount('#guidelines-logo ul li', 3, 'Three download links exist');
        var href = this.getElementAttribute('#guidelines-logo ul li a', 'href');
        test.assert(href.indexOf('https://assets.mozilla.org/') !== -1, 'Link points to Mozilla assets portal');

        test.assertVisible('#usage', 'Usage section is visible');
        test.assertVisible('#mistakes', 'Unacceptable use section is visible');
        test.assertVisible('#partner', 'Partner co-branding section visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Styleguide, Wordmarks page: ' + url + 'identity/firefox/wordmarks/', 16, function suite(test) {
    casper.start(url + 'identity/firefox/wordmarks/', function() {
        test.assertHttpStatus(200);

        test.assertVisible('#intro', 'Intro section visible');

        test.assertVisible('#firefox', 'Release channel section visible');
        test.assertElementCount('#firefox .logo img[alt="Logo"]', 3, 'There are three variations of the wordmark present');
        test.assertVisible('#firefox .download', 'Download links section visible');
        test.assertElementCount('#firefox .download .button-list', 3, 'There are three lists of download links');
        var href = this.getElementAttribute('#firefox .download .button-list:first-of-type li:first-child a', 'href');
        test.assert(href.indexOf('https://assets.mozilla.org/') !== -1, 'Link points to Mozilla assets portal');

        test.assertVisible('#firefox-beta', 'Beta channel section visible');
        test.assertElementCount('#firefox-beta .logo img[alt="Logo"]', 2, 'There are two variations of the wordmark present');
        test.assertVisible('#firefox-beta .download', 'Beta channel wordmark download links visible');

        test.assertVisible('#firefox-nightly', 'Nightly channel section visible');
        test.assertElementCount('#firefox-nightly .logo img[alt="Logo"]', 2, 'There are two variations of the wordmark present');
        test.assertVisible('#firefox-nightly .download', 'Nightly channel wordmark download links visible');

        test.assertVisible('#firefox-developer', 'Nightly channel section visible');
        test.assertElementCount('#firefox-developer .logo img[alt="Logo"]', 2, 'There are two variations of the wordmark present');
        test.assertVisible('#firefox-developer .download', 'Developer channel wordmark download links visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Styleguide, previous and next navigation: ' + url + 'identity/firefox-family/overview/', 5, function suite(test) {
    casper.start(url + 'identity/firefox-family/overview/', function() {
        test.assertHttpStatus(200);

        test.assertVisible('#nextprev', 'Next and previous section visible');
        test.assertElementCount('#nextprev a', 2, 'Both previous and next navigation elements exist');

        var prevHref = this.getElementAttribute('#nextprev .prev', 'href');
        test.assert(prevHref.indexOf('styleguide/identity/mozilla/color/') !== -1, 'Previous link points to the correct URL');

        var nextHref = this.getElementAttribute('#nextprev .next', 'href');
        test.assert(nextHref.indexOf('styleguide/identity/firefox-family/platform/') !== -1, 'Next link points to the correct URL');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
