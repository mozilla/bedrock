/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    var subNavTitle =
        '.t-firefox-family .c-sub-navigation .c-sub-navigation-title';

    function handleMqChange(mq) {
        if (mq.matches) {
            window.MzpDetails.init(subNavTitle);
        } else {
            window.MzpDetails.destroy(subNavTitle);
        }
    }

    // check we have global Supports and Details library
    if (
        typeof window.MzpSupports !== 'undefined' &&
        typeof window.MzpDetails !== 'undefined'
    ) {
        // check browser supports matchMedia
        if (window.MzpSupports.matchMedia) {
            var _mqWide = matchMedia('(max-width: 1060px)');

            // initialize details if screen is small
            if (_mqWide.matches) {
                window.MzpDetails.init(subNavTitle);
            }

            if (window.matchMedia('all').addEventListener) {
                // evergreen
                _mqWide.addEventListener('change', handleMqChange, false);
            } else if (window.matchMedia('all').addListener) {
                // IE fallback
                _mqWide.addListener(handleMqChange);
            }
        }
    }
})();
