/* This Source Code Form is subject to the terms of the Mozilla Public" + '/n' +
 "* License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/contribute/stories/shreyas/';
var url = config.base() + path;

casper.test.begin('Contribute Stories, Elements: ' + url, 11, function suite(test) {
    casper.start(url, function() {
        test.assertHttpStatus(200);

        test.assertVisible('#contribute-nav-menu .nav-cta', 'Get involved button is visible');
        test.assertVisible('.head-stats', 'Community stats visible');

        test.assertVisible('.story-intro .photo', 'The Mozillian profile image is visible');
        test.assertVisible('.story-areas', 'Areas of activity content visible');
        test.assertVisible('.story-links', 'List of links to social and other external links visible');

        test.assertElementCount('.stories-other .person', 3, 'List of three Mozillians visible');
        test.assertElementCount('.person a.url', 3, 'Each Mozillians read more link is visible');

        test.assertVisible('.extra-event .event-link', 'There is one featured event');
        test.assertVisible('.extra-event .events-all', 'All events link visible');
        test.assertVisible('#newsletter-form', 'The newsletter form is visible.');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Contribute Stories, More toggle interaction: ' + url, 4, function suite(test) {
    casper.start(url, function() {
        test.assertNotVisible('.story-more', 'Additional story details hidden');
        test.assertVisible('.more-toggle', 'The more toggle is visible');

        this.click('.more-toggle button');
    });

    casper.waitUntilVisible('.story-more', function() {
        test.assert(true, 'Additional story content shown');
        this.click('.more-toggle button');
    });

    casper.waitWhileVisible('.story-more', function() {
        test.assert(true, 'Additional story content hidden');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
