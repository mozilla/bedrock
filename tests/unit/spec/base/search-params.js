/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect, sinon, spyOn */

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

    });

});
