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
    describe('setItem method', function () {
        const cookieId = 'test-cookie';
        it('should set a cookie onto document.cookie', function () {
            var date = new Date();
            date.setHours(date.getHours() + 48);
            window.Mozilla.Cookies.setItem(cookieId, true, date, '/');
            expect(document.cookie).toContain(cookieId);
        });
    });
});
