/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global sinon */
/* eslint new-cap: [2, {"capIsNewExceptions": ["Deferred"]}] */

describe('stub-attribution.js', function () {
    const GA_VISIT_ID = '1456954538.1610960957';

    describe('init', function () {
        let data = {};

        beforeEach(function () {
            /* eslint-disable camelcase */
            data = {
                utm_source: 'desktop-snippet',
                utm_medium: 'referral',
                utm_campaign: 'F100_4242_otherstuff_in_here',
                utm_content: 'rel-esr',
                referrer: '',
                ua: 'chrome'
            };
            /* eslint-enable camelcase */

            spyOn(Mozilla.StubAttribution, 'requestAuthentication');
            spyOn(Mozilla.StubAttribution, 'updateBouncerLinks');

            // stub out GA client ID
            spyOn(Mozilla.StubAttribution, 'getGAVisitID').and.returnValue(
                GA_VISIT_ID
            );
        });

        it('should update download links if session cookie exists', function () {
            /* eslint-disable camelcase */
            const cookieData = {
                attribution_code: 'foo',
                attribution_sig: 'bar'
            };
            /* eslint-enable camelcase */
            spyOn(
                Mozilla.StubAttribution,
                'withinAttributionRate'
            ).and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(
                true
            );
            spyOn(Mozilla.StubAttribution, 'hasValidData').and.returnValue(
                true
            );
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'getCookie').and.returnValue(
                cookieData
            );
            Mozilla.StubAttribution.init();
            expect(
                Mozilla.StubAttribution.requestAuthentication
            ).not.toHaveBeenCalled();
            expect(
                Mozilla.StubAttribution.updateBouncerLinks
            ).toHaveBeenCalledWith(cookieData);
        });

        it('should authenticate attribution data if none exists', function () {
            spyOn(
                Mozilla.StubAttribution,
                'withinAttributionRate'
            ).and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(
                true
            );
            spyOn(Mozilla.StubAttribution, 'hasValidData').and.returnValue(
                true
            );
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(false);
            spyOn(
                Mozilla.StubAttribution,
                'isFirefoxNewScene2'
            ).and.returnValue(false);
            spyOn(
                Mozilla.StubAttribution,
                'getAttributionData'
            ).and.returnValue(data);
            Mozilla.StubAttribution.init();
            expect(
                Mozilla.StubAttribution.requestAuthentication
            ).toHaveBeenCalledWith(data);
            expect(
                Mozilla.StubAttribution.updateBouncerLinks
            ).not.toHaveBeenCalled();
        });

        it('should do nothing if stub attribution requirements are not satisfied', function () {
            spyOn(
                Mozilla.StubAttribution,
                'withinAttributionRate'
            ).and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(
                false
            );
            spyOn(Mozilla.StubAttribution, 'hasValidData').and.returnValue(
                true
            );
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(false);
            spyOn(
                Mozilla.StubAttribution,
                'isFirefoxNewScene2'
            ).and.returnValue(false);
            spyOn(
                Mozilla.StubAttribution,
                'getAttributionData'
            ).and.returnValue(data);
            Mozilla.StubAttribution.init();
            expect(
                Mozilla.StubAttribution.requestAuthentication
            ).not.toHaveBeenCalled();
            expect(
                Mozilla.StubAttribution.updateBouncerLinks
            ).not.toHaveBeenCalled();
        });

        it('should do nothing if session is not within sample rate', function () {
            spyOn(
                Mozilla.StubAttribution,
                'withinAttributionRate'
            ).and.returnValue(false);
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(
                true
            );
            spyOn(Mozilla.StubAttribution, 'hasValidData').and.returnValue(
                true
            );
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(false);
            spyOn(
                Mozilla.StubAttribution,
                'isFirefoxNewScene2'
            ).and.returnValue(false);
            spyOn(
                Mozilla.StubAttribution,
                'getAttributionData'
            ).and.returnValue(data);
            Mozilla.StubAttribution.init();
            expect(
                Mozilla.StubAttribution.requestAuthentication
            ).not.toHaveBeenCalled();
            expect(
                Mozilla.StubAttribution.updateBouncerLinks
            ).not.toHaveBeenCalled();
        });

        it('should do nothing if page is scene2 of /firefox/new/', function () {
            spyOn(
                Mozilla.StubAttribution,
                'withinAttributionRate'
            ).and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(
                true
            );
            spyOn(Mozilla.StubAttribution, 'hasValidData').and.returnValue(
                true
            );
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(false);
            spyOn(
                Mozilla.StubAttribution,
                'isFirefoxNewScene2'
            ).and.returnValue(true);
            spyOn(
                Mozilla.StubAttribution,
                'getAttributionData'
            ).and.returnValue(data);
            Mozilla.StubAttribution.init();
            expect(
                Mozilla.StubAttribution.requestAuthentication
            ).not.toHaveBeenCalled();
            expect(
                Mozilla.StubAttribution.updateBouncerLinks
            ).not.toHaveBeenCalled();
        });

        it('should do nothing attribution data is invalid', function () {
            spyOn(
                Mozilla.StubAttribution,
                'withinAttributionRate'
            ).and.returnValue(true);
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(
                true
            );
            spyOn(Mozilla.StubAttribution, 'hasValidData').and.returnValue(
                false
            );
            spyOn(Mozilla.StubAttribution, 'hasCookie').and.returnValue(false);
            spyOn(
                Mozilla.StubAttribution,
                'isFirefoxNewScene2'
            ).and.returnValue(false);
            spyOn(
                Mozilla.StubAttribution,
                'getAttributionData'
            ).and.returnValue(data);
            Mozilla.StubAttribution.init();
            expect(
                Mozilla.StubAttribution.requestAuthentication
            ).not.toHaveBeenCalled();
            expect(
                Mozilla.StubAttribution.updateBouncerLinks
            ).not.toHaveBeenCalled();
        });
    });

    describe('meetsRequirements', function () {
        afterEach(function () {
            window.site.platform = 'other';
        });

        it('should return false if cookies are not enabled', function () {
            spyOn(Mozilla.Cookies, 'enabled').and.returnValue(false);
            expect(Mozilla.StubAttribution.meetsRequirements()).toBeFalsy();
        });

        it('should return false if platform is not windows', function () {
            window.site.platform = 'osx';
            expect(Mozilla.StubAttribution.meetsRequirements()).toBeFalsy();
        });

        it('should return false if browser has DNT enabled', function () {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(true);
            expect(Mozilla.StubAttribution.meetsRequirements()).toBeFalsy();
        });

        it('should return true for windows users who satisfy all other requirements', function () {
            window.site.platform = 'windows';
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            expect(Mozilla.StubAttribution.meetsRequirements()).toBeTruthy();
        });
    });

    describe('hasValidData', function () {
        it('should return true for valid attribution data', function () {
            /* eslint-disable camelcase */
            const data = {
                utm_source: 'desktop-snippet',
                utm_medium: 'referral',
                utm_campaign: 'F100_4242_otherstuff_in_here',
                utm_content: 'rel-esr',
                referrer: '',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data)).toBeTruthy();
        });

        it('should return true for valid RTAMO data', function () {
            /* eslint-disable camelcase */
            const data = {
                utm_source: 'addons.mozilla.org',
                utm_medium: 'referral',
                utm_campaign: 'non-fx-button',
                utm_content: 'rta%3Acm9uaW4td2FsbGV0QGF4aWVpbmZpbml0eS5jb20',
                referrer: 'https://addons.mozilla.org/',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data)).toBeTruthy();

            /* eslint-disable camelcase */
            const data2 = {
                utm_source: 'addons.mozilla.org',
                utm_medium: 'referral',
                utm_campaign: 'amo-fx-cta-607454',
                utm_content: 'rta:dUJsb2NrMEByYXltb25kaGlsbC5uZXQ',
                referrer: 'https://addons.mozilla.org/',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data2)).toBeTruthy();

            /* eslint-disable camelcase */
            const data3 = {
                utm_source: 'addons.mozilla.org',
                utm_medium: 'referral',
                utm_campaign: 'non-fx-button',
                utm_content: 'rta%25253AdUJsb2NrMEByYXltb25kaGlsbC5uZXQ',
                referrer: 'https://addons.mozilla.org/',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data3)).toBeTruthy();

            /* eslint-disable camelcase */
            const data4 = {
                utm_source: 'addons.mozilla.org',
                utm_medium: 'referral',
                utm_campaign: 'non-fx-button',
                utm_content: '%72%74%61%3AdUJsb2NrMEByYXltb25kaGlsbC5uZXQ',
                referrer: 'https://addons.mozilla.org/',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data4)).toBeTruthy();
        });

        it('should return false for RTAMO data that does not have AMO as the referrer', function () {
            /* eslint-disable camelcase */
            const data = {
                utm_source: 'addons.mozilla.org',
                utm_medium: 'referral',
                utm_campaign: 'non-fx-button',
                utm_content: 'rta%3Acm9uaW4td2FsbGV0QGF4aWVpbmZpbml0eS5jb20',
                referrer: 'https://example.com/',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data)).toBeFalsy();

            /* eslint-disable camelcase */
            const data2 = {
                utm_source: 'addons.mozilla.org',
                utm_medium: 'referral',
                utm_campaign: 'non-fx-button',
                utm_content: 'rta:cm9uaW4td2FsbGV0QGF4aWVpbmZpbml0eS5jb20',
                referrer: 'https://example.com/',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data2)).toBeFalsy();

            /* eslint-disable camelcase */
            const data3 = {
                utm_source: 'addons.mozilla.org',
                utm_medium: 'referral',
                utm_campaign: 'non-fx-button',
                utm_content: 'rta%25253AdUJsb2NrMEByYXltb25kaGlsbC5uZXQ',
                referrer: 'https://example.com/',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data3)).toBeFalsy();

            /* eslint-disable camelcase */
            const data4 = {
                utm_source: 'addons.mozilla.org',
                utm_medium: 'referral',
                utm_campaign: 'non-fx-button',
                utm_content: '%72%74%61%3AdUJsb2NrMEByYXltb25kaGlsbC5uZXQ',
                referrer: '',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data4)).toBeFalsy();
        });

        it('should return false if utm_content is too long', function () {
            /* eslint-disable camelcase */
            const data1 = {
                utm_source: 'addons.mozilla.org',
                utm_medium: 'referral',
                utm_campaign: 'non-fx-button',
                utm_content: `rta%${'25'.repeat(
                    58
                )}3AdUJsb2NrMEByYXltb25kaGlsbC5uZXQ`,
                referrer: '',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data1)).toBeFalsy();

            /* eslint-disable camelcase */
            const data2 = {
                utm_source: 'addons.mozilla.org',
                utm_medium: 'referral',
                utm_campaign: 'non-fx-button',
                utm_content: `rta%${'25'.repeat(
                    58
                )}3AdUJsb2NrMEByYXltb25kaGlsbC5uZXQ`,
                referrer: 'https://addons.mozilla.org/',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data2)).toBeFalsy();
        });

        it('should return false for RTAMO data if referrer is not set', function () {
            /* eslint-disable camelcase */
            const data = {
                utm_source: 'addons.mozilla.org',
                utm_medium: 'referral',
                utm_campaign: 'non-fx-button',
                utm_content: 'rta%3Acm9uaW4td2FsbGV0QGF4aWVpbmZpbml0eS5jb20',
                referrer: '',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            expect(Mozilla.StubAttribution.hasValidData(data)).toBeFalsy();
        });
    });

    describe('isFirefoxNewScene2', function () {
        it('should return true if the page is scene 2 of /firefox/new/', function () {
            const url =
                'https://www.mozilla.org/en-US/firefox/download/thanks/';
            expect(
                Mozilla.StubAttribution.isFirefoxNewScene2(url)
            ).toBeTruthy();

            const url2 =
                'https://www.mozilla.org/en-US/firefox/download/thanks/?foo=bar';
            expect(
                Mozilla.StubAttribution.isFirefoxNewScene2(url2)
            ).toBeTruthy();
        });
    });

    describe('getUserAgent', function () {
        const ie8 =
            'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)';
        const ie9 =
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)';
        const ie10 =
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)';
        const ie11 =
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko';
        const ff =
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0';
        const chrome =
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36';
        const edgeium =
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43';
        const edge =
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931';

        it('should identify Internet Explorer', function () {
            expect(Mozilla.StubAttribution.getUserAgent(ie8)).toEqual('ie');
            expect(Mozilla.StubAttribution.getUserAgent(ie9)).toEqual('ie');
            expect(Mozilla.StubAttribution.getUserAgent(ie10)).toEqual('ie');
            expect(Mozilla.StubAttribution.getUserAgent(ie11)).toEqual('ie');
        });

        it('should identify Edge', function () {
            expect(Mozilla.StubAttribution.getUserAgent(edge)).toEqual('edge');
            expect(Mozilla.StubAttribution.getUserAgent(edgeium)).toEqual(
                'edge'
            );
        });

        it('should identify Firefox', function () {
            expect(Mozilla.StubAttribution.getUserAgent(ff)).toEqual('firefox');
        });

        it('should identify Chrome', function () {
            expect(Mozilla.StubAttribution.getUserAgent(chrome)).toEqual(
                'chrome'
            );
        });
    });

    describe('waitForGoogleAnalytics', function () {
        beforeEach(function () {
            // stub out GA client ID
            spyOn(Mozilla.StubAttribution, 'getGAVisitID').and.returnValue(
                GA_VISIT_ID
            );
        });

        it('should fire a callback with the GA visit ID', function () {
            const callback = jasmine.createSpy('callback');

            Mozilla.StubAttribution.waitForGoogleAnalytics(callback);
            expect(callback).toHaveBeenCalledWith(true);
        });
    });

    describe('getAttributionData', function () {
        beforeEach(function () {
            // stub out GA client ID
            spyOn(Mozilla.StubAttribution, 'getGAVisitID').and.returnValue(
                GA_VISIT_ID
            );
        });

        it('should return attribution data if utm params are present', function () {
            const referrer = '';

            /* eslint-disable camelcase */
            const utms = {
                utm_source: 'desktop-snippet',
                utm_medium: 'referral',
                utm_campaign: 'F100_4242_otherstuff_in_here',
                utm_content: 'rel-esr'
            };
            /* eslint-enable camelcase */

            /* eslint-disable camelcase */
            const data = {
                utm_source: 'desktop-snippet',
                utm_medium: 'referral',
                utm_campaign: 'F100_4242_otherstuff_in_here',
                utm_content: 'rel-esr',
                referrer: '',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(
                utms
            );
            spyOn(Mozilla.StubAttribution, 'getUserAgent').and.returnValue(
                'chrome'
            );
            const result = Mozilla.StubAttribution.getAttributionData(referrer);
            expect(result).toEqual(data);
        });

        it('should return attribution data if referrer is present', function () {
            const referrer = 'https://www.mozilla.org/en-US/';

            /* eslint-disable camelcase */
            const utms = {
                utm_source: undefined,
                utm_medium: undefined,
                utm_campaign: undefined,
                utm_content: undefined
            };
            /* eslint-enable camelcase */

            /* eslint-disable camelcase */
            const data = {
                referrer: 'https://www.mozilla.org/en-US/',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(
                utms
            );
            spyOn(Mozilla.StubAttribution, 'getUserAgent').and.returnValue(
                'chrome'
            );
            const result = Mozilla.StubAttribution.getAttributionData(referrer);
            expect(result).toEqual(data);
        });

        it('should return only UA and GA data if neither utm params and referrer are present', function () {
            const referrer = '';

            /* eslint-disable camelcase */
            const utms = {
                utm_source: undefined,
                utm_medium: undefined,
                utm_campaign: undefined,
                utm_content: undefined
            };
            /* eslint-enable camelcase */

            /* eslint-disable camelcase */
            const data = {
                referrer: '',
                ua: 'chrome',
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(
                utms
            );
            spyOn(Mozilla.StubAttribution, 'getUserAgent').and.returnValue(
                'chrome'
            );
            const result = Mozilla.StubAttribution.getAttributionData(referrer);
            expect(result).toEqual(data);
        });

        it('should return optional experimental parameters if present', function () {
            const referrer = '';

            /* eslint-disable camelcase */
            const utms = {
                utm_source: undefined,
                utm_medium: undefined,
                utm_campaign: undefined,
                utm_content: undefined
            };
            /* eslint-enable camelcase */

            /* eslint-disable camelcase */
            const data = {
                referrer: '',
                ua: 'chrome',
                experiment: 'firefox-new',
                variation: 1,
                visit_id: GA_VISIT_ID
            };
            /* eslint-enable camelcase */

            spyOn(window._SearchParams.prototype, 'utmParams').and.returnValue(
                utms
            );
            spyOn(window._SearchParams.prototype, 'get').and.callFake(function (
                key
            ) {
                return key === 'experiment' ? 'firefox-new' : 1;
            });
            spyOn(Mozilla.StubAttribution, 'getUserAgent').and.returnValue(
                'chrome'
            );
            const result = Mozilla.StubAttribution.getAttributionData(referrer);
            expect(result).toEqual(data);
        });
    });

    describe('requestAuthentication', function () {
        let xhr;
        let xhrRequests = [];

        beforeEach(function () {
            xhr = sinon.useFakeXMLHttpRequest();
            xhr.onCreate = (req) => {
                xhrRequests.push(req);
            };
            jasmine.clock().install();
            Mozilla.StubAttribution.requestComplete = false;
        });

        afterEach(function () {
            xhr.restore();
            xhrRequests = [];
            jasmine.clock().uninstall();
            Mozilla.StubAttribution.requestComplete = false;
        });

        it('should handle a request successfully', function () {
            /* eslint-disable camelcase */
            const data = {
                attribution_code: 'foo',
                attribution_sig: 'bar'
            };
            /* eslint-enable camelcase */

            const callback = function () {}; // eslint-disable-line no-empty-function
            Mozilla.StubAttribution.successCallback = callback;

            spyOn(
                Mozilla.StubAttribution,
                'onRequestSuccess'
            ).and.callThrough();
            spyOn(Mozilla.StubAttribution, 'updateBouncerLinks');
            spyOn(Mozilla.StubAttribution, 'setCookie');
            spyOn(Mozilla.StubAttribution, 'successCallback');
            Mozilla.StubAttribution.requestAuthentication();
            xhrRequests[0].respond(
                200,
                { 'Content-Type': 'application/json' },
                JSON.stringify(data)
            );
            expect(
                Mozilla.StubAttribution.onRequestSuccess
            ).toHaveBeenCalledWith(data);
            expect(
                Mozilla.StubAttribution.updateBouncerLinks
            ).toHaveBeenCalledWith(data);
            expect(Mozilla.StubAttribution.setCookie).toHaveBeenCalledWith(
                data
            );
            expect(Mozilla.StubAttribution.successCallback).toHaveBeenCalled();
            expect(Mozilla.StubAttribution.requestComplete).toBeTruthy();
        });

        it('should handle a timeout as expected', function () {
            const callback = function () {}; // eslint-disable-line no-empty-function
            Mozilla.StubAttribution.timeoutCallback = callback;
            spyOn(
                Mozilla.StubAttribution,
                'onRequestTimeout'
            ).and.callThrough();
            spyOn(Mozilla.StubAttribution, 'timeoutCallback');
            Mozilla.StubAttribution.requestAuthentication();
            jasmine.clock().tick(10100);
            expect(Mozilla.StubAttribution.onRequestTimeout).toHaveBeenCalled();
            expect(Mozilla.StubAttribution.timeoutCallback).toHaveBeenCalled();
            expect(Mozilla.StubAttribution.requestComplete).toBeTruthy();
        });
    });

    describe('onRequestSuccess', function () {
        beforeEach(function () {
            Mozilla.StubAttribution.requestComplete = false;
        });

        afterEach(function () {
            Mozilla.StubAttribution.requestComplete = false;
        });

        it('should handle the data as expected', function () {
            /* eslint-disable camelcase */
            const data = {
                attribution_code: 'foo',
                attribution_sig: 'bar'
            };
            /* eslint-enable camelcase */

            spyOn(Mozilla.StubAttribution, 'updateBouncerLinks');
            spyOn(Mozilla.StubAttribution, 'setCookie');
            Mozilla.StubAttribution.onRequestSuccess(data);
            expect(
                Mozilla.StubAttribution.updateBouncerLinks
            ).toHaveBeenCalledWith(data);
            expect(Mozilla.StubAttribution.setCookie).toHaveBeenCalledWith(
                data
            );
            expect(Mozilla.StubAttribution.requestComplete).toBeTruthy();
        });

        it('should only handle the request once', function () {
            /* eslint-disable camelcase */
            const data = {
                attribution_code: 'foo',
                attribution_sig: 'bar'
            };
            /* eslint-enable camelcase */

            spyOn(Mozilla.StubAttribution, 'updateBouncerLinks');
            spyOn(Mozilla.StubAttribution, 'setCookie');
            Mozilla.StubAttribution.requestComplete = true;
            Mozilla.StubAttribution.onRequestSuccess(data);
            expect(
                Mozilla.StubAttribution.updateBouncerLinks
            ).not.toHaveBeenCalled();
            expect(Mozilla.StubAttribution.setCookie).not.toHaveBeenCalled();
        });
    });

    describe('updateBouncerLinks', function () {
        /* eslint-disable camelcase */
        const data = {
            attribution_code: 'test-code',
            attribution_sig: 'test-sig'
        };
        /* eslint-enable camelcase */

        const winUrl =
            'https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US';
        const win64Url =
            'https://download.mozilla.org/?product=firefox-50.0b11-SSL&os=win64&lang=en-US';
        const transitionalUrl =
            'https://www.mozilla.org/firefox/download/thanks/';

        beforeEach(function () {
            const downloadMarkup = `<ul class="download-list">
                    <li><a id="link-transitional" class="download-link" data-download-version="win" href="${transitionalUrl}" data-direct-link="${winUrl}">Download</a></li>
                    <li><a id="link-direct-win" class="download-link" data-download-version="win" href="${winUrl}">Download</a></li>
                    <li><a id="link-direct-win64" class="download-link" data-download-version="win64" href="${win64Url}">Download</a></li>
                </ul>`;

            document.body.insertAdjacentHTML('beforeend', downloadMarkup);
        });

        afterEach(function () {
            const content = document.querySelector('.download-list');
            content.parentNode.removeChild(content);
        });

        it('should update download links with attribution data as expected', function () {
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(
                true
            );
            Mozilla.StubAttribution.updateBouncerLinks(data);
            expect(document.getElementById('link-transitional').href).toEqual(
                'https://www.mozilla.org/firefox/download/thanks/'
            );
            expect(
                document
                    .getElementById('link-transitional')
                    .getAttribute('data-direct-link')
            ).toEqual(
                'https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US&attribution_code=test-code&attribution_sig=test-sig'
            );
            expect(document.getElementById('link-direct-win').href).toEqual(
                'https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US&attribution_code=test-code&attribution_sig=test-sig'
            );
            expect(document.getElementById('link-direct-win64').href).toEqual(
                'https://download.mozilla.org/?product=firefox-50.0b11-SSL&os=win64&lang=en-US&attribution_code=test-code&attribution_sig=test-sig'
            );
        });

        it('should do nothing if stub attribution requirements are not satisfied', function () {
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(
                false
            );
            spyOn(Mozilla.StubAttribution, 'appendToDownloadURL');
            Mozilla.StubAttribution.updateBouncerLinks(data);
            expect(
                Mozilla.StubAttribution.appendToDownloadURL
            ).not.toHaveBeenCalled();
        });

        it('should do nothing if attribution data is not as expected', function () {
            spyOn(Mozilla.StubAttribution, 'meetsRequirements').and.returnValue(
                true
            );
            spyOn(Mozilla.StubAttribution, 'appendToDownloadURL');
            Mozilla.StubAttribution.updateBouncerLinks({});
            expect(
                Mozilla.StubAttribution.appendToDownloadURL
            ).not.toHaveBeenCalled();
        });
    });

    describe('appendToDownloadURL', function () {
        let params = {};
        let originalUrl = '';
        let expectedUrl = '';

        beforeEach(function () {
            /* eslint-disable camelcase */
            params = {
                attribution_code:
                    'source%3Dbrandt%26medium%3Daether%26campaign%3D%28not+set%29%26content%3D%28not+set%29%26timestamp%3D1478181983',
                attribution_sig:
                    '241c4ef87bd2554154c5658d99230660d4c242abbe1ac87b89ac0e9dd56b2f4e'
            };
            /* eslint-enable camelcase */

            originalUrl =
                'https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US';
            expectedUrl =
                'https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US&attribution_code=source%3Dbrandt%26medium%3Daether%26campaign%3D%28not+set%29%26content%3D%28not+set%29%26timestamp%3D1478181983&attribution_sig=241c4ef87bd2554154c5658d99230660d4c242abbe1ac87b89ac0e9dd56b2f4e';
        });

        it('should append stub attribution data to url', function () {
            expect(
                Mozilla.StubAttribution.appendToDownloadURL(originalUrl, params)
            ).toEqual(expectedUrl);
        });

        it('should return original url if stub attribution data is missing', function () {
            params = {};
            expect(
                Mozilla.StubAttribution.appendToDownloadURL(originalUrl, params)
            ).toEqual(originalUrl);
        });

        it('should ignore any other parameters', function () {
            params['foo'] = 'bar';
            expect(
                Mozilla.StubAttribution.appendToDownloadURL(originalUrl, params)
            ).toEqual(expectedUrl);
        });
    });

    describe('getCookie', function () {
        it('should return an object as expected', function () {
            spyOn(Mozilla.Cookies, 'getItem').and.callFake((id) => {
                return id === Mozilla.StubAttribution.COOKIE_CODE_ID
                    ? 'foo'
                    : 'bar';
            });
            /* eslint-disable camelcase */
            expect(Mozilla.StubAttribution.getCookie()).toEqual({
                attribution_code: 'foo',
                attribution_sig: 'bar'
            });
            /* eslint-enable camelcase */
            expect(Mozilla.Cookies.getItem.calls.count()).toEqual(2);
        });
    });

    describe('setCookie', function () {
        beforeEach(function () {
            spyOn(Mozilla.Cookies, 'setItem');
        });

        it('should set session cookies as expected', function () {
            /* eslint-disable camelcase */
            const data = {
                attribution_code: 'foo',
                attribution_sig: 'bar'
            };
            /* eslint-enable camelcase */

            Mozilla.StubAttribution.setCookie(data);
            expect(Mozilla.Cookies.setItem.calls.count()).toEqual(2);
            expect(Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                Mozilla.StubAttribution.COOKIE_CODE_ID,
                data.attribution_code,
                jasmine.any(String),
                '/',
                undefined,
                false,
                'lax'
            );
            expect(Mozilla.Cookies.setItem).toHaveBeenCalledWith(
                Mozilla.StubAttribution.COOKIE_SIGNATURE_ID,
                data.attribution_sig,
                jasmine.any(String),
                '/',
                undefined,
                false,
                'lax'
            );
        });

        it('should not set session cookies if data is not passed', function () {
            Mozilla.StubAttribution.setCookie({});
            expect(Mozilla.Cookies.setItem).not.toHaveBeenCalled();
        });
    });

    describe('hasCookie', function () {
        it('should return true if both session cookies exists', function () {
            spyOn(Mozilla.Cookies, 'hasItem').and.returnValue(true);
            const result = Mozilla.StubAttribution.hasCookie();
            expect(Mozilla.Cookies.hasItem.calls.count()).toEqual(2);
            expect(Mozilla.Cookies.hasItem).toHaveBeenCalledWith(
                Mozilla.StubAttribution.COOKIE_CODE_ID
            );
            expect(Mozilla.Cookies.hasItem).toHaveBeenCalledWith(
                Mozilla.StubAttribution.COOKIE_SIGNATURE_ID
            );
            expect(result).toBeTruthy();
        });

        it('should return false if one or more session cookies do not exist', function () {
            spyOn(Mozilla.Cookies, 'hasItem').and.callFake((id) => {
                return id === Mozilla.StubAttribution.COOKIE_CODE_ID
                    ? true
                    : false;
            });
            const result = Mozilla.StubAttribution.hasCookie();
            expect(Mozilla.Cookies.hasItem.calls.count()).toEqual(2);
            expect(result).toBeFalsy();
        });
    });

    describe('getAttributionRate', function () {
        const html = document.documentElement;
        const attr = 'data-stub-attribution-rate';

        afterEach(function () {
            html.removeAttribute(attr);
        });

        it('should return the stub attribution rate as expected', function () {
            html.setAttribute(attr, '0.5');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(0.5);
        });

        it('should return 0 if data attribute is not present', function () {
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(0);
        });

        it('should not return negative values', function () {
            html.setAttribute(attr, '-0.5');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(0);
            html.setAttribute(attr, '-1');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(0);
        });

        it('should not return values greater than 1', function () {
            html.setAttribute(attr, '1.5');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(1);
            html.setAttribute(attr, '2');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(1);
        });

        it('should not return other values', function () {
            html.setAttribute(attr, 'foo');
            expect(Mozilla.StubAttribution.getAttributionRate()).toEqual(0);
        });
    });

    describe('withinAttributionRate', function () {
        beforeEach(function () {
            spyOn(
                Mozilla.StubAttribution,
                'getAttributionRate'
            ).and.returnValue(0.5);
        });

        it('should return true if within sample rate', function () {
            spyOn(window.Math, 'random').and.returnValue(0.3);
            expect(
                Mozilla.StubAttribution.withinAttributionRate()
            ).toBeTruthy();
        });

        it('should return false if exceeds sample rate', function () {
            spyOn(window.Math, 'random').and.returnValue(0.6);
            expect(Mozilla.StubAttribution.withinAttributionRate()).toBeFalsy();
        });
    });

    describe('getGAVisitID', function () {
        it('should return a valid Google Analytics visit ID', function () {
            window.ga = sinon.stub();
            window.ga.getAll = sinon.stub().returns([
                {
                    get: () => GA_VISIT_ID
                }
            ]);

            expect(Mozilla.StubAttribution.getGAVisitID()).toEqual(GA_VISIT_ID);
        });

        it('should return a null if Google Analytics visit ID is invalid', function () {
            window.ga = sinon.stub();
            window.ga.getAll = sinon.stub().returns([
                {
                    get: () => ''
                }
            ]);

            expect(Mozilla.StubAttribution.getGAVisitID()).toBeNull();
        });

        it('should return a null if accessing Google Analytics object throws an error', function () {
            window.ga = sinon.stub().throws(function () {
                return new Error();
            });
            expect(Mozilla.StubAttribution.getGAVisitID()).toBeNull();
        });
    });
});
