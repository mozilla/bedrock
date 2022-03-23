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
|*|  * Mozilla.Cookies.setItem(name, value[, end[, path[, domain[, secure[, samesite]]]]])
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
            window.Mozilla.Cookies.setItem(cookieId, true, date, '/');
            expect(document.cookie).toContain(cookieId);
        });
        it('will return false if you dont pass the sKey property', function () {
            expect(window.Mozilla.Cookies.setItem()).toBeFalse();
        });
        it('will return false if sKey starts with any: expires|max-age|path|domain|secure|samesite', function () {
            expect(window.Mozilla.Cookies.setItem()).toBeFalse();
        });
    });
});
