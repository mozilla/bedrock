/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import FirefoxDefault from '../../../../../media/js/base/fx-is-default.es6.js';

describe('fx-is-default.js', function () {
    beforeEach(function () {
        window.Mozilla.UITour = sinon.stub();
        window.Mozilla.UITour.ping = sinon.stub();
        window.Mozilla.UITour.getConfiguration = sinon.stub();
        document.body.append(document.createElement('main'));

        spyOn(window.Mozilla.UITour, 'ping').and.callFake((callback) => {
            callback();
        });
    });

    afterEach(function () {
        document.querySelector('main').remove();
    });

    describe('when desktop Firefox is default', function () {
        it('should add class', function () {
            spyOn(FirefoxDefault, 'isSupported').and.returnValue(true);

            spyOn(window.Mozilla.UITour, 'getConfiguration').and.callFake(
                (id, callback) => {
                    callback({
                        defaultBrowser: true
                    });
                }
            );

            return FirefoxDefault.init('main').then(() => {
                expect(document.querySelector('main').classList).toContain(
                    'is-firefox-default'
                );
            });
        });
    });

    describe('when desktop Firefox is not default', function () {
        it('should not add class', async function () {
            spyOn(FirefoxDefault, 'isSupported').and.returnValue(true);

            spyOn(window.Mozilla.UITour, 'getConfiguration').and.callFake(
                (id, callback) => {
                    callback({
                        defaultBrowser: false
                    });
                }
            );

            return FirefoxDefault.init('main').then(() => {
                expect(document.querySelector('main').classList).not.toContain(
                    'is-firefox-default'
                );
            });
        });
    });

    describe('when not desktop Firefox', function () {
        it('should not call UITour to check default browser', async function () {
            spyOn(FirefoxDefault, 'isSupported').and.returnValue(false);

            spyOn(window.Mozilla.UITour, 'getConfiguration');

            expect(
                window.Mozilla.UITour.getConfiguration
            ).not.toHaveBeenCalled();
        });
    });
});
