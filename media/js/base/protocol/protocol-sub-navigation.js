/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // check we have global variable
    if (typeof window.Mzp !== 'undefined') {
        var Mzp = window.Mzp;
        var subNavTitle = '.c-sub-navigation .c-sub-navigation-title';

        // check we have global Supports and Details library
        if (typeof Mzp.Supports !== 'undefined' && typeof Mzp.Details !== 'undefined') {

            // check browser supports matchMedia
            if(Mzp.Supports.matchMedia) {
                var _mqWide = matchMedia('(max-width: 768px');

                // initialize details if screen is small
                if (_mqWide.matches) {
                    Mzp.Details.init(subNavTitle);
                }

                // remove details if screen is big
                _mqWide.addListener(function(mq) {
                    if (mq.matches) {
                        Mzp.Details.init(subNavTitle);
                    } else {
                        Mzp.Details.destroy(subNavTitle);
                    }
                });
            }
        }
    }
})();
