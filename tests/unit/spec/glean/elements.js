/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/
 * Sinon docs: http://sinonjs.org/docs/
 */

import { testResetGlean } from '@mozilla/glean/testing';
import { clickPing } from '../../../../media/js/glean/elements.es6';
import * as element from '../../../../media/js/libs/glean/element.js';
import { interaction as interactionPing } from '../../../../media/js/libs/glean/pings.js';

describe('elements.js', function () {
    beforeEach(async function () {
        await testResetGlean('moz-bedrock-test');
    });

    describe('clickPing', function () {
        it('should send an interaction ping when clickPing is called', async function () {
            const ping = interactionPing.testBeforeNextSubmit(
                async function () {
                    const snapshot = await element.clicked.testGetValue();
                    expect(snapshot.length).toEqual(1);
                    const click = snapshot[0];
                    expect(click.extra.label).toEqual('Firefox Download');
                    expect(click.extra.type).toEqual('macOS, release, en-US');
                    expect(click.extra.position).toEqual('primary');
                }
            );

            clickPing({
                label: 'Firefox Download',
                type: 'macOS, release, en-US',
                position: 'primary'
            });

            // Wait for the validation to finish.
            await expectAsync(ping).toBeResolved();
        });
    });
});
