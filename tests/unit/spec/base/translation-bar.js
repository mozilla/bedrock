/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

/* eslint new-cap: [2, {"capIsNewExceptions": ["Deferred"]}] */
import translationBar from '../../../../media/js/base/translation-bar.es6.js';

describe('translation-bar.js', function () {
    describe('normalize', function () {
        it('should normalize en-us to en-US', function () {
            expect(translationBar.normalize('en-us')).toBe('en-US');
        });
        it('should normalize DE to de', function () {
            expect(translationBar.normalize('DE')).toBe('de');
        });
    });
    describe('isLangMatch', function () {
        it('should match en-US to itself', function () {
            expect(translationBar.isLangMatch('en-US', 'en-US')).toBe(true);
        });
        it('should match es to es-ES', function () {
            expect(translationBar.isLangMatch('es', 'es-ES')).toBe(true);
        });
        it('should match en-CA to en-US', function () {
            expect(translationBar.isLangMatch('en-CA', 'en-US')).toBe(true);
        });
        it('should match de-XX to de', function () {
            expect(translationBar.isLangMatch('de-XX', 'de')).toBe(true);
        });
        it('should match en to en-CA', function () {
            // This will match short code to first sorted locale.
            expect(translationBar.isLangMatch('en', 'en-CA')).toBe(true);
        });
        it('should not match en to de', function () {
            expect(translationBar.isLangMatch('en', 'de')).toBe(false);
        });
    });
    // translationBar.getBestMatch = function (acceptLangs, availableLangs) {
    describe('getBestMatch', function () {
        const available = [
            'de',
            'en-CA',
            'en-GB',
            'en-US',
            'es-AR',
            'es-ES',
            'fr',
            'it',
            'ja',
            'pt-BR',
            'pt-PT',
            'zh-CN',
            'zh-TW'
        ];
        it('should return the correct mapping from short locales to full locales', function () {
            expect(translationBar.getBestMatch(['en'], available)).toBe(
                'en-US'
            );
            expect(translationBar.getBestMatch(['en-US'], available)).toBe(
                'en-US'
            );
            expect(translationBar.getBestMatch(['en-CA'], available)).toBe(
                'en-CA'
            );
            expect(translationBar.getBestMatch(['es'], available)).toBe(
                'es-ES'
            );
            expect(translationBar.getBestMatch(['es-MX'], available)).toBe(
                'es-ES'
            );
            expect(translationBar.getBestMatch(['ja-jp-mac'], available)).toBe(
                'ja'
            );
            expect(translationBar.getBestMatch(['pt'], available)).toBe(
                'pt-BR'
            );
            expect(translationBar.getBestMatch(['zh-hant'], available)).toBe(
                'zh-TW'
            );
        });
    });
});
