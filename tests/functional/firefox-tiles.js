/* This Source Code Form is subject to the terms of the Mozilla Public" + '/n' +
 "* License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/firefox/tiles/';
var url = config.base() + path;

casper.test.begin('Firefox Tiles, Elements: ' + url, 5, function suite(test) {
    casper.start(url, function() {
        test.assertHttpStatus(200);

        test.assertElementCount('.sidebar-inset img', 2, 'There are two images in the sidebar inset');
        test.assertElementCount('.tls-personalize ol img', 3, 'There are three images as part of the personalize content block');
        test.assertElementCount('#main-content section', 4, 'The main content is made up of four sections');

        var href = this.getElementAttribute('.tls-personalize p:last-child a', 'href');
        test.assert(href.indexOf('support.mozilla.org/kb/new-tab-page-show-hide-and-customize') > -1, 'Link to SUMO New Tab article');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
