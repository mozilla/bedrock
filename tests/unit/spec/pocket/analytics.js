/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('analytics.es6.js', function () {
    beforeEach(function () {
        window.OptanonActiveGroups = sinon.stub();
        window.snowplow = sinon.stub();
    });

    describe('OptanonWrapper', function () {
        beforeEach(function () {
            window.OptanonActiveGroups = null;
            window.PocketAnalytics.loaded = false;

            spyOn(window.PocketAnalytics, 'loadSnowPlow');
            spyOn(window.PocketAnalytics, 'loadGA');
            spyOn(window.PocketAnalytics, 'reloadPage');
            spyOn(window, 'snowplow');
        });

        it('should load both GA and Snowplow when cookie consent is given', function () {
            window.OptanonActiveGroups = 'C0001,C0002';
            window.OptanonWrapper();
            expect(window.PocketAnalytics.loadSnowPlow).toHaveBeenCalledWith({
                eventMethod: 'beacon',
                stateStorageStrategy: 'cookieAndLocalStorage',
                anonymousTracking: false
            });
            expect(window.PocketAnalytics.loadGA).toHaveBeenCalled();
            expect(window.PocketAnalytics.loaded).toBeTrue();
            expect(window.PocketAnalytics.reloadPage).not.toHaveBeenCalled();
        });

        it('should not load GA when cookie consent is not given', function () {
            window.OptanonActiveGroups = 'C0001';
            window.OptanonWrapper();
            expect(window.PocketAnalytics.loadGA).not.toHaveBeenCalled();
            expect(window.PocketAnalytics.loaded).toBeTrue();
            expect(window.PocketAnalytics.reloadPage).not.toHaveBeenCalled();
        });

        it('should load Snowplow in privacy mode when cookie consent is not given', function () {
            window.OptanonActiveGroups = 'C0001';
            window.OptanonWrapper();
            expect(window.PocketAnalytics.loadSnowPlow).toHaveBeenCalledWith({
                eventMethod: 'post',
                stateStorageStrategy: 'none',
                anonymousTracking: {
                    withServerAnonymisation: true
                }
            });
            expect(window.PocketAnalytics.loaded).toBeTrue();
            expect(window.PocketAnalytics.reloadPage).not.toHaveBeenCalled();
        });

        it('should not load analytics scripts twice', function () {
            window.OptanonActiveGroups = 'C0001,C0002';
            window.OptanonWrapper();
            expect(window.PocketAnalytics.loaded).toBeTrue();
            window.OptanonWrapper();
            expect(window.PocketAnalytics.loadSnowPlow).toHaveBeenCalledTimes(
                1
            );
            expect(window.PocketAnalytics.loadGA).toHaveBeenCalledTimes(1);
            expect(window.PocketAnalytics.reloadPage).not.toHaveBeenCalled();
        });

        it('should clear snowplow user data and reload the page if consent is withdrawn', function () {
            window.OptanonActiveGroups = 'C0001,C0002';
            window.OptanonWrapper();
            expect(window.PocketAnalytics.loadSnowPlow).toHaveBeenCalled();
            expect(window.PocketAnalytics.loadGA).toHaveBeenCalled();
            expect(window.PocketAnalytics.loaded).toBeTrue();

            window.OptanonActiveGroups = 'C0001';
            window.OptanonWrapper();

            expect(window.snowplow).toHaveBeenCalledWith(
                'clearUserData',
                true,
                true
            );
            expect(window.PocketAnalytics.reloadPage).toHaveBeenCalledTimes(1);
        });
    });
});
