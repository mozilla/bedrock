/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('experiment-utils.es6.js', function () {
    describe('isApprovedToRun', function () {
        it('should return true if experimental params are not found in the page URL', function () {
            const isApprovedToRun =
                require('../../../../media/js/base/experiment-utils.es6.js').isApprovedToRun;
            expect(
                isApprovedToRun('?utm_source=test&utm_campaign=test')
            ).toBeTruthy();

            expect(isApprovedToRun('')).toBeTruthy();
        });

        it('should return false if experimental params are found in the page URL', function () {
            const isApprovedToRun =
                require('../../../../media/js/base/experiment-utils.es6.js').isApprovedToRun;
            expect(isApprovedToRun('?utm_medium=cpc')).toBeFalsy();

            expect(isApprovedToRun('?utm_source=firefox-browser')).toBeFalsy();

            expect(
                isApprovedToRun(
                    '?entrypoint_experiment=test&entrypoint_variation=a'
                )
            ).toBeFalsy();

            expect(isApprovedToRun('?experiment=test&variation=a')).toBeFalsy();

            expect(isApprovedToRun('?automation=true')).toBeFalsy();
        });
    });
});
