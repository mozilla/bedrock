/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import TrackBeginCheckout from '../../../../media/js/base/datalayer-begincheckout.es6.js';

describe('datalayer-begincheckout.es6.js', function () {
    const expectedObj = {
        event: 'begin_checkout',
        currency: 'USD',
        value: '11.88',
        items: [
            {
                item_id: 'testid',
                item_name: 'email',
                item_category: 'relay',
                item_variant: 'yearly',
                price: '11.88',
                discount: '12.00'
            }
        ]
    };

    describe('TrackBeginCheckout.getEventObject', function () {
        // for begin_checkout docs see https://developers.google.com/analytics/devguides/collection/ga4/reference/events?client_type=gtag#begin_checkout
        it('will return an object formatted as a Google Analytics begin_checkout recommended event', function () {
            const returnObj = TrackBeginCheckout.getEventObject(
                'testid',
                'relay',
                'email',
                'yearly',
                '11.88',
                'USD',
                '12.00'
            );

            expect(returnObj === expectedObj);
        });
    });

    describe('TrackBeginCheckout.getEventObjectAndSend', function () {
        beforeEach(function () {
            // watch
            spyOn(TrackBeginCheckout, 'sendEvent');
        });
        it('will pass the object to sendEvent', function () {
            TrackBeginCheckout.getEventObjectAndSend(
                'testid',
                'relay',
                'email',
                'yearly',
                '11.88',
                'USD',
                '12.00'
            );

            expect(TrackBeginCheckout.sendEvent).toHaveBeenCalledWith(
                expectedObj
            );
        });
    });

    describe('TrackBeginCheckout.sendEvent', function () {
        beforeEach(function () {
            window.dataLayer = [];
        });

        afterEach(function () {
            delete window.dataLayer;
        });

        it('will append the begin_checkout event to the dataLayer', function () {
            TrackBeginCheckout.sendEvent(expectedObj);
            expect(
                window.dataLayer[0]['event'] === 'begin_checkout'
            ).toBeTruthy();
        });
    });
});
