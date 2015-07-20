/* This Source Code Form is subject to the terms of the Mozilla Public" + '/n' +
 "* License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/contribute/signup/';
var url = config.base() + path;

casper.test.begin('Contribute Signup, Elements: ' + url, 15, function suite(test) {
    casper.start(url, function() {
        test.assertHttpStatus(200);

        test.assertVisible('#inquiry-form', 'The inquiry form is visible');
        test.assertVisible('.option-list', 'The categories option list is visible');
        test.assertElementCount('.option-list li', 8, 'There are eight category items');

        test.assertNotVisible('.areas', 'The areas form fields are initially hidden');

        test.assertElementCount('.personal input[type="text"]', 1, 'Name input field exists');
        test.assertElementCount('.personal input[type="email"]', 1, 'Email input field exists');
        test.assertElementCount('.personal select', 1, 'Country select field exist');
        test.assertElementCount('.personal textarea', 1, 'Message field exist');
        test.assertElementCount('.form-format input[type="radio"]', 2, 'Email format radio buttons exist');
        test.assertElementCount('.form-agree input[type="checkbox"]', 1, 'Accept privacy policy checkbox exists');
        test.assertElementCount('.submit button', 1, 'Start Contributing buttons exists');
        test.assertElementCount('.form-newsletter input[type="checkbox"]', 1, 'Newsletter subscribe checkbox exists');

        test.assertVisible('.next-steps', 'The next steps section is visible');
        test.assertElementCount('.steps li', 3, 'There are three steps listed');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Contribute Signup, Areas of interest interaction: ' + url, 8, function suite(test) {
    casper.start(url, function() {
        casper.click('.option-list li:first-child label');
    });

    casper.waitUntilVisible('.areas', function() {
        test.assert(true, 'The areas of interest section is visible');
    });

    casper.waitUntilVisible('#area-coding', function() {
        test.assert(true, 'The appropriate area of interest select field is visible');
        test.assertElementCount('#area-coding select', 1, 'The select field exists');

        casper.click('.option-list li:nth-child(3) label');
    })

    casper.waitUntilVisible('#area-writing', function() {
        test.assert(true, 'The writing area of interest section is visible');
        test.assertElementCount('#area-writing select', 1, 'The select field exists');
        test.assertNotVisible('#area-coding', 'The coding area of interest section has been hidden');

        casper.click('.option-list li:nth-child(5) label');
    });

    casper.waitWhileVisible('#area-writing', function() {
        test.assert(true, 'The writing area of interest is hidden');
        test.assertNotVisible('.areas', 'Areas of interest select fields hidden');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Contribute Signup, Tooltip: ' + url, 2, function suite(test) {
    casper.start(url, function() {
        this.mouse.move('a.info');
    });

    casper.waitUntilVisible('.tooltip', function() {
        test.assert(true, 'The tooltip is shown');
        // move the mouse off the info icon
        this.mouse.move(0, 0);
    });

    casper.waitWhileVisible('.tooltip', function() {
        test.assert(true, 'The tooltip has been removed');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Contribute Signup, Server side validation prevents form submission: ' + url, 2, function suite(test) {
    casper.start(url).thenEvaluate(function() {
        document.getElementById('inquiry-form').setAttribute('novalidate', true);
        document.querySelector('#inquiry-form button').click();
    });

    casper.waitUntilVisible('.errorlist', function() {
        test.assert(true, 'Server side validation failed and returned error list');
        test.assertElementCount('.errorlist', 5, 'There are five lists containing errors');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Contribute Signup, Successfull form submission: ' + url, 1, function suite(test) {
    casper.start(url, function() {
        this.fill('#inquiry-form', {
            category: 'coding',
            area_coding: 'coding-websites',
            name: 'Casper the friendly Ghost',
            email: 'noreply@mozilla.com',
            country: 'af',
            format: 'T',
            privacy: true
        }, true);
    });

    casper.waitForUrl(/contribute\/thankyou\//g, function() {
        test.assert(true, 'Form was submitted successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});

casper.test.begin('Contribute Signup, Click element labels: ' + url, 2, function suite(test) {
    casper.start(url, function() {

        this.click('#id_privacy');
        this.click('#id_newsletter');

        var formValues = this.getFormValues('#inquiry-form');

        test.assertEquals(formValues.privacy, true, 'Privacy checkbox checked');
        test.assertEquals(formValues.newsletter, true, 'Newsletter checkbox checked');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });
});
