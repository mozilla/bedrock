/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect */

describe('whatsnew-62.js', function () {
    'use strict';

    describe('init', function () {

        afterEach(function() {
            Mozilla.WNP62.locale = null;
        });

        it('should call showPocket if user is not logged in to FxA and lang is en', function () {
            Mozilla.WNP62.locale = 'en';
            spyOn(Mozilla.WNP62, 'showPocket');

            Mozilla.WNP62.init({
                setup: false
            });

            expect(Mozilla.WNP62.showPocket).toHaveBeenCalled();
        });

        it('should call showFxa if user is not logged in to FxA and lang is *not* en', function () {
            Mozilla.WNP62.locale = 'fr';
            spyOn(Mozilla.WNP62, 'showFxa');

            Mozilla.WNP62.init({
                setup: false
            });

            expect(Mozilla.WNP62.showFxa).toHaveBeenCalled();
        });

        it('should call showFirefoxMobile if user is logged in to FxA but has no mobile devices set up', function () {
            spyOn(Mozilla.WNP62, 'showFirefoxMobile');

            Mozilla.WNP62.init({
                setup: true,
                mobileDevices: 0
            });

            expect(Mozilla.WNP62.showFirefoxMobile).toHaveBeenCalled();
        });

        it('should call geolocate if user is logged in to FxA and does have mobile devices set up', function () {
            spyOn(Mozilla.WNP62, 'geolocate');

            Mozilla.WNP62.init({
                setup: true,
                mobileDevices: 1
            });

            expect(Mozilla.WNP62.geolocate).toHaveBeenCalled();
        });
    });

    describe('chooseFocusOrKlar', function () {

        beforeEach(function() {
            spyOn(Mozilla.WNP62, 'showFocusOrKlar');
        });

        it('should call showFocusOrKlar with "focus" if country is not marked for Klar', function () {
            Mozilla.WNP62.chooseFocusOrKlar('pl');

            expect(Mozilla.WNP62.showFocusOrKlar).toHaveBeenCalledWith('pl', 'focus');
        });

        it('should call showFocusOrKlar with "focus" if no country code is provided', function () {
            Mozilla.WNP62.chooseFocusOrKlar();

            expect(Mozilla.WNP62.showFocusOrKlar).toHaveBeenCalledWith(undefined, 'focus');
        });

        it('should call showFocusOrKlar with "klar" if country is tagged for Klar', function () {
            Mozilla.WNP62.chooseFocusOrKlar('de');

            expect(Mozilla.WNP62.showFocusOrKlar).toHaveBeenCalledWith('de', 'klar');
        });
    });
});
