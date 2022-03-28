/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-cookie-helper.js', function () {
    function clearCookies() {
        document.cookie = '';
    }

    beforeEach(clearCookies);
    afterEach(clearCookies);

    describe('setItem method', function () {
        const cookieId = 'test-cookie';
        var date = new Date();
        date.setHours(date.getHours() + 48);

        beforeEach(clearCookies);
        afterEach(clearCookies);

        it('should set a cookie onto document.cookie', function () {
            window.Mozilla.Cookies.setItem(cookieId, 'test', date, '/');
            expect(document.cookie).toContain(cookieId);
        });

        it('will return false if you dont pass the sKey property', function () {
            expect(window.Mozilla.Cookies.setItem()).toBeFalse();
        });

        it('will return false if sKey equals any of the folllowing: expires|max-age|path|domain|secure|samesite', function () {
            expect(window.Mozilla.Cookies.setItem('expires')).toBeFalse();
            expect(window.Mozilla.Cookies.setItem('max-age')).toBeFalse();
            expect(window.Mozilla.Cookies.setItem('path')).toBeFalse();
            expect(window.Mozilla.Cookies.setItem('domain')).toBeFalse();
            expect(window.Mozilla.Cookies.setItem('secure')).toBeFalse();
            expect(window.Mozilla.Cookies.setItem('samesite')).toBeFalse();
        });
    });

    describe('checkSameSite method', function () {
        const cookieId = 'test-cookie';
        var date = new Date();
        date.setHours(date.getHours() + 48);

        beforeEach(clearCookies);
        afterEach(clearCookies);

        it('should be called when calling Mozilla.Cookies.setItem', function () {
            const spy = spyOn(window.Mozilla.Cookies, 'checkSameSite');
            window.Mozilla.Cookies.setItem(cookieId);
            expect(spy).toHaveBeenCalled();
        });

        it('should return null if no argument is passed', function () {
            expect(window.Mozilla.Cookies.checkSameSite()).toBeNull();
        });

        it('should return "lax" if a truthy string is passed (but not strict | none)', function () {
            expect(window.Mozilla.Cookies.checkSameSite('flour')).toBe('lax');
            expect(window.Mozilla.Cookies.checkSameSite('lax')).toBe('lax');
        });
        it('should return "none" if "none" is passed to function', function () {
            expect(window.Mozilla.Cookies.checkSameSite('none')).toBe('none');
        });

        it('should return "lax" if "lax" is passed to function', function () {
            expect(window.Mozilla.Cookies.checkSameSite('none')).toBe('none');
        });
    });

    describe('getItem method', function () {
        const cookieId = 'test-cookie';
        var date = new Date();
        date.setHours(date.getHours() + 48);

        beforeEach(function () {
            clearCookies();
            window.Mozilla.Cookies.setItem(cookieId, 'test', date, '/');
        });

        afterEach(clearCookies);

        it('should return the value of the cookie that is passed to the getItem method', function () {
            expect(window.Mozilla.Cookies.getItem(cookieId)).toBe('test');
        });

        it('should return null if no cookie with that name is found', function () {
            expect(window.Mozilla.Cookies.getItem('oatmeal-raisin')).toBeNull();
        });
        it('should return null if no argument for sKey is passed', function () {
            expect(window.Mozilla.Cookies.getItem()).toBeNull();
        });
    });

    describe('hasItem method', function () {
        const cookieId = 'test-cookie';
        var date = new Date();
        date.setHours(date.getHours() + 48);

        beforeEach(function () {
            clearCookies();
            window.Mozilla.Cookies.setItem(cookieId, 'test', date, '/');
        });

        afterEach(clearCookies);

        it('should return false if no argument for sKey is passed', function () {
            expect(window.Mozilla.Cookies.hasItem()).toBeFalse();
        });
        it('should return false if no matching cookie is found', function () {
            expect(
                window.Mozilla.Cookies.hasItem('chocolate-chip')
            ).toBeFalse();
        });
        it('should return true if matching cookie is found', function () {
            expect(window.Mozilla.Cookies.hasItem(cookieId)).toBeTrue();
        });
    });

    describe('removeItem method', function () {
        const cookieId = 'test-cookie';
        var date = new Date();
        date.setHours(date.getHours() + 48);

        beforeEach(function () {
            clearCookies();
            window.Mozilla.Cookies.setItem(cookieId, 'test', date, '/');
        });

        afterEach(clearCookies);

        it('should return false if the cookie doesnt exist', function () {
            expect(
                window.Mozilla.Cookies.removeItem('snickerdoodle')
            ).toBeFalse();
        });

        it('should return true if the cookie is found in document.cookie', function () {
            expect(window.Mozilla.Cookies.removeItem(cookieId)).toBeTrue();
        });
    });

    describe('keys method', function () {
        const cookieId = 'test-cookie';
        var date = new Date();
        date.setHours(date.getHours() + 48);

        beforeEach(clearCookies);

        afterEach(clearCookies);

        it('should return the cookie keys found in document.cookie', function () {
            window.Mozilla.Cookies.setItem(cookieId, 'test', date, '/');
            expect(window.Mozilla.Cookies.keys()).toContain(cookieId);
            expect(window.Mozilla.Cookies.keys().length).toEqual(1);
            window.Mozilla.Cookies.setItem(
                'oatmeal-chocolate-chip',
                'tasty',
                date,
                '/'
            );
            expect(window.Mozilla.Cookies.keys().length).toEqual(2);
        });
    });
});
