/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, _SearchParams */

describe('search-params.js', function() {

    'use strict';

    describe('_SearchParams', function () {

        var params = new _SearchParams('scene=2&source=getfirefox');

        it('should return a proper value', function () {
            expect(params.get('scene')).toEqual(2);
            expect(params.get('source')).toEqual('getfirefox');
            expect(params.get('utm_campaign')).toBeUndefined();
        });

        it('should set a proper value', function () {
            params.set('scene', '3');
            params.set('utm_medium', 'referral');
            expect(params.get('scene')).toEqual(3);
            expect(params.get('utm_medium')).toEqual('referral');
        });

        it('should detect if the key exists', function () {
            expect(params.has('scene')).toBeTruthy();
            expect(params.has('utm_medium')).toBeTruthy();
            expect(params.has('utm_source')).toBeFalsy();
        });

        it('should remove a value', function () {
            params.remove('utm_medium');
            expect(params.has('utm_medium')).toBeFalsy();
            expect(params.get('utm_medium')).toBeUndefined();
        });

        it('should return a param string', function () {
            expect(params.toString()).toEqual('scene=3&source=getfirefox');
        });

        it('should return an object of utm_ values', function () {
            var sp = new _SearchParams('utm_dude=lebowski&utm_sport=bowling&source=getfirefox');
            var utms = sp.utmParams();
            var keys = Object.keys(utms);
            expect(keys).toEqual(['utm_dude', 'utm_sport']);
            expect(utms.utm_dude).toEqual('lebowski');
            expect(utms.utm_sport).toEqual('bowling');
        });

        it('should return an object of utm_ values with defaults for FxA', function () {
            var sp = new _SearchParams('utm_dude=lebowski&utm_sport=bowling&source=getfirefox');
            var utms = sp.utmParamsFxA('/es-ES/firefox/sync/');
            expect(utms.utm_dude).toEqual('lebowski');
            expect(utms.utm_campaign).toEqual('page referral - not part of a campaign');
            expect(utms.utm_content).toEqual('/firefox/sync/');
        });

        it('should return an object of string utm_ values for FxA', function () {
            var sp = new _SearchParams('utm_dude=lebowski&utm_strikes=10&source=getfirefox');
            var utms = sp.utmParamsFxA('/es-ES/firefox/sync/');
            expect(utms.utm_dude).toEqual('lebowski');
            expect(utms.utm_strikes).not.toEqual(10);
            expect(utms.utm_strikes).toEqual('10');
            expect(utms.utm_content).toEqual('/firefox/sync/');
        });

        it('should not override utm_campaign when set in URL', function () {
            var sp = new _SearchParams('utm_dude=lebowski&utm_campaign=bowling&source=getfirefox');
            var utms = sp.utmParamsFxA();
            expect(utms.utm_campaign).toEqual('bowling');
        });

    });

});
