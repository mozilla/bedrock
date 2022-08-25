/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

import { checkEmailValidity } from '../../../../media/js/newsletter/form-utils.es6';

describe('checkEmailValidity', function () {
    it('should return true for primitive email format', function () {
        expect(checkEmailValidity('a@a')).toBeTruthy();
        expect(checkEmailValidity('example@example.com')).toBeTruthy();
    });

    it('should return false for anything else', function () {
        expect(checkEmailValidity(1234567890)).toBeFalsy();
        expect(checkEmailValidity('aaa')).toBeFalsy();
        expect(checkEmailValidity(null)).toBeFalsy();
        expect(checkEmailValidity(undefined)).toBeFalsy();
        expect(checkEmailValidity(true)).toBeFalsy();
        expect(checkEmailValidity(false)).toBeFalsy();
    });
});
