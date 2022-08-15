/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import { isApprovedToRun } from '../../../../media/js/base/experiment-utils.es6';

describe('experiment-utils.es6.js', function () {
    describe('isApprovedToRun', function () {
        it('should return true if experimental params are not found in the page URL', function () {
            expect(
                isApprovedToRun('?utm_source=test&utm_campaign=test')
            ).toBeTrue();
            expect(isApprovedToRun('')).toBeTrue();
        });

        it('should return false if experimental params are found in the page URL', function () {
            expect(isApprovedToRun('?utm_medium=cpc')).toBeFalse();
            expect(isApprovedToRun('?utm_source=firefox-browser')).toBeFalse();
            expect(
                isApprovedToRun(
                    '?entrypoint_experiment=test&entrypoint_variation=a'
                )
            ).toBeFalse();
            expect(isApprovedToRun('?experiment=test&variation=a')).toBeFalse();
            expect(isApprovedToRun('?automation=true')).toBeFalse();
            expect(isApprovedToRun('?cjevent=1234567890')).toBeFalse();
        });
    });
});
