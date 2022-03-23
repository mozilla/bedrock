/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

/*
|*|  * Mozilla.Cookies.getItem(name)
|*|  * Mozilla.Cookies.removeItem(name[, path[, domain]])
|*|  * Mozilla.Cookies.hasItem(name)
|*|  * Mozilla.Cookies.keys()
*/

describe('mozilla-cookie-helper.js', function () {
    function clearCookies() {
        document.cookies = '';
    }

    beforeEach(clearCookies);
    afterEach(clearCookies);

    describe('setItem method', function () {
        const cookieId = 'test-cookie';
        var date = new Date();
        date.setHours(date.getHours() + 48);

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

    describe('getItem method', function () {
        const cookieId = 'test-cookie';
        var date = new Date();
        date.setHours(date.getHours() + 48);
        window.Mozilla.Cookies.setItem(cookieId, 'test', date, '/');

        it('should return the value of the cookie that is passed to the getItem method', function () {
            expect(window.Mozilla.Cookies.getItem(cookieId)).toBe('test');
        });

        it('should return null if no cookie with that name is found', function () {
            expect(
                window.Mozilla.Cookies.getItem("Nathan's secret stuff")
            ).toBeNull();
        });
        it('should return null if no argument for sKey is passed', function () {
            expect(window.Mozilla.Cookies.getItem()).toBeNull();
        });
    });

    describe('hasItem method', function () {
        const cookieId = 'test-cookie';
        var date = new Date();
        date.setHours(date.getHours() + 48);
        window.Mozilla.Cookies.setItem(cookieId, 'test', date, '/');

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
});
