/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
;(function(w, $, enquire, Modernizr) {
    'use strict';

    // tablet is good enough for full experience?
    enquire.register("screen and (min-width: 760px)", {
        deferSetup: true, // don't run setup until mq matches
        setup: function() {
            Modernizr.load([{
                both: [ '/media/js/libs/jquery.pageslide.min.js', '/media/js/libs/tweenmax.min.js', '/media/js/libs/superscrollorama.js', '/media/js/libs/jquery.spritely-0.6.1.js', '/media/js/firefox/partners/desktop.js' ],
                complete: function() {
                    // no action needed?
                }
            }]);
        },
        match: function() {
            // no action needed, but handler must be present
        },
        unmatch: function() {
            // no action needed?
            // currently no way of unbinding superscrollorama stuff (wut!?)
            // however, only desktop users should ever go from desktop to mobile, so...it's ok? maybe?
        }
    }, true).listen(); // true param here forces non-mq browsers to match this rule
    // so, i don't think we need a polyfill
})(window, window.jQuery, window.enquire, window.Modernizr);
