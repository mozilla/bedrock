/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

/* global describe, afterEach, it, expect */

describe('mozilla-pixel.js', function() {

    'use strict';

    afterEach(function() {
        $('.moz-px').remove();
    });

    describe('init', function() {

        it('should not add pixel img if "do not track" is enabled', function() {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(true);
            spyOn(Mozilla.Pixel, 'setPixels');
            Mozilla.Pixel.init();
            expect(Mozilla.Pixel.setPixels).not.toHaveBeenCalled();
        });

        it('should add multiple pixels to document body', function() {
            var pixels = '/img/foo.png::/img/foo.png?v=1::/img/foo.png?v=2';
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Pixel, 'getPixelData').and.returnValue(pixels);
            Mozilla.Pixel.init();
            expect($('.moz-px').length).toEqual(3);
        });

        it('should add one pixel to document body', function() {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Pixel, 'getPixelData').and.returnValue('/img/foo.png');
            Mozilla.Pixel.init();
            expect($('.moz-px').length).toEqual(1);
        });

        it('should not add pixel if data is undefined', function() {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Pixel, 'getPixelData').and.returnValue(undefined);
            Mozilla.Pixel.init();
            expect($('.moz-px').length).toEqual(0);
        });

        it('should not add pixel if data is empty', function() {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Pixel, 'getPixelData').and.returnValue('');
            Mozilla.Pixel.init();
            expect($('.moz-px').length).toEqual(0);
        });
    });
});
