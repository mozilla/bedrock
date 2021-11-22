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
import {
    bindElementClicks,
    unbindElementClicks
} from '../../../../media/js/glean/elements.es6';
import * as element from '../../../../media/js/libs/glean/element.js';
import { interaction as interactionPing } from '../../../../media/js/libs/glean/pings.js';

describe('elements.js', function () {
    beforeEach(async function () {
        await testResetGlean('moz-bedrock-test');
        bindElementClicks();
    });

    afterEach(function () {
        unbindElementClicks();
    });

    describe('Element Click (data-cta)', function () {
        beforeEach(async function () {
            const link =
                '<button type="button" class="mzp-c-button glean-test-element" data-cta-text="Subscribe" data-cta-type="button" data-cta-position="primary">Subscribe</button>';
            document.body.insertAdjacentHTML('beforeend', link);
        });

        afterEach(function () {
            document
                .querySelectorAll('.glean-test-element')
                .forEach(function (e) {
                    e.parentNode.removeChild(e);
                });
        });

        it('should send an interaction ping when element is clicked containing data-cta attributes', async function () {
            let validatorRun = false;
            const ping = interactionPing.testBeforeNextSubmit(
                async function () {
                    const snapshot = await element.clicked.testGetValue();
                    expect(snapshot.length).toEqual(1);
                    const click = snapshot[0];
                    expect(click.extra.label).toEqual('Subscribe');
                    expect(click.extra.type).toEqual('button');
                    expect(click.extra.position).toEqual('primary');
                    validatorRun = true;
                }
            );

            document.querySelector('.glean-test-element').click();

            // Wait for the validation to finish.
            await ping;

            expect(validatorRun).toBeTrue();
        });
    });

    describe('Element Click (data-link)', function () {
        beforeEach(async function () {
            const link =
                '<button type="button" class="mzp-c-button glean-test-element" data-link-name="Submit" data-link-type="button" data-link-position="primary">Submit</button>';
            document.body.insertAdjacentHTML('beforeend', link);
        });

        afterEach(function () {
            document
                .querySelectorAll('.glean-test-element')
                .forEach(function (e) {
                    e.parentNode.removeChild(e);
                });
        });

        it('should send an interaction ping when element is clicked containing data-link attributes', async function () {
            let validatorRun = false;
            const ping = interactionPing.testBeforeNextSubmit(
                async function () {
                    const snapshot = await element.clicked.testGetValue();
                    expect(snapshot.length).toEqual(1);
                    const click = snapshot[0];
                    expect(click.extra.label).toEqual('Submit');
                    expect(click.extra.type).toEqual('button');
                    expect(click.extra.position).toEqual('primary');
                    validatorRun = true;
                }
            );

            document.querySelector('.glean-test-element').click();

            // Wait for the validation to finish.
            await ping;

            expect(validatorRun).toBeTrue();
        });
    });

    describe('Firefox Download Click', function () {
        beforeEach(async function () {
            const link =
                '<button type="button" class="mzp-c-button glean-test-element" data-link-type="download" data-download-os="Desktop" data-display-name="macOS" data-download-version="osx" data-download-location="primary">Submit</button>';
            document.body.insertAdjacentHTML('beforeend', link);
        });

        afterEach(function () {
            document
                .querySelectorAll('.glean-test-element')
                .forEach(function (e) {
                    e.parentNode.removeChild(e);
                });
        });

        it('should send an interaction ping when element is clicked containing data-link attributes', async function () {
            let validatorRun = false;
            const ping = interactionPing.testBeforeNextSubmit(
                async function () {
                    const snapshot = await element.clicked.testGetValue();
                    expect(snapshot.length).toEqual(1);
                    const click = snapshot[0];
                    expect(click.extra.label).toEqual(
                        'Firefox Download Desktop'
                    );
                    expect(click.extra.type).toEqual('macOS');
                    expect(click.extra.position).toEqual('primary');
                    validatorRun = true;
                }
            );

            document.querySelector('.glean-test-element').click();

            // Wait for the validation to finish.
            await ping;

            expect(validatorRun).toBeTrue();
        });
    });

    describe('Nested element click (data-cta)', function () {
        beforeEach(async function () {
            const link = `<button type="button" class="mzp-c-button glean-test-element" data-cta-text="Subscribe" data-cta-type="button" data-cta-position="primary">
                    <span class="child-element">Subscribe</span>
                </button>`;
            document.body.insertAdjacentHTML('beforeend', link);
        });

        afterEach(function () {
            document
                .querySelectorAll('.glean-test-element')
                .forEach(function (e) {
                    e.parentNode.removeChild(e);
                });
        });

        it('should send an interaction ping for a parent element when element a child element is clicked', async function () {
            let validatorRun = false;
            const ping = interactionPing.testBeforeNextSubmit(
                async function () {
                    const snapshot = await element.clicked.testGetValue();
                    expect(snapshot.length).toEqual(1);
                    const click = snapshot[0];
                    expect(click.extra.label).toEqual('Subscribe');
                    expect(click.extra.type).toEqual('button');
                    expect(click.extra.position).toEqual('primary');
                    validatorRun = true;
                }
            );

            document
                .querySelector('.glean-test-element > .child-element')
                .click();

            // Wait for the validation to finish.
            await ping;

            expect(validatorRun).toBeTrue();
        });
    });
});
