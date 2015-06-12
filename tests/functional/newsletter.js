/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

/* global casper */
'use strict';

var config = require('../lib/config');
var helpers = require('../lib/helpers');
var path = '/newsletter/';
var url = config.base() + path;

casper.test.begin('Newsletter, Elements: ' + url, 7, function suite(test) {

    casper.start(url, function() {
        test.assertHttpStatus(200);

        test.assertVisible('#newsletter-form', 'Form is visible');
        test.assertElementCount('#newsletter-form input[type="email"]', 1, 'One email field exists');
        test.assertElementCount('#newsletter-form select', 2, 'Two select drop downs exist');
        test.assertElementCount('#newsletter-form input[type="radio"]', 2, 'Two radio buttons exist');
        test.assertElementCount('#newsletter-form input[type="checkbox"]', 1, 'One checkbox exist');
        test.assertElementCount('#newsletter-form input[type="submit"]', 1, 'Submit button exist');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });

});

casper.test.begin('Newsletter, Successful form submission: ' + url, 1, function suite(test) {

    casper.start(url, function() {
        this.fill('#newsletter-form', {
            email: 'noreply@mozilla.com',
            privacy: true
        }, true);
    });

    casper.waitUntilVisible('#newsletter-form-thankyou', function() {
        test.assertVisible('#newsletter-form-thankyou h3', 'Form submitted successfully');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });

});

casper.test.begin('Newsletter, Validation failed, form submission prevented: ' + url, 1, function suite(test) {

    casper.start(url).thenEvaluate(function() {
        document.querySelector('#newsletter-form').setAttribute('novalidate', true);
        document.querySelector('#footer_email_submit').click();
    });

    casper.waitUntilVisible('#footer-email-errors', function() {
        // there should be a .errorlist of two items
        test.assertElementCount('#footer-email-errors ul li', 2, 'Two error messages in list');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });

});

casper.test.begin('Newsletter, Click element labels: ' + url, 2, function suite(test) {

    casper.start(url, function() {

        this.click('#id_fmt_1');
        this.click('#id_privacy');

        var formValues = this.getFormValues('#newsletter-form');

        test.assertEquals(formValues.fmt, 'T', 'Text format is selected');
        test.assertEquals(formValues.privacy, true, 'Privacy checkbox checked');
    });

    casper.run(function() {
        test.done();
        helpers.done();
    });

});
