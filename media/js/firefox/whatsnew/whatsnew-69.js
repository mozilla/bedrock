/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    // Issue #7671 measure potential UITour failure for bug 1557153
    function pingUITour() {
        var startTime = performance.now();
        var timeout = window.setTimeout(trackImpression, 1000, 'UITour Timeout');

        Mozilla.UITour.ping(function() {
            window.clearTimeout(timeout);
            trackImpression('UITour Response');
        });

        function trackImpression(eLabel) {
            var endTime = performance.now() - startTime;

            window.dataLayer.push({
                'eLabel': eLabel,
                'data-response-time': endTime,
                'event': 'non-interaction'
            });
        }
    }

    // Prevent double-requesting Flow IDs. Inits signed out button even on non-firefox browsers (highly unlikely on this page, but you never know).
    if (Mozilla.Client.isFirefoxDesktop) {
        Mozilla.Client.getFxaDetails(function(details) {
            if (details.setup) {
                Mozilla.MonitorButton.init('monitor-button-signed-in');
            } else {
                Mozilla.MonitorButton.init('monitor-button-signed-out');
            }
        });
    } else {
        Mozilla.MonitorButton.init('monitor-button-signed-out');
    }

    pingUITour();
})();
