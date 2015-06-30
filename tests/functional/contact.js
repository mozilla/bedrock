/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper, __clientHelper__ */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/contact/';
var url = config.base() + path;
var spacesUrl = url + 'spaces/';
var communitiesUrl = url + 'communities/';

casper.test.begin('Contact, Spaces elements: ' + spacesUrl, 10, function suite(test) {

    casper.start(spacesUrl, function() {
        test.assertHttpStatus(200);
        test.assertVisible('#map', 'Map is visible');
        test.assertElementCount('.category-tabs li a', 2, 'Tab navigation exists');
        test.assertElementCount('.leaflet-marker-pane img', 12, '12 markers exist');
        test.assertVisible('#nav-spaces', 'Spaces navigation is visible');
        test.assertNotVisible('#nav-communities', 'Communities navigation is not visible');
        test.assertNotVisible('#nav-spaces-select', 'Mobile navigation is not visible');
        test.assertVisible('#mozorg-newsletter-form', 'Newsletter is visible');
        test.assertVisible('.contacting', 'Contacting Mozilla section is visible');
        test.assertExists('.category-tabs > li[data-id="spaces"].current', 'Spaces tab is selected');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Contact, Communities elements: ' + communitiesUrl, 10, function suite(test) {

    casper.start(communitiesUrl, function() {
        test.assertHttpStatus(200);
        test.assertVisible('#map', 'Map is visible');
        test.assertElementCount('.category-tabs li a', 2, 'Tab navigation exists');
        test.assertVisible('#map .legend', 'Communities legend is visible');
        test.assertNotVisible('#nav-spaces', 'Spaces navigation is not visible');
        test.assertVisible('#nav-communities', 'Communities navigation is visible');
        test.assertNotVisible('#nav-spaces-select', 'Mobile navigation is not visible');
        test.assertVisible('#mozorg-newsletter-form', 'Newsletter is visible');
        test.assertVisible('.contacting', 'Contacting Mozilla section is visible');
        test.assertExists('.category-tabs > li[data-id="communities"].current', 'Communities tab is selected');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Contact, Spaces navigation click: ' + spacesUrl, 2, function suite(test) {

    casper.options.waitTimeout = 10000;

    casper.start(spacesUrl, function() {
        this.click('#nav-spaces li[data-id="mountain-view"] > a');
    });

    casper.waitForUrl(/mountain-view/, function() {
        test.assertUrlMatch(/mountain-view/, 'URL changed sucessfully');
    });

    casper.waitForSelector('#entry-container #mountain-view', function() {
        test.assert(true, 'Page content updated successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Contact, Tab navigation click: ' + spacesUrl, 3, function suite(test) {

    casper.options.waitTimeout = 10000;

    casper.start(spacesUrl, function() {
        this.click('.category-tabs li[data-id="communities"] > a');
    });

    casper.waitForUrl(/communities/, function() {
        test.assertUrlMatch(/communities/, 'URL changed sucessfully');
        test.assertVisible('#map .legend', 'Communities legend is visible');
    });

    casper.waitForSelector('#entry-container #communities', function() {
        test.assert(true, 'Page content updated successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Contact, Mobile interaction: ' + spacesUrl, 6, function suite(test) {

    casper.options.viewportSize = config.viewport.mobile;
    casper.options.waitTimeout = 10000;

    casper.start(url, function() {
        test.assertNotVisible('#map', 'Map is not visible on mobile');
        test.assertVisible('#nav-spaces-select', 'Mobile navigation is visible');
        test.assertNotVisible('#nav-spaces', 'Spaces navigation is not visible');
        test.assertNotVisible('#nav-communities', 'Communities navigation is not visible');
    });

    casper.thenEvaluate(function(space) {
        var select = document.getElementById('nav-spaces-select');
        select.value = space;
        __clientHelper__.triggerEvent('change', select);
    }, 'mountain-view');

    casper.waitForUrl(/mountain-view/, function() {
        test.assertUrlMatch(/mountain-view/, 'URL updated on mobile nav change');
    });

    casper.waitForSelector('#entry-container #mountain-view', function() {
        test.assert(true, 'Page content updated successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
