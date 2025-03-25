/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import { meetsExperimentCriteria } from '../../../../../../media/js/firefox/new/desktop/default-experiment-criteria.es6';

describe('default-experiment-criteria.es6.js', function () {
    describe('meetsExperimentCriteria', function () {
        it('should return false if platform is not windows', function () {
            expect(meetsExperimentCriteria('osx')).toBeFalse();
            expect(meetsExperimentCriteria('linux')).toBeFalse();
            expect(meetsExperimentCriteria('ios')).toBeFalse();
            expect(meetsExperimentCriteria('android')).toBeFalse();
            expect(meetsExperimentCriteria('other')).toBeFalse();
        });

        it('should return false if cookies are disabled', function () {
            spyOn(window.Mozilla.Cookies, 'enabled').and.returnValue(false);
            expect(meetsExperimentCriteria('windows')).toBeFalse();
        });

        it('should return false if consent cookie rejects analytics', function () {
            spyOn(window.Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'hasItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'getItem').and.returnValue(
                JSON.stringify({
                    analytics: false,
                    preference: true
                })
            );

            expect(meetsExperimentCriteria('windows')).toBeFalse();
        });

        it('should return false if UTM params are already present', function () {
            spyOn(window.Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(false);

            expect(
                meetsExperimentCriteria(
                    'windows',
                    'utm_source=test&utm_campaign=test'
                )
            ).toBeFalse();
            expect(
                meetsExperimentCriteria(
                    'osx',
                    'utm_medium=test&utm_term=test&utm_content=test'
                )
            ).toBeFalse();
        });

        it('should return false if attribution cookie already exists', function () {
            spyOn(window.Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'hasItem')
                .withArgs('moz-consent-pref')
                .and.returnValue(false)
                .withArgs('download-as-default')
                .and.returnValue(false)
                .withArgs('moz-stub-attribution-code')
                .and.returnValue(true)
                .withArgs('moz-stub-attribution-sig')
                .and.returnValue(true);

            expect(meetsExperimentCriteria('windows')).toBeFalse();
        });

        it('should return true if all criteria are met', function () {
            spyOn(window.Mozilla.Cookies, 'enabled').and.returnValue(true);
            spyOn(window.Mozilla.Cookies, 'hasItem').and.returnValue(false);
            expect(
                meetsExperimentCriteria('windows', 'param1=test&param2=test')
            ).toBeTrue();
            expect(meetsExperimentCriteria('windows')).toBeTrue();
        });
    });
});
