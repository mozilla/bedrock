/* This Source Code Form is subject to the terms of the Mozilla Public" + '/n' +
 "* License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/contribute/events/';
var url = config.base() + path;

casper.test.begin('Contribute Events, Elements: ' + url, 8, function suite(test) {
    casper.start(url, function() {
        test.assertHttpStatus(200);

        test.assertVisible('#contribute-nav-menu .nav-cta', 'Get involved button is visible');

        test.assertVisible('.head-stats', 'Community stats visible');
        test.assertVisible('.events-table', 'The events table is visible');
        test.assertVisible('.events-table td.event-date', 'At least one event in the events table');

        test.assertVisible('.extra-event .event-link', 'There is one featured event');
        test.assertVisible('.extra-event .events-all', 'All events link visible');
        test.assertVisible('#newsletter-form', 'The newsletter form is visible.');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
