/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import TrackScroll from '../../../../media/js/base/datalayer-trackscroll.es6.js';

describe('datalayer-trackscroll.es6.js', function () {
    const scrollHeight = 1000;
    const innerHeight = 200;
    const scroll25 = 200;
    const scroll50 = 400;
    const scroll75 = 600;
    const scroll90 = 720;

    beforeEach(function () {
        window.dataLayer = [];
    });

    afterEach(function () {
        delete window.dataLayer;
    });

    it('calculates scroll depth correctly', function () {
        const depth25 = TrackScroll.getDepth(
            scrollHeight,
            innerHeight,
            scroll25
        );
        expect(depth25 === 25).toBeTruthy();
        const depth50 = TrackScroll.getDepth(
            scrollHeight,
            innerHeight,
            scroll50
        );
        expect(depth50 === 50).toBeTruthy();
        const depth75 = TrackScroll.getDepth(
            scrollHeight,
            innerHeight,
            scroll75
        );
        expect(depth75 === 75).toBeTruthy();
        const depth90 = TrackScroll.getDepth(
            scrollHeight,
            innerHeight,
            scroll90
        );
        expect(depth90 === 90).toBeTruthy();
    });

    it('correctly identifies when multiple scroll thresholds have been passed', function () {
        spyOn(TrackScroll, 'getDepth').and.returnValue(80);
        TrackScroll.scrollHandler();
        expect(window.dataLayer[0]['percent_scrolled'] === '25').toBeTruthy();
        expect(window.dataLayer[1]['percent_scrolled'] === '50').toBeTruthy();
        expect(window.dataLayer[2]['percent_scrolled'] === '75').toBeTruthy();
        expect(window.dataLayer[4]).toBeFalsy();
    });

    it('will append the scroll event to the dataLayer', function () {
        TrackScroll.sendEvent('50');
        expect(window.dataLayer[0]['event'] === 'scroll').toBeTruthy();
        expect(window.dataLayer[0]['percent_scrolled'] === '50').toBeTruthy();
    });
});
