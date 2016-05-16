/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, dataLayer) {
    'use strict';

    var $html = $(document.documentElement);
    var client = window.Mozilla.Client;
    var state; // track page state

    var uiTourSendEvent = function(action, data) {
        var event = new CustomEvent('mozUITour', {
            bubbles: true,
            detail: {
                action: action,
                data: data || {}
            }
        });

        document.dispatchEvent(event);
    };

    if (client.isFirefoxDesktop ||client.isFirefoxAndroid) {
        // Detect whether the Firefox is up-to-date in a non-strict way. The minor version and channel are not
        // considered. This can/should be strict, once the UX especially for ESR users is decided. (Bug 939470)
        if (client._isFirefoxUpToDate(false)) {
            // the firefox-latest class prevents the download button from displaying
            $html.addClass('firefox-latest');
            // if user is on desktop release channel and has latest version, offer refresh button
            if (client.isFirefoxDesktop) {
                client.getFirefoxDetails(function(data) {
                    // data.accurate will only be true if UITour API is working.
                    if (data.channel === 'release' && data.isUpToDate && data.accurate) {
                        $html.addClass('show-refresh');
                        
                        $('#refresh-firefox').on('click', function() {
                            uiTourSendEvent('resetFirefox');
                        });
                    }
                });
            }
        } else {
            $html.addClass('firefox-old');
        }
    }

    // Add GA custom tracking and external link tracking
    state = 'Desktop, not Firefox';

    if (client.platform === 'android') {
        if ($html.hasClass('firefox-latest')) {
            state = 'Android, Firefox up-to-date';
        } else if ($html.hasClass('firefox-old')) {
            state = 'Android, Firefox not up-to-date';
        } else {
            state = 'Android, not Firefox';
        }
    } else if (client.platform === 'ios') {
        state = 'iOS';
    } else if (client.platform === 'fxos') {
        state = 'FxOS';
    } else {
        if ($html.hasClass('firefox-latest')) {
            state = 'Desktop, Firefox up-to-date';
        } else if ($html.hasClass('firefox-old')) {
            state = 'Desktop, Firefox not up-to-date';
        }
    }

    //GA Custom Dimension in Pageview
    dataLayer.push({
        'event': 'set-state',
        'state': state
    });

})(window.jQuery, window.dataLayer = window.dataLayer || []);
