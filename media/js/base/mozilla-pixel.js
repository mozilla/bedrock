/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function() {
    'use strict';

    /**
     * Tracking pixels for /firefox/download/thanks/ download page.
     * For more info see websites privacy notice and bugs:
     * https://www.mozilla.org/privacy/websites/
     * Yahoo: bug 1343033.
     * Double Click: bug 1331069.
     * Pixel switch status: bug 1311423.
     */
    var Pixel = {};

    Pixel.getPixelData = function() {
        return document.getElementById('strings').getAttribute('data-pixels');
    };

    Pixel.setPixels = function() {
        var body = document.querySelector('body');
        var pixels = Pixel.getPixelData();
        var pixel;

        if (typeof pixels !== 'string' || pixels === '') {
            return;
        }

        // '::' is a separator for each pixel URL.
        pixels = pixels.split('::');

        for (var i = 0; i < pixels.length; i++) {
            pixel = document.createElement('img');
            pixel.width = 1;
            pixel.height = 1;
            pixel.src = pixels[i].replace(/\s/g, '');

            // Cache bust doubleclick pixel (see issue 9128)
            if (pixels[i].indexOf('ad.doubleclick.net') !== -1) {
                var num = Math.random() + '' * 10000000000000;
                pixel.src += ';num=' + num;
            }

            pixel.className = 'moz-px';
            body.appendChild(pixel);
        }
    };

    Pixel.init = function() {
        // Do not set pixels if visitor has DNT enabled.
        if (!Mozilla.dntEnabled()) {
            Pixel.setPixels();
        }
    };

    window.Mozilla.Pixel = Pixel;
})();
