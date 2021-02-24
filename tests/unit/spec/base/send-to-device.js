/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global sinon, */
/* eslint camelcase: [2, {properties: "never"}] */
/* eslint new-cap: [2, {"capIsNewExceptions": ["Deferred"]}] */

describe('send-to-device.js', function() {

    'use strict';

    var form;

    beforeEach(function () {

        var formMarkup = [
            '<section id="send-to-device" class="send-to-device" data-countries="|us|gb|">' +
                '<div class="form-container">' +
                    '<form class="send-to-device-form">' +
                        '<ul class="mzp-c-form-errors hidden"></ul>' +
                        '<div class="send-to-device-form-fields">' +
                            '<input type="hidden" value="all">' +
                            '<label id="mzp-c-field-label" for="send-to-device-input">Enter your email.</label>' +
                            '<div class="mzp-c-field mzp-l-stretch">' +
                                '<input id="send-to-device-input" class="mzp-c-field-control send-to-device-input" name="s2d-email" type="text" required>' +
                                '<button type="submit" class="button mzp-c-button mzp-t-product">Send</button>' +
                            '</div>' +
                        '</div>' +
                        '<div class="thank-you hidden"></div>' +
                        '<div class="loading-spinner"></div>' +
                        '</form>' +
                    '</div>' +
            '</section>'
        ].join();

        document.body.insertAdjacentHTML('beforeend', formMarkup);

        // stub out spinner.js
        window.Spinner = sinon.stub();
        window.Spinner.prototype.spin = sinon.stub();

        // stub out google tag manager
        window.dataLayer = sinon.stub();
        window.dataLayer.push = sinon.stub();

        form = new Mozilla.SendToDevice();
    });

    afterEach(function () {
        form.unbindEvents();
        var content = document.getElementById('send-to-device');
        content.parentNode.removeChild(content);
        Mozilla.SendToDevice.COUNTRY_CODE = '';
    });

    describe('instantiation', function() {

        it('should create a new instance of SendToDevice', function() {
            spyOn(form, 'bindEvents');
            form.init();
            expect(form instanceof Mozilla.SendToDevice).toBeTruthy();
            expect(form.bindEvents).toHaveBeenCalled();
        });
    });

    describe('checkEmailValidity', function() {

        it('should return true for primitive email format', function() {
            expect(form.checkEmailValidity('a@a')).toBeTruthy();
            expect(form.checkEmailValidity('example@example.com')).toBeTruthy();
        });

        it('should return false for anything else', function() {
            expect(form.checkEmailValidity(1234567890)).toBeFalsy();
            expect(form.checkEmailValidity('aaa')).toBeFalsy();
            expect(form.checkEmailValidity(null)).toBeFalsy();
            expect(form.checkEmailValidity(undefined)).toBeFalsy();
            expect(form.checkEmailValidity(true)).toBeFalsy();
            expect(form.checkEmailValidity(false)).toBeFalsy();
        });
    });

    describe('onFormSubmit', function() {

        it('should handle success', function() {

            spyOn(window.$, 'post').and.callFake(function () {
                var d = window.$.Deferred();
                var data = {
                    'success': 'success'
                };
                d.resolve(data);
                return d.promise();
            });

            spyOn(form, 'onFormSuccess').and.callThrough();

            form.init();
            document.getElementById('send-to-device-input').value = 'success@example.com';
            document.querySelector('.send-to-device-form button[type="submit"]').click();
            expect(window.$.post).toHaveBeenCalled();
            expect(form.onFormSuccess).toHaveBeenCalledWith('success');
        });

        it('should handle error', function() {

            spyOn($, 'post').and.callFake(function () {
                var d = window.$.Deferred();
                var data = {
                    'errors': 'Please enter an email address.'
                };
                d.resolve(data);
                return d.promise();
            });

            spyOn(form, 'onFormError').and.callThrough();

            form.init();
            document.getElementById('send-to-device-input').value = 'invalid@email';
            document.querySelector('.send-to-device-form button[type="submit"]').click();
            expect(window.$.post).toHaveBeenCalled();
            expect(form.onFormError).toHaveBeenCalledWith('Please enter an email address.');
        });

        it('should handle failure', function() {

            spyOn($, 'post').and.callFake(function () {
                var d = window.$.Deferred();
                var error = 'An error occurred in our system. Please try again later.';
                d.reject(error);
                return d.promise();
            });

            spyOn(form, 'onFormFailure').and.callThrough();

            form.init();
            document.getElementById('send-to-device-input').value = 'failure@example.com';
            document.querySelector('.send-to-device-form button[type="submit"]').click();
            expect($.post).toHaveBeenCalled();
            expect(form.onFormFailure).toHaveBeenCalledWith('An error occurred in our system. Please try again later.');
        });
    });

});
