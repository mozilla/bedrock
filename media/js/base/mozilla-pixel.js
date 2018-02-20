/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
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
        return $('#strings').data('pixels');
    };

    Pixel.setPixels = function() {
        var $body = $('body');
        var pixels = Pixel.getPixelData();
        var $pixel;

        if (typeof pixels !== 'string' || pixels === '') {
            return;
        }

        // '::' is a separator for each pixel URL.
        pixels = pixels.split('::');

        for (var i = 0; i < pixels.length; i++) {
            $pixel = $('<img />', {
                width: '1',
                height: '1',
                src: pixels[i].replace(/\s/g, '')
            });
            $pixel.addClass('moz-px');
            $body.append($pixel);
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
