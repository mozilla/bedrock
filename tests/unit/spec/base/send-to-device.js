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
                        '<ul class="error-list hidden"></ul>' +
                        '<div class="send-to-device-form-fields">' +
                            '<input type="hidden" value="all">' +
                            '<label class="form-input-label" for="send-to-device-input" data-alt="Enter your email or 10-digit phone number.">Enter your email.</label>' +
                            '<div class="inline-field">' +
                                '<input id="send-to-device-input" class="send-to-device-input" type="text" required>' +
                                '<button type="submit">Send</button>' +
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

        beforeEach(function() {
            jasmine.clock().install();
        });

        afterEach(function() {
            jasmine.clock().uninstall();
        });

        it('should call bedrock geo to update the messaging', function() {
            spyOn(window, 'fetch').and.callFake(function () {
                var d = $.Deferred();
                var data = {
                    country_code: 'us'
                };
                d.resolve(data, 'success');
                return d.promise();
            });

            spyOn(form, 'updateMessaging').and.callThrough();
            form.init();

            // Wait for the fetch().then() to execute
            jasmine.clock().tick(6000);

            expect(window.fetch).toHaveBeenCalledWith('/country-code.json');
            expect(form.updateMessaging).toHaveBeenCalled();
            expect(Mozilla.SendToDevice.COUNTRY_CODE).toEqual('us');
        });
    });

    describe('executeGeoCallback', function() {

        beforeEach(function() {
            jasmine.clock().install();
        });

        afterEach(function() {
            jasmine.clock().uninstall();
        });

        it('should execute the geoCallback function when provided', function() {
            spyOn(window, 'fetch').and.callFake(function () {
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

            // Wait for the fetch().then() to execute
            jasmine.clock().tick(6000);

            expect(form.geoCallback).toHaveBeenCalledWith('fr');
        });

        it('should execute the geoCallback function when geo lookup fails', function() {
            spyOn(window, 'fetch').and.callFake(function () {
                var d = $.Deferred();
                d.reject('error');
                return d.promise();
            });

            form.geoCallback = sinon.stub();
            spyOn(form, 'geoCallback').and.callThrough();
            form.init();

            // Wait for the fetch().then() to execute
            jasmine.clock().tick(6000);

            expect(form.geoCallback).toHaveBeenCalledWith('');
        });
    });

    describe('showSMS', function() {

        beforeEach(function() {
            jasmine.clock().install();
        });

        afterEach(function() {
            jasmine.clock().uninstall();
        });

        it('should call showSMS if users is inside the US', function() {
            spyOn(window, 'fetch').and.callFake(function () {
                var d = $.Deferred();
                var data = {
                    country_code: 'us'
                };
                d.resolve(data);
                return d.promise();
            });

            spyOn(form, 'showSMS').and.callThrough();
            form.init();

            // Wait for the fetch().then() to execute
            jasmine.clock().tick(6000);

            expect(form.showSMS).toHaveBeenCalled();
            expect($('.send-to-device-form').hasClass('sms-country')).toBeTruthy();
        });

        it('should not call showSMS if users is outside a supported country', function() {
            spyOn(window, 'fetch').and.callFake(function () {
                var d = $.Deferred();
                var data = {
                    country_code: 'de'
                };
                d.resolve(data);
                return d.promise();
            });

            spyOn(form, 'showSMS').and.callThrough();
            form.init();

            // Wait for the fetch().then() to execute
            jasmine.clock().tick(6000);

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
            this.firstGetCall = function(){
                var data = {
                    country_code: 'us'
                };
                var pd = window.Promise.resolve(
                    new Response(
                        new Blob([JSON.stringify(data)])
                    )
                );
                return pd;
            };

            // Specifies the delay to use in setTimeout for `expect` calls
            //    The `expect` functions need to be run after a slighty delay
            //    as we need to wait for the Promise chain to finish executing.
            // Note:
            // Small values(100) work, but might fail depending on the order of how
            // specs are run
            // Higher values(1000) means overall test execution will take slightly longer
            // 500 is a middle ground
            this.timeDelayExpect = 500;
        });


        it('should handle success', function(done) {
            var second = function() {
                var data = {
                    'success': 'success'
                };
                var pd = window.Promise.resolve(
                    new Response(
                        new Blob([JSON.stringify(data)])
                    )
                );
                return pd;
            };

            var fetchSpy = spyOn(window, 'fetch');
            fetchSpy.and.callFake(this.firstGetCall);

            spyOn(form, 'onFormSuccess').and.callThrough();

            form.init();

            fetchSpy.and.callFake(second);

            // requestSubmit() validates the form,
            // so we need to insert some data in the <input> tag
            document.getElementById('send-to-device-input').value = 'abc@def.com';
            document.querySelector('.send-to-device-form').requestSubmit();


            setTimeout(function(){
                // once for get, once for post
                expect(window.fetch).toHaveBeenCalledTimes(2);
                expect(form.onFormSuccess).toHaveBeenCalledWith('success');
                done();
            }, this.timeDelayExpect);
        });
        
        it('should handle error', function(done) {

            var fetchSpy = spyOn(window, 'fetch');
            fetchSpy.and.callFake(this.firstGetCall);


            spyOn(form, 'onFormError').and.callThrough();

            form.init();
            var second = function() {
                var data = {
                    'errors': 'Please enter an email address.'
                };
                var pd = window.Promise.resolve(
                    new Response(
                        new Blob([JSON.stringify(data)])
                    )
                );
                return pd;
            };
            fetchSpy.and.callFake(second);

            // requestSubmit() validates the form,
            // so we need to insert some data in the <input> tag
            document.getElementById('send-to-device-input').value = 'abc@def.com';
            document.querySelector('.send-to-device-form').requestSubmit();


            setTimeout(function(){
                // once for get, once for post
                expect(window.fetch).toHaveBeenCalledTimes(2);
                expect(form.onFormError).toHaveBeenCalledWith('Please enter an email address.');
                done();
            }, this.timeDelayExpect);
        });

        it('should handle failure', function(done) {

            var fetchSpy = spyOn(window, 'fetch');
            fetchSpy.and.callFake(this.firstGetCall);

            spyOn(form, 'onFormFailure').and.callThrough();

            form.init();
            var second = function() {
                var error = 'An error occurred in our system. Please try again later.';
                var pd = window.Promise.reject(
                    error
                );
                return pd;
            };
            fetchSpy.and.callFake(second);

            // requestSubmit() validates the form,
            // so we need to insert some data in the <input> tag
            document.getElementById('send-to-device-input').value = 'abc@def.com';
            document.querySelector('.send-to-device-form').requestSubmit();

            setTimeout(function() {
                // only 1 get request
                expect(window.fetch).toHaveBeenCalled();
                expect(form.onFormFailure).toHaveBeenCalledWith('An error occurred in our system. Please try again later.');
                done();
            }, this.timeDelayExpect);
        });
        
    });

});
