/* Base JS unit test spec for bedrock send-to-device.js
 * For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('send-to-device.js', function() {

    var form;
    var spinnerStub;

    beforeEach(function () {

        var formMarkup = [
            '<section id="send-to-device">' +
                '<div class="form-container">' +
                    '<form id="send-to-device-form">' +
                        '<ul class="error-list hidden"></ul>' +
                        '<div class="input">' +
                            '<input type="hidden" id="id-platform" value="all">' +
                            '<label id="form-input-label" for="id-input" data-alt="Enter your email or 10-digit phone number.">Enter your email.</label>' +
                            '<div class="inline-field">' +
                                '<input id="id-input" type="text" required>' +
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

        window.Spinner = sinon.stub();
        window.Spinner.prototype.spin = sinon.stub();

        spyOn($, 'getScript').andCallFake(function (req) {
            var d = $.Deferred();
            d.resolve('foo', 'success');
            return d.promise();
        });

        form = new Mozilla.SendToDevice();
    });

    afterEach(function () {
        form.unbindEvents();
        $('#send-to-device').remove();
    });

    describe('instantiation', function() {

        it('should create a new instance of SendToDevice', function() {
            spyOn(form, 'checkLocation').andCallThrough();
            spyOn(form, 'bindEvents').andCallThrough();
            form.init();
            expect(form instanceof Mozilla.SendToDevice).toBeTruthy();
            expect(form.checkLocation).toHaveBeenCalled();
            expect(form.bindEvents).toHaveBeenCalled();
        });
    });

    describe('checkLocation', function() {

        it('should load GeoDude to update the messaging', function() {
            spyOn(form, 'updateMessaging').andCallThrough();
            form.init();
            expect($.getScript).toHaveBeenCalledWith('https://geo.mozilla.org/country.js');
            expect(form.updateMessaging).toHaveBeenCalled();
        });
    });

    describe('updateMessaging', function() {

        it('should call showSMS if users is inside the US', function() {
            window.geoip_country_code = sinon.stub().returns('us');
            spyOn(form, 'showSMS').andCallThrough();
            form.init();
            expect(form.showSMS).toHaveBeenCalled();
        });

        it('should not call showSMS if users is outside the US', function() {
            window.geoip_country_code = sinon.stub().returns('gb');
            spyOn(form, 'showSMS').andCallThrough();
            form.init();
            expect(form.showSMS).not.toHaveBeenCalled();
        });
    });

    describe('showSMS', function() {

        it('should show SMS messaging', function() {
            window.geoip_country_code = sinon.stub().returns('us');
            spyOn(form, 'showSMS').andCallThrough();
            form.init();
            expect($('#send-to-device-form').hasClass('us')).toBeTruthy();
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

            spyOn($, 'post').andCallFake(function (req) {
                var d = $.Deferred();
                var data = {
                    'success': 'success'
                };
                d.resolve(data);
                return d.promise();
            });

            spyOn(form, 'onFormSuccess').andCallThrough();

            form.init();
            $('#send-to-device-form').submit();
            expect($.post).toHaveBeenCalled();
            expect(form.onFormSuccess).toHaveBeenCalledWith('success');
        });

        it('should handle error', function() {

            spyOn($, 'post').andCallFake(function (req) {
                var d = $.Deferred();
                var data = {
                    'errors': 'Please enter an email address.'
                };
                d.resolve(data);
                return d.promise();
            });

            spyOn(form, 'onFormError').andCallThrough();

            form.init();
            $('#send-to-device-form').submit();
            expect($.post).toHaveBeenCalled();
            expect(form.onFormError).toHaveBeenCalledWith('Please enter an email address.');
        });

        it('should handle failure', function() {

            spyOn($, 'post').andCallFake(function (req) {
                var d = $.Deferred();
                var error = 'An error occurred in our system. Please try again later.';
                d.reject(error);
                return d.promise();
            });

            spyOn(form, 'onFormFailure').andCallThrough();

            form.init();
            $('#send-to-device-form').submit();
            expect($.post).toHaveBeenCalled();
            expect(form.onFormFailure).toHaveBeenCalledWith('An error occurred in our system. Please try again later.');
        });
    });

});
