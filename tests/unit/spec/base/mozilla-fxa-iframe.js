/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect */

describe('mozilla-fxa-iframe.js', function() {

    'use strict';

    var fxaHost = 'http://localhost:9876';
    var partnerAFxaHost = 'http://127.0.0.1:9876';

    beforeEach(function () {
        var fxaMarkup = [
            '<section id="fxa-iframe-config" data-host="' + fxaHost + '" data-partnera-host="' + partnerAFxaHost + '">' +
                '<iframe id="fxa" data-src="' + fxaHost + '?utm_campaign=fxa-embedded-form&amp;utm_medium=referral&amp;utm_source=firstrun&amp;utm_content=fx-{{ version }}&amp;entrypoint=firstrun&amp;service=sync&amp;context=iframe&amp;style=chromeless&amp;haltAfterSignIn=true"></iframe>' +
            '</section>'
        ].join();

        $(fxaMarkup).appendTo($('body'));
    });

    afterEach(function () {
        $('#fxa-iframe-config').remove();
    });

    describe('Mozilla.FxaIframe.init', function () {
        it('should initialize the FxA iframe', function () {
            Mozilla.FxaIframe.init();

            // make sure iframe src is as expected
            expect($('#fxa').attr('src')).toContain(fxaHost);
        });

        it('should update iframe src for Fx 46+', function () {
            var fxVersion = Mozilla.Client.FirefoxMajorVersion;
            Mozilla.Client.FirefoxMajorVersion = 47;

            Mozilla.FxaIframe.init();

            expect($('#fxa').attr('src')).toContain('context=fx_firstrun_v2');

            Mozilla.Client.FirefoxMajorVersion = fxVersion;
        });

        it('should not update iframe src for Fx < 46', function () {
            var fxVersion = Mozilla.Client.FirefoxMajorVersion;
            Mozilla.Client.FirefoxMajorVersion = 45;

            Mozilla.FxaIframe.init();

            expect($('#fxa').attr('src')).not.toContain('context=fx_firstrun_v2');

            Mozilla.Client.FirefoxMajorVersion = fxVersion;
        });

        it('should append URL encoded email if sent in config', function () {
            var email = 'thedude@abides.net';

            Mozilla.FxaIframe.init({
                userEmail: email
            });

            expect($('#fxa').attr('src')).toContain('&email=' + encodeURIComponent(email));
        });

        it('should not accept an invalid email address', function () {
            var invalidEmail = 'thedude@abies';

            Mozilla.FxaIframe.init({
                userEmail: invalidEmail
            });

            expect($('#fxa').attr('src')).not.toContain('&email=');
        });

        it('should use specified fxa host for certain distributions', function () {
            var distribution = 'PartnerA';

            Mozilla.FxaIframe.init({
                distribution: distribution
            });

            expect($('#fxa').attr('src')).toContain(partnerAFxaHost);
        });

        it('should use default fxa host for other distributions', function () {
            var distribution = 'PartnerB';

            Mozilla.FxaIframe.init({
                distribution: distribution
            });

            expect($('#fxa').attr('src')).toContain(fxaHost);
        });
    });

    describe('Mozilla.FxaIframe postMessage handling', function() {
        var config;

        it('should execute callback for loaded postMessage', function(done) {
            var messageData = {
                command: 'loaded'
            };

            config = {
                onLoaded: function(data) {
                    var command = data.command;
                    expect(config.onLoaded).toHaveBeenCalled();
                    expect(command).toEqual('loaded');
                    done();
                }
            };

            spyOn(config, 'onLoaded').and.callThrough();

            Mozilla.FxaIframe.init(config);

            window.postMessage(JSON.stringify(messageData), '*');
        });

        it('should execute callback and resize iframe for resize postMessage', function(done) {
            var messageData = {
                command: 'resize',
                data: {
                    height: 555
                }
            };

            config = {
                onResize: function(data) {
                    var command = data.command;
                    expect(config.onResize).toHaveBeenCalled();
                    expect(command).toEqual('resize');
                    expect($('#fxa').css('height')).toEqual('555px');
                    done();
                }
            };

            spyOn(config, 'onResize').and.callThrough();

            Mozilla.FxaIframe.init(config);

            window.postMessage(JSON.stringify(messageData), '*');
        });

        it('should execute callback for form_engaged postMessage', function(done) {
            var messageData = {
                command: 'form_engaged'
            };

            config = {
                onFormEngaged: function(data) {
                    var command = data.command;
                    expect(config.onFormEngaged).toHaveBeenCalled();
                    expect(command).toEqual('form_engaged');
                    done();
                }
            };

            spyOn(config, 'onFormEngaged').and.callThrough();

            Mozilla.FxaIframe.init(config);

            window.postMessage(JSON.stringify(messageData), '*');
        });

        it('should execute callback for form_disabled postMessage', function(done) {
            var messageData = {
                command: 'form_disabled'
            };

            config = {
                onFormDisabled: function(data) {
                    var command = data.command;
                    expect(config.onFormDisabled).toHaveBeenCalled();
                    expect(command).toEqual('form_disabled');
                    done();
                }
            };

            spyOn(config, 'onFormDisabled').and.callThrough();

            Mozilla.FxaIframe.init(config);

            window.postMessage(JSON.stringify(messageData), '*');
        });

        it('should execute callback for navigated postMessage', function(done) {
            var messageData = {
                command: 'navigated'
            };

            config = {
                onNavigated: function(data) {
                    var command = data.command;
                    expect(config.onNavigated).toHaveBeenCalled();
                    expect(command).toEqual('navigated');
                    done();
                }
            };

            spyOn(config, 'onNavigated').and.callThrough();

            Mozilla.FxaIframe.init(config);

            window.postMessage(JSON.stringify(messageData), '*');
        });

        it('should execute callback for signup_must_verify postMessage', function(done) {
            var messageData = {
                command: 'signup_must_verify',
                data: {}
            };

            config = {
                onSignupMustVerify: function(data) {
                    var command = data.command;
                    expect(config.onSignupMustVerify).toHaveBeenCalled();
                    expect(command).toEqual('signup_must_verify');
                    done();
                }
            };

            spyOn(config, 'onSignupMustVerify').and.callThrough();

            Mozilla.FxaIframe.init(config);

            window.postMessage(JSON.stringify(messageData), '*');
        });

        it('should execute callback for verification_complete postMessage', function(done) {
            var messageData = {
                command: 'verification_complete'
            };

            config = {
                onVerificationComplete: function(data) {
                    var command = data.command;
                    expect(config.onVerificationComplete).toHaveBeenCalled();
                    expect(command).toEqual('verification_complete');
                    done();
                }
            };

            spyOn(config, 'onVerificationComplete').and.callThrough();

            Mozilla.FxaIframe.init(config);

            window.postMessage(JSON.stringify(messageData), '*');
        });

        it('should redirect the user to FxA host /settings URL if no custom handler defined', function(done) {
            var messageData = {
                command: 'login'
            };

            spyOn(Mozilla.Utils, 'doRedirect').and.callFake(function(destination) {
                expect(destination).toEqual(fxaHost + '/settings?service=sync');
                done();
            });

            Mozilla.FxaIframe.init();

            window.postMessage(JSON.stringify(messageData), '*');
        });

        it('should execute callback for login postMessage', function(done) {
            var messageData = {
                command: 'login'
            };

            config = {
                onLogin: function(data) {
                    var command = data.command;
                    expect(config.onLogin).toHaveBeenCalled();
                    expect(command).toEqual('login');
                    done();
                }
            };

            spyOn(config, 'onLogin').and.callThrough();

            Mozilla.FxaIframe.init(config);

            window.postMessage(JSON.stringify(messageData), '*');
        });
    });
});
