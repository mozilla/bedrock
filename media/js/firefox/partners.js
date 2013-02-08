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
            // TODO: attach desktop hooks
        },
        unmatch: function() {
            // TODO: detach desktop hooks

            // currently no way of unbinding superscrollorama stuff (wut!?)
            // however, only desktop users should ever go from desktop to mobile, so...it's ok?
        }
    // true param here forces non-mq browsers to match this rule, so, i don't think we need a polyfill
    }, true).register("screen and (max-width: 759px)", {
        deferSetup: true,
        setup: function() {
            Modernizr.load([{
                both: [ '/media/js/firefox/partners/mobile.js' ],
                complete: function() {
                    w.attach_mobile();
                }
            }]);
        },
        match: function() {
            // handler must exist
        },
        unmatch: function() {
            w.detach_mobile();
        }
    }, false).listen();
})(window, window.jQuery, window.enquire, window.Modernizr);
