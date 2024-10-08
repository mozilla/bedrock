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
    beforeEach(function () {
        window.dataLayer = [];
    });

    afterEach(function () {
        delete window.dataLayer;
    });

    it('will append the scroll event to the dataLayer', function () {
        TrackScroll.sendEvent('50');
        expect(window.dataLayer[0]['event'] === 'scroll').toBeTruthy();
        expect(window.dataLayer[0]['percent_scrolled'] === '50').toBeTruthy();
    });
});
