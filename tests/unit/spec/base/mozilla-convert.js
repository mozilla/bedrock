/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-convert.js', function() {
    'use strict';

    describe('getCurrentExperiment', function() {

        it('should return the current experiment name and variation', function() {
            var data = {
                'data': {
                    'experiments': {
                        '10033458': {
                            'n': 'Test #10033458'
                        },
                        '10033459': {
                            'n': 'Test #10033459'
                        }
                    }
                },
                'currentData': {
                    'experiments': {
                        '10033458': {
                            'variation_name': 'Var #100361887'
                        }
                    }
                }
            };

            var result = Mozilla.Convert.getCurrentExperiment(data);
            expect(result.experimentName).toEqual('10033458');
            expect(result.experimentVariation).toEqual('100361887');
        });

        it('should be falsy if no experiment is running', function() {
            var data = {
                'data': {
                    'experiments': {
                        '10033458': {
                            'n': 'Test #10033458'
                        },
                        '10033459': {
                            'n': 'Test #10033459'
                        }
                    }
                },
                'currentData': {
                    'experiments': {}
                }
            };

            var result = Mozilla.Convert.getCurrentExperiment(data);
            expect(result).toBeFalsy();
        });
    });
});
