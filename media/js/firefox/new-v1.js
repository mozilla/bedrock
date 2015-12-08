/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($) {
    'use strict';

    var $html = $(document.documentElement);
    var isIELT9 = (site.platform === 'windows' && /MSIE\s[1-8]\./.test(navigator.userAgent));

    var queryWideViewport;

    var loadFonts = function(mq) {
        if (mq.matches) {
            var fntOpenSans = new FontFaceObserver('Open Sans', {
                weight: 'normal'
            });
            var fntOpenSansBold = new FontFaceObserver('Open Sans', {
                weight: 'bold'
            });
            var fntOpenSansLight = new FontFaceObserver('Open Sans Light');

            Promise.all([fntOpenSans.check(), fntOpenSansLight.check()]).then(function() {
                $html.addClass('fonts'); // use fonts
                queryWideViewport.removeListener(loadFonts); // stop listening
            }, function() {
                // couldn't load fonts, but that's okay because content is
                // still readable
            });
        }
    };

    // if IE9+ with matchMedia supported, conditionally load fonts
    if (!isIELT9 && typeof matchMedia !== 'undefined') {
        queryWideViewport = matchMedia('(min-width: 760px)');

        queryWideViewport.addListener(loadFonts);

        if (queryWideViewport.matches) {
            loadFonts(queryWideViewport);
        }
    }
})(window.jQuery);
