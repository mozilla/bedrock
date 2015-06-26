/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/contribute/';
var url = config.base() + path;

casper.test.begin('Contribute, Elements: ' + url, 11, function suite(test) {

    casper.start(url, function() {

        test.assertHttpStatus(200);

        test.assertVisible('.contribute-nav', 'The top navigation is visible');

        test.assertVisible('#slideshow', 'Slide show is visible');
        test.assertElementCount('.cycle-pager > span', 3, 'Three links available for manual pager cycle');
        test.assertVisible('#slideshow .cta', 'Get involved CTA is visible');

        test.assertElementCount('#landing-stories .stories li', 3, 'Three Mozillian stories in list');
        test.assertVisible('#landing-howto .cta', 'Get started CTA visible');

        test.assertElementCount('#landing-notready .other-actions li', 4, 'Donate, download and social buttons exist');
        test.assertVisible('#newsletter-form', 'The newsletter form is visible.');

        test.assertVisible('.extra-event .event-link', 'There is one featured event');
        test.assertVisible('.extra-event .events-all', 'All events link visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
})

casper.test.begin('Contribute, Video modal: ' + url, 4, function suite(test) {

    casper.start(url, function() {
        test.assertVisible('#landing-mission .video-play');
        this.click('.video-play');
    });

    casper.waitUntilVisible('#video-iamamozillian', function() {
        test.assert(true, 'Video modal is shown')
        test.assertExists('#video-iamamozillian video', 'Video is displayed in modal');
        this.click('#modal-close');
    });

    casper.waitWhileVisible('#video-iamamozillian', function() {
        test.assert(true, 'Video modal closed successfully');
    })

    casper.run(function() {
        test.done();
        helpers.done();
    });
})
