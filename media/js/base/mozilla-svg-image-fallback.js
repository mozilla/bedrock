/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

Mozilla.SVGImage = {};

Mozilla.SVGImage.isSupported = function() {
    'use strict';
    return document.implementation.hasFeature('http://www.w3.org/TR/SVG11/feature#Image', '1.1');
};

// fallback to .png for browsers that don't support .svg as an image.
Mozilla.SVGImage.fallback = function() {
    'use strict';
    if (!Mozilla.SVGImage.isSupported()) {
        $('img[src*="svg"][data-fallback="true"]').attr('src', function() {
            return $(this).data('png');
        });
    }
};
