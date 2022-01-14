/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global _SearchParams */

describe('search-params.js', function () {
    describe('_SearchParams', function () {
        it('should return a proper value', function () {
            const params = new _SearchParams('scene=2&source=getfirefox');
            expect(params.get('scene')).toEqual(2);
            expect(params.get('source')).toEqual('getfirefox');
            expect(params.get('utm_campaign')).toBeUndefined();
        });

        it('should set a proper value', function () {
            const params = new _SearchParams('scene=2&source=getfirefox');
            params.set('scene', '3');
            params.set('utm_medium', 'referral');
            expect(params.get('scene')).toEqual(3);
            expect(params.get('utm_medium')).toEqual('referral');
        });

        it('should detect if the key exists', function () {
            const params = new _SearchParams('scene=2&source=getfirefox');
            expect(params.has('scene')).toBeTruthy();
            expect(params.has('source')).toBeTruthy();
            expect(params.has('utm_source')).toBeFalsy();
        });

        it('should remove a value', function () {
            const params = new _SearchParams('scene=2&source=getfirefox');
            params.remove('utm_medium');
            expect(params.has('utm_medium')).toBeFalsy();
            expect(params.get('utm_medium')).toBeUndefined();
        });

        it('should return a param string', function () {
            const params = new _SearchParams('scene=2&source=getfirefox');
            expect(params.toString()).toEqual('scene=2&source=getfirefox');
        });

        it('should return an object of utm_ values', function () {
            const sp = new _SearchParams(
                'utm_dude=lebowski&utm_sport=bowling&source=getfirefox'
            );
            const utms = sp.utmParams();
            const keys = Object.keys(utms);
            expect(keys).toEqual(['utm_dude', 'utm_sport']);
            expect(utms.utm_dude).toEqual('lebowski');
            expect(utms.utm_sport).toEqual('bowling');
        });

        it('should return an object of utm_ values with defaults for FxA', function () {
            const sp = new _SearchParams(
                'utm_dude=lebowski&utm_sport=bowling&source=getfirefox'
            );
            const utms = sp.utmParamsFxA('/es-ES/firefox/sync/');
            expect(utms.utm_dude).toEqual('lebowski');
            expect(utms.utm_campaign).toEqual(
                'page referral - not part of a campaign'
            );
            expect(utms.utm_content).toEqual('/firefox/sync/');
        });

        it('should return an object of string utm_ values for FxA', function () {
            const sp = new _SearchParams(
                'utm_dude=lebowski&utm_strikes=10&source=getfirefox'
            );
            const utms = sp.utmParamsFxA('/es-ES/firefox/sync/');
            expect(utms.utm_dude).toEqual('lebowski');
            expect(utms.utm_strikes).not.toEqual(10);
            expect(utms.utm_strikes).toEqual('10');
            expect(utms.utm_content).toEqual('/firefox/sync/');
        });

        it('should not override utm_campaign when set in URL', function () {
            const sp = new _SearchParams(
                'utm_dude=lebowski&utm_campaign=bowling&source=getfirefox'
            );
            const utms = sp.utmParamsFxA();
            expect(utms.utm_campaign).toEqual('bowling');
        });
    });
});
