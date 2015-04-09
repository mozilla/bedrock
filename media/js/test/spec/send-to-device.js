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
                        '<ul class="error-list hidden">' +
                            '<li>An error occurred in our system. Please try again later.</li>' +
                        '</ul>' +
                        '<div class="input">' +
                            '<input type="hidden" id="id-platform" value="all">' +
                            '<label id="form-input-label" for="id-input" data-alt="Enter your email or 10-digit phone number.">Enter your email.</label>' +
                            '<div class="inline-field">' +
                                '<input id="id-input" type="text" data-alt="Enter your email or 10-digit phone number." placeholder="Enter your email." required>' +
                                '<button type="submit" class="button-flat">Send</button>' +
                            '</div>' +
                        '</div>' +
                        '<div class="thank-you hidden">' +
                            '<p>Check your device for the email or text message!</p>' +
                            '<a href="#" role="button" class="more send-another">Send to another device</a>' +
                        '</div>' +
                        '<div class="loading-spinner"></div>' +
                        '</form>' +
                    '</div>' +
                '<footer>' +
                    '<ul>' +
                        '<li class="app-store">' +
                            '<a class="more" href="#">Go to the App Store</a>' +
                        '</li>' +
                        '<li class="google-play">' +
                            '<a class="more" href="#">Go to Google Play</a>' +
                        '</li>' +
                    '</ul>' +
                '</footer>' +
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
                    'error': 'Please enter an email address.'
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
