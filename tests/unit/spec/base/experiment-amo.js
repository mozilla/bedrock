/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import { getAMOExperiment } from '../../../../media/js/base/experiment-amo.es6';

describe('experiment-amo.js', function () {
    describe('getAMOExperiment', function () {
        it('should return true when experiment and variation params are well formatted', function () {
            const params = {
                experiment: '20210708_amo_experiment_name',
                variation: 'variation_1_name'
            };
            expect(getAMOExperiment(params)).toEqual(params);
        });

        it('should return falsy when experiment and variation params are not specific to amo', function () {
            const params = {
                experiment: 'some_other_experiment',
                variation: 'variation_1_name'
            };
            expect(getAMOExperiment(params)).toBeFalsy();
        });

        it('should return falsy when experiment and variation params contain dangerous characters', function () {
            const params = {
                experiment: '20210708_amo_"><h1>hello</h1>',
                variation: '<script>alert("test");</script>'
            };
            expect(getAMOExperiment(params)).toBeFalsy();

            const params2 = {
                experiment: '20210708_amo_%22%3E%3Ch1%3Ehello%3C%2Fh1%3E',
                variation: '%3Cscript%3Ealert%28%22test%22%29%3B%3C%2Fscript%3E'
            };
            expect(getAMOExperiment(params2)).toBeFalsy();
        });

        it('should return falsy if parameters values are more than 50 chars', function () {
            const params = {
                experiment: '20210708_amo_experiment_name',
                variation:
                    'a_very_very_very_very_very_long_experiment_variation_name_much_much_much_more_than_50_chars'
            };
            expect(getAMOExperiment(params)).toBeFalsy();

            const params2 = {
                experiment:
                    '20210708_amo_a_very_very_very_long_experiment_name_much_much_much_much_more_than_50_chars',
                variation: 'variation_1_name'
            };
            expect(getAMOExperiment(params2)).toBeFalsy();
        });
    });
});
