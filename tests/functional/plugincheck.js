/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/plugincheck/';
var url = config.base() + path;

casper.test.begin('PluginCheck, Elements: ' + url, 5, function suite(test) {

    casper.start();

    casper.userAgent(config.userAgent.fx);

    casper.thenOpen(url, function() {
        test.assertHttpStatus(200);
        test.assertResourceExists(/media\/img\/plugincheck\/screenshots\/addons-screenshot/);
        // The tests below ensure that the newsletter section is always visible irrespective of browser
        test.assertVisible('#newsletter-form', 'The newletter signup is visible in Fx');

        casper.userAgent(config.userAgent.chrome);
    });

    casper.thenOpen(url, function() {
        test.assertVisible('#newsletter-form', 'The newletter signup is visible in webkit');
        test.assertVisible('.download-button', 'Download button visible in webkit');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('PluginCheck, conditional content Firefox: ' + url, 2, function suite(test) {

    casper.start();

    casper.userAgent(config.userAgent.fx);

    casper.thenOpen(url, function() {
        test.assertVisible('.plugin-status-container h2', 'Plugin Status heading exists');
        test.assertNotVisible('.not-supported', 'Unsupported browser message not visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('PluginCheck, conditional content Webkit: ' + url, 2, function suite(test) {

    casper.start(url, function() {
        test.assertVisible('.not-supported', 'Unsupported browser message visible');
        test.assertNotVisible('.plugin-status-container h2', 'Plugin Status heading not visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('PluginCheck, outated Firefox: ' + url, 1, function suite(test) {

    casper.start();

    casper.userAgent(config.userAgent.fxOutdated);

    casper.thenOpen(url, function() {
        test.assertVisible('.version-message-container', 'Update Firefox button visible');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

// This test assumes that no plugins will be loaded as the Casper loadPlugins option,
// casper.options.pageSettings.loadPlugins, has not been set to true.
// http://docs.casperjs.org/en/latest/modules/casper.html#pagesettings
casper.test.begin('PluginCheck, no plugins found message: ' + url, 2, function suite(test) {
    casper.start();

    casper.userAgent(config.userAgent.fx);

    casper.thenOpen(url, function() {
        test.assertVisible('#no-plugins', 'The no plugins container is visible');
        test.assertNotVisible('#plugins', 'The plugins container is hidden');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
