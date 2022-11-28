/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

/* For reference read the Jasmine and Sinon docs
 * Jasmine docs: https://jasmine.github.io/2.0/introduction.html
 * Sinon docs: http://sinonjs.org/docs/
 */

describe('mozilla-pixel.js', function () {
    afterEach(function () {
        window.Mozilla.dntEnabled = sinon.stub();

        document.querySelectorAll('.moz-px').forEach((e) => {
            e.parentNode.removeChild(e);
        });
    });

    describe('init', function () {
        it('should not add pixel img if "do not track" is enabled', function () {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(true);
            spyOn(Mozilla.Pixel, 'setPixels');
            Mozilla.Pixel.init();
            expect(Mozilla.Pixel.setPixels).not.toHaveBeenCalled();
        });

        it('should add multiple pixels to document body', function () {
            const pixels = '/img/foo.png::/img/foo.png?v=1::/img/foo.png?v=2';
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Pixel, 'getPixelData').and.returnValue(pixels);
            Mozilla.Pixel.init();
            expect(document.querySelectorAll('.moz-px').length).toEqual(3);
        });

        it('should add one pixel to document body', function () {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Pixel, 'getPixelData').and.returnValue(
                '/img/foo.png'
            );
            Mozilla.Pixel.init();
            expect(document.querySelectorAll('.moz-px').length).toEqual(1);
        });

        it('should not add pixel if data is undefined', function () {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Pixel, 'getPixelData').and.returnValue(undefined);
            Mozilla.Pixel.init();
            expect(document.querySelectorAll('.moz-px').length).toEqual(0);
        });

        it('should not add pixel if data is empty', function () {
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Pixel, 'getPixelData').and.returnValue('');
            Mozilla.Pixel.init();
            expect(document.querySelectorAll('.moz-px').length).toEqual(0);
        });

        it('should cache bust doubleclick request', function () {
            // this is a bit of a hack to avoid making real requests to ad.doubleclick.net in test runs.
            const pixels = '/img/foo.png?ad.doubleclick.net/src=6417015';
            Math.random = sinon.stub().returns(0.853456456);
            spyOn(Mozilla, 'dntEnabled').and.returnValue(false);
            spyOn(Mozilla.Pixel, 'getPixelData').and.returnValue(pixels);
            Mozilla.Pixel.init();

            expect(document.querySelector('.moz-px').src).toContain(
                ';num=8534564560000'
            );
        });
    });
});
