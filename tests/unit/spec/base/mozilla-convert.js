/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-convert.js', function () {
    describe('getCurrentExperiment', function () {
        it('should return the current experiment name and variation', function () {
            const data = {
                data: {
                    experiments: {
                        10033458: {
                            n: 'Test #10033458'
                        },
                        10033459: {
                            n: 'Test #10033459'
                        }
                    }
                },
                currentData: {
                    experiments: {
                        10033458: {
                            variation_name: 'Var #100361887'
                        }
                    }
                }
            };

            const result = Mozilla.Convert.getCurrentExperiment(data);
            expect(result.experimentName).toEqual('10033458');
            expect(result.experimentVariation).toEqual('100361887');
        });

        it('should be falsy if no experiment is running', function () {
            const data = {
                data: {
                    experiments: {
                        10033458: {
                            n: 'Test #10033458'
                        },
                        10033459: {
                            n: 'Test #10033459'
                        }
                    }
                },
                currentData: {
                    experiments: {}
                }
            };

            const result = Mozilla.Convert.getCurrentExperiment(data);
            expect(result).toBeFalsy();
        });
    });
});
