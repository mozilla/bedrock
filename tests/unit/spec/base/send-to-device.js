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
                            '<label id="mzp-c-field-label" for="send-to-device-input" data-alt="Enter your email or 10-digit phone number.">Enter your email.</label>' +
                            '<div class="mzp-c-field mzp-l-stretch">' +
                                '<input id="send-to-device-input" class="mzp-c-field-control send-to-device-input" type="text" required>' +
                                '<button type="submit" class="button mzp-c-button mzp-t-product">Send</button>' +
                            '</div>' +
                        '</div>' +
                        '<div class="thank-you hidden"></div>' +
                        '<div class="loading-spinner"></div>' +
                        '</form>' +
                    '</div>' +
            '</section>'
        ].join();

        $(formMarkup).appendTo('body');

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
        $('#send-to-device').remove();
        Mozilla.SendToDevice.COUNTRY_CODE = '';
    });

    describe('instantiation', function() {

        it('should create a new instance of SendToDevice', function() {
            spyOn(form, 'getLocation');
            spyOn(form, 'bindEvents');
            form.init();
            expect(form instanceof Mozilla.SendToDevice).toBeTruthy();
            expect(form.getLocation).toHaveBeenCalled();
            expect(form.bindEvents).toHaveBeenCalled();
        });
    });

    describe('inSupportedCountry', function() {
        it('should be true for countries in data-countries, and false for others', function() {
            Mozilla.SendToDevice.COUNTRY_CODE = 'de';
            expect(form.inSupportedCountry()).toBeFalsy();
            Mozilla.SendToDevice.COUNTRY_CODE = 'cn';
            expect(form.inSupportedCountry()).toBeFalsy();
            Mozilla.SendToDevice.COUNTRY_CODE = 'gb';
            expect(form.inSupportedCountry()).toBeTruthy();
            Mozilla.SendToDevice.COUNTRY_CODE = 'us';
            expect(form.inSupportedCountry()).toBeTruthy();
        });
    });

    describe('getLocation', function() {

        it('should call bedrock geo to update the messaging', function() {
            spyOn($, 'get').and.callFake(function () {
                var d = $.Deferred();
                var data = {
                    country_code: 'us'
                };
                d.resolve(data, 'success');
                return d.promise();
            });
            spyOn(form, 'updateMessaging').and.callThrough();
            form.init();
            expect($.get).toHaveBeenCalledWith('/country-code.json');
            expect(form.updateMessaging).toHaveBeenCalled();
            expect(Mozilla.SendToDevice.COUNTRY_CODE).toEqual('us');
        });
    });

    describe('executeGeoCallback', function() {

        it('should execute the geoCallback function when provided', function() {
            spyOn($, 'get').and.callFake(function () {
                var d = $.Deferred();
                var data = {
                    country_code: 'fr'
                };
                d.resolve(data, 'success');
                return d.promise();
            });

            form.geoCallback = sinon.stub();
            spyOn(form, 'geoCallback').and.callThrough();
            form.init();
            expect(form.geoCallback).toHaveBeenCalledWith('fr');
        });

        it('should execute the geoCallback function when geo lookup fails', function() {
            spyOn($, 'get').and.callFake(function () {
                var d = $.Deferred();
                d.reject('error');
                return d.promise();
            });

            form.geoCallback = sinon.stub();
            spyOn(form, 'geoCallback').and.callThrough();
            form.init();
            expect(form.geoCallback).toHaveBeenCalledWith('');
        });
    });

    describe('showSMS', function() {

        it('should call showSMS if users is inside the US', function() {
            spyOn($, 'get').and.callFake(function () {
                var d = $.Deferred();
                var data = {
                    country_code: 'us'
                };
                d.resolve(data);
                return d.promise();
            });

            spyOn(form, 'showSMS').and.callThrough();
            form.init();
            expect(form.showSMS).toHaveBeenCalled();
            expect($('.send-to-device-form').hasClass('sms-country')).toBeTruthy();
        });

        it('should not call showSMS if users is outside a supported country', function() {
            spyOn($, 'get').and.callFake(function () {
                var d = $.Deferred();
                var data = {
                    country_code: 'de'
                };
                d.resolve(data);
                return d.promise();
            });

            spyOn(form, 'showSMS').and.callThrough();
            form.init();
            expect(form.showSMS).not.toHaveBeenCalled();
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

        beforeEach(function() {
            spyOn($, 'get').and.callFake(function () {
                var d = $.Deferred();
                var data = {
                    country_code: 'us'
                };
                d.resolve(data);
                return d.promise();
            });
        });

        it('should handle success', function() {

            spyOn($, 'post').and.callFake(function () {
                var d = $.Deferred();
                var data = {
                    'success': 'success'
                };
                d.resolve(data);
                return d.promise();
            });

            spyOn(form, 'onFormSuccess').and.callThrough();

            form.init();
            $('.send-to-device-form').submit();
            expect($.post).toHaveBeenCalled();
            expect(form.onFormSuccess).toHaveBeenCalledWith('success');
        });

        it('should handle error', function() {

            spyOn($, 'post').and.callFake(function () {
                var d = $.Deferred();
                var data = {
                    'errors': 'Please enter an email address.'
                };
                d.resolve(data);
                return d.promise();
            });

            spyOn(form, 'onFormError').and.callThrough();

            form.init();
            $('.send-to-device-form').submit();
            expect($.post).toHaveBeenCalled();
            expect(form.onFormError).toHaveBeenCalledWith('Please enter an email address.');
        });

        it('should handle failure', function() {

            spyOn($, 'post').and.callFake(function () {
                var d = $.Deferred();
                var error = 'An error occurred in our system. Please try again later.';
                d.reject(error);
                return d.promise();
            });

            spyOn(form, 'onFormFailure').and.callThrough();

            form.init();
            $('.send-to-device-form').submit();
            expect($.post).toHaveBeenCalled();
            expect(form.onFormFailure).toHaveBeenCalledWith('An error occurred in our system. Please try again later.');
        });
    });

});
