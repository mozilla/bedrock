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
import Utils from '../../../../media/js/glean/utils.es6';
import {
    recordCustomPageMetrics,
    pageEvent
} from '../../../../media/js/glean/page.es6';
import { testResetGlean } from '@mozilla/glean/testing';

describe('page.js', function () {
    beforeEach(async function () {
        /**
         * note: maxEvents is set to a number greater than 1 here,
         * to circumvent a bug in Glean's test helper where `snapshot`
         * will be undefined. This can hopefully be removed in the
         * next release.
         */
        await testResetGlean('moz-bedrock-test', true, { maxEvents: 100 });

        spyOn(Utils, 'getPathFromUrl').and.returnValue('/firefox/new/');
        spyOn(Utils, 'getLocaleFromUrl').and.returnValue('en-US');
        spyOn(Utils, 'getReferrer').and.returnValue('https://google.com/');
    });

    it('should register a page view correctly', async function () {
        recordCustomPageMetrics();

        const path = await page.path.testGetValue();
        expect(path).toEqual('/firefox/new/');

        const locale = await page.locale.testGetValue();
        expect(locale).toEqual('en-US');

        const referrer = await page.referrer.testGetValue();
        expect(referrer).toEqual('https://google.com/');

        const httpStatus = await page.httpStatus.testGetValue();
        expect(httpStatus).toEqual('200');
    });

    it('should record specific query parameters in the page view', async function () {
        const query =
            'utm_source=test-source&utm_campaign=test-campaign&utm_medium=test-medium&utm_content=test-content&entrypoint_experiment=test_entrypoint_experiment&entrypoint_variation=1&experiment=test-experiment&variation=1&v=1&xv=test-xv';
        spyOn(Utils, 'getQueryParamsFromUrl').and.returnValue(
            new window._SearchParams(query)
        );

        recordCustomPageMetrics();

        const source = await page.queryParams['utm_source'].testGetValue();
        expect(source).toEqual('test-source');

        const campaign = await page.queryParams['utm_campaign'].testGetValue();
        expect(campaign).toEqual('test-campaign');

        const medium = await page.queryParams['utm_medium'].testGetValue();
        expect(medium).toEqual('test-medium');

        const content = await page.queryParams['utm_content'].testGetValue();
        expect(content).toEqual('test-content');

        const entrypointExperiment =
            await page.queryParams['entrypoint_experiment'].testGetValue();
        expect(entrypointExperiment).toEqual('test_entrypoint_experiment');

        const entrypointVariation =
            await page.queryParams['entrypoint_variation'].testGetValue();
        expect(entrypointVariation).toEqual('1');

        const experiment = await page.queryParams['experiment'].testGetValue();
        expect(experiment).toEqual('test-experiment');

        const variation = await page.queryParams['variation'].testGetValue();
        expect(variation).toEqual('1');

        const v = await page.queryParams['v'].testGetValue();
        expect(v).toEqual('1');

        const xv = await page.queryParams['xv'].testGetValue();
        expect(xv).toEqual('test-xv');
    });

    it('should not record unspecified query params in the page view', async function () {
        const query =
            'unspecified_param=test-unspecified-param&utm_content=test-content';
        spyOn(Utils, 'getQueryParamsFromUrl').and.returnValue(
            new window._SearchParams(query)
        );

        recordCustomPageMetrics();

        const unspecifiedParam =
            await page.queryParams['unspecified_param'].testGetValue();
        expect(unspecifiedParam).toBeUndefined();

        const content = await page.queryParams['utm_content'].testGetValue();
        expect(content).toEqual('test-content');
    });

    it('should decode known params', async function () {
        const query = 'utm_source=%25&utm_campaign=%2F';
        spyOn(Utils, 'getQueryParamsFromUrl').and.returnValue(
            new window._SearchParams(query)
        );

        recordCustomPageMetrics();

        const source = await page.queryParams['utm_source'].testGetValue();
        expect(source).toEqual('%');

        const campaign = await page.queryParams['utm_campaign'].testGetValue();
        expect(campaign).toEqual('/');
    });

    it('should not record known params that contain bad values', async function () {
        const query =
            'utm_source=<script>yikes</script>&utm_campaign=%5Ctest&utm_medium=%3Ctest&utm_content=test-content&experiment';
        spyOn(Utils, 'getQueryParamsFromUrl').and.returnValue(
            new window._SearchParams(query)
        );

        recordCustomPageMetrics();

        const source = await page.queryParams['utm_source'].testGetValue();
        expect(source).toEqual('');

        const campaign = await page.queryParams['utm_campaign'].testGetValue();
        expect(campaign).toEqual('');

        const medium = await page.queryParams['utm_medium'].testGetValue();
        expect(medium).toEqual('');

        const content = await page.queryParams['utm_content'].testGetValue();
        expect(content).toEqual('test-content');

        const experiment = await page.queryParams['experiment'].testGetValue();
        expect(experiment).toEqual('');
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
