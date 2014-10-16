/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    //Only run the tour if user is on Firefox 33 for desktop.
    if (window.isFirefox() && !window.isFirefoxMobile() && window.getFirefoxMasterVersion() >= 33) {

        // Query if the UITour API is working before we start the tour
        Mozilla.UITour.getConfiguration('sync', function (config) {

            var tour = new Mozilla.BrowserTour({
                id: $('#tour-page').data('telemetry')
            });

            tour.init();
        });
    }

})(window.jQuery, window.Mozilla);
