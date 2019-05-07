/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.

 Portions based on http://blog.gospodarets.com/native_smooth_scrolling/
*/

if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

Mozilla.smoothScroll = (function() {
    'use strict';

    var _smoothScroll;
    var $htmlBody;

    var _init = function(unitTest) {
        var hasSmoothScroll;

        // try to use native smooth scrolling
        if (unitTest) {
            hasSmoothScroll = (unitTest === 'native') ? true : false;
        } else {
            hasSmoothScroll = 'scrollBehavior' in document.documentElement.style;
        }

        // use native smooth scrolling
        if (hasSmoothScroll) {
            _smoothScroll = function(opts) {
                window.scrollTo(opts);
            };
        // otherwise, use jQuery if it's available
        } else if (window.jQuery) {
            $htmlBody = $('html, body');

            _smoothScroll = function(opts) {
                $htmlBody.animate({
                    scrollTop: opts.top,
                    scrollLeft: opts.left
                }, 400);
            };
        // default to regular ol' jump scrolling
        } else {
            _smoothScroll = function(opts) {
                window.scrollTo(opts.top, opts.left);
            };
        }
    };

    /*
    userOpts: object of params (required):
        behavior: type of scrolling. (default: 'smooth')
        top: number of pixels from the top to scroll. (default: 0)
        left: number of pixels from the left to scroll. (default: 0)

    At least one of the two axes (top, left) should be specified.
    */
    return function(userOpts) {
        // set up defaults
        var opts = {
            behavior: userOpts.behavior || 'smooth',
            top: userOpts.top || 0,
            left: userOpts.left || 0
        };

        // lazy load behavior detection
        if (typeof _smoothScroll !== 'function' || userOpts.unitTest) {
            _init(userOpts.unitTest);
        }

        _smoothScroll(opts);
    };
})();
