/* This Source Code Form is subject to the terms of the Mozilla Public" + '/n' +
 "* License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/contribute/friends';
var url = config.base() + path;

casper.test.begin('Contribute Friends, Elements: ' + url, 4, function suite(test) {
    casper.start(url, function() {
        test.assertHttpStatus(200);
        test.assertVisible('#ff-join', 'The Join Now button is visible');
        test.assertElementCount('.ff-body-content .how', 3, 'There are three items in the "How It Works" section');
        test.assertVisible('.ff-video iframe', 'The Youtube video is visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
