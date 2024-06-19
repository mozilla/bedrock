/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import * as page from '../../../../media/js/libs/glean/page.js';
import { pageEvent } from '../../../../media/js/glean/page.es6';
import { testResetGlean } from '@mozilla/glean/testing';

describe('page.js', function () {
    beforeEach(function () {
        /**
         * note: maxEvents is set to a number greater than 1 here,
         * to circumvent a bug in Glean's test helper where `snapshot`
         * will be undefined. This can hopefully be removed in the
         * next release.
         */
        testResetGlean('moz-bedrock-test', true, { maxEvents: 100 });
    });

    it('should send an interaction event as expected', async function () {
        pageEvent({
            label: 'newsletter-signup-success',
            type: 'mozilla-and-you'
        });

        const snapshot = await page.interaction.testGetValue();
        expect(snapshot.length).toEqual(1);
        const event = snapshot[0];
        expect(event.extra.label).toEqual('newsletter-signup-success');
        expect(event.extra.type).toEqual('mozilla-and-you');
    });

    it('should send a non-interaction event as expected', async function () {
        pageEvent({
            label: 'firefox-default',
            nonInteraction: true
        });

        const snapshot = await page.nonInteraction.testGetValue();
        expect(snapshot.length).toEqual(1);
        const event = snapshot[0];
        expect(event.extra.label).toEqual('firefox-default');
        expect(event.extra.type).toEqual('');
    });
});
