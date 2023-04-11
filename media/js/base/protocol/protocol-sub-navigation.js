/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

(function () {
    'use strict';

    var subNavTitle = '.c-sub-navigation .c-sub-navigation-title';

    // check we have global Supports and Details library
    if (
        typeof window.MzpSupports !== 'undefined' &&
        typeof window.MzpDetails !== 'undefined'
    ) {
        // check browser supports matchMedia
        if (window.MzpSupports.matchMedia) {
            var _mqWide = matchMedia('(max-width: 767px)');

            // initialize details if screen is small
            if (_mqWide.matches) {
                window.MzpDetails.init(subNavTitle);
            }

            // remove details if screen is big
            _mqWide.addListener(function (mq) {
                if (mq.matches) {
                    window.MzpDetails.init(subNavTitle);
                } else {
                    window.MzpDetails.destroy(subNavTitle);
                }
            });
        }
    }
})();
