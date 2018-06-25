/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: http://pivotal.github.io/jasmine/
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, beforeEach, afterEach, it, expect */

describe('whatsnew-61.js', function () {
    'use strict';

    describe('init', function () {

        it('should call showFxa if user is not logged in to FxA', function () {
            spyOn(Mozilla.WNP61, 'showFxa');

            Mozilla.WNP61.init({
                setup: false
            });

            expect(Mozilla.WNP61.showFxa).toHaveBeenCalled();
        });

        it('should call showFirefoxMobile if user is logged in to FxA but has no mobile devices set up', function () {
            spyOn(Mozilla.WNP61, 'showFirefoxMobile');

            Mozilla.WNP61.init({
                setup: true,
                mobileDevices: 0
            });

            expect(Mozilla.WNP61.showFirefoxMobile).toHaveBeenCalled();
        });

        it('should call geolocate if user is logged in to FxA and does have mobile devices set up', function () {
            spyOn(Mozilla.WNP61, 'geolocate');

            Mozilla.WNP61.init({
                setup: true,
                mobileDevices: 1
            });

            expect(Mozilla.WNP61.geolocate).toHaveBeenCalled();
        });
    });

    describe('chooseFocusOrKlar', function () {

        beforeEach(function() {
            spyOn(Mozilla.WNP61, 'showFocusOrKlar');
        });

        it('should call showFocusOrKlar with "focus" if country is not marked for Klar', function () {
            Mozilla.WNP61.chooseFocusOrKlar('pl');

            expect(Mozilla.WNP61.showFocusOrKlar).toHaveBeenCalledWith('pl', 'focus');
        });

        it('should call showFocusOrKlar with "focus" if no country code is provided', function () {
            Mozilla.WNP61.chooseFocusOrKlar();

            expect(Mozilla.WNP61.showFocusOrKlar).toHaveBeenCalledWith(undefined, 'focus');
        });

        it('should call showFocusOrKlar with "klar" if country is tagged for Klar', function () {
            Mozilla.WNP61.chooseFocusOrKlar('de');

            expect(Mozilla.WNP61.showFocusOrKlar).toHaveBeenCalledWith('de', 'klar');
        });
    });
});
