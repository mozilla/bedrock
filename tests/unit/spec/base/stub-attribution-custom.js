/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, it, expect */

describe('stub-attribution-custom.js', function () {

    'use strict';

    var params = {
        /* eslint-disable camelcase */
        utm_source: 'www.mozilla.org',
        utm_medium: 'download_button',
        utm_campaign: 'download_thanks_page',
        utm_content: 'download_thanks_experiment'
        /* eslint-enable camelcase */
    };

    describe('setAttributionValues', function () {

        it('should return custom attribution parameters as expected', function () {
            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue({});

            var result = Mozilla.CustomStubAttribution.setAttributionValues(params);
            expect(result.utm_source).toEqual('www.mozilla.org');
            expect(result.utm_medium).toEqual('download_button');
            expect(result.utm_campaign).toEqual('download_thanks_page');
            expect(result.utm_content).toEqual('download_thanks_experiment');
        });

        it('should call return false if there is already utm_content', function() {
            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue({
                /* eslint-disable camelcase */
                utm_content: 'some-other-content'
                /* eslint-enable camelcase */
            });

            var result = Mozilla.CustomStubAttribution.setAttributionValues(params);
            expect(result).toBeFalsy();
        });

        it('should call return false if utm_source is addons.mozilla.org', function() {
            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue({
                /* eslint-disable camelcase */
                utm_campaign: 'non-fx-button',
                utm_medium: 'referral',
                utm_source: 'addons.mozilla.org'
                /* eslint-enable camelcase */
            });

            var result = Mozilla.CustomStubAttribution.setAttributionValues(params);
            expect(result).toBeFalsy();
        });

        it('should return false if custom attribution data is not fully formed', function() {
            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue({});

            var params = {
                /* eslint-disable camelcase */
                utm_source: 'www.mozilla.org',
                utm_medium: 'download_button',
                utm_content: 'download_thanks_experiment'
                /* eslint-enable camelcase */
            };

            var result = Mozilla.CustomStubAttribution.setAttributionValues(params);
            expect(result).toBeFalsy();
        });

        it('should not override any other existing utm params', function() {
            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue({
                /* eslint-disable camelcase */
                utm_source: 'support.mozilla.org',
                /* eslint-enable camelcase */
            });

            var result = Mozilla.CustomStubAttribution.setAttributionValues(params);
            expect(result.utm_source).toEqual('support.mozilla.org');
            expect(result.utm_medium).toEqual('download_button');
            expect(result.utm_campaign).toEqual('download_thanks_page');
            expect(result.utm_content).toEqual('download_thanks_experiment');
        });
    });

    describe('init', function () {

        it('should return false if stub attribution requirements are not satisfied', function() {
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(false);

            var result = Mozilla.CustomStubAttribution.init(params);
            expect(result).toBeFalsy();
        });

        it('should authenticate stub attribution data as expected', function() {
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'requestAuthentication');
            spyOn(Mozilla.CustomStubAttribution, 'setAttributionValues').and.returnValue(params);

            Mozilla.CustomStubAttribution.init(params);
            expect(Mozilla.CustomStubAttribution.setAttributionValues).toHaveBeenCalledWith(params);
            expect(Mozilla.StubAttribution.requestAuthentication).toHaveBeenCalledWith(params);
        });

        it('should fire a callback once authenticated', function() {
            var options = {
                callback: function() {} // eslint-disable-line no-empty-function
            };
            spyOn(options, 'callback');
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'requestAuthentication');

            Mozilla.CustomStubAttribution.init(params, options.callback);
            expect(options.callback).toHaveBeenCalled();
        });

        it('should call regular stub attribution flow if custom data is not satisfied', function() {
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(true);
            spyOn(Mozilla.CustomStubAttribution, 'setAttributionValues').and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'init');
            Mozilla.CustomStubAttribution.init(params);
            expect(Mozilla.StubAttribution.init).toHaveBeenCalled();
        });

    });
});
