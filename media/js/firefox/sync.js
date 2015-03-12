/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

;(function($, Mozilla) {
    'use strict';

    setTimeout(Mozilla.syncAnimation, 1000);

    /* This shows six different content variations, depending on the browser/state
     * 1. Firefox 31+ (signed-in to Sync) <-- default
     * 2. Firefox 31+ (signed-out of Sync)
     * 3. Firefox 29 or 30
     * 4. Firefox 28 or older
     * 5. Firefox for Android
     * 6. Not Firefox (any other browser)
     */

    // Variation #1: Firefox 31+ signed-in to Sync
    // Default (do nothing)

    var fxMasterVersion = window.getFirefoxMasterVersion();
    var state = 'Unknown';
    var syncCapable = false;
    var body = $('body');

    var swapState = function(stateClass) {
        body.removeClass('state-default');
        body.addClass(stateClass);
    };

    // Variations 1-5 are Firefox
    if (window.isFirefox()) {

        // Variation #5: Firefox for Android
        if (window.isFirefoxMobile()) {

            swapState('state-fx-android');
            state = 'Firefox for Android';

        // Variation #1-4: Firefox for Desktop
        } else {

            if (fxMasterVersion >= 31) {

                // Set syncCapable so we know not to call gaTrack()
                // again later
                syncCapable = true;

                // Query if the UITour API is working before we use the API
                Mozilla.UITour.getConfiguration('sync', function (config) {

                    // Variation #1: Firefox 31+ signed IN to Sync (default)
                    if (config.setup) {

                        swapState('state-fx-31-signed-in');
                        state = 'Firefox 31 or Higher: Signed-In';

                    // Variation #2: Firefox 31+ signed OUT of Sync
                    } else {
                        swapState('state-fx-31-signed-out');
                        state = 'Firefox 31 or Higher: Signed-Out';
                    }

                    // Call GA tracking here to ensure it waits for the
                    // getConfiguration async call
                    gaTrack(['_trackEvent', '/sync/ Page Interactions', 'load', state]);

                });

            // Variation #3: Firefox 29 or 30
            } else if (fxMasterVersion === 29 || fxMasterVersion === 30) {
                swapState('state-fx-29-30');
                state = 'Firefox 29 or 30';

            // Variation #4: Firefox 28 or older
            } else if (fxMasterVersion <= 28) {
                swapState('state-fx-28-older');
                state = 'Firefox 28 or Older';
            }

        }

    // Variation #6: Not Firefox
    } else {
        swapState('state-not-fx');
        state = 'Not Firefox';
    }

    // Send page state to GA if it hasn't already been sent in the
    // getConfiguration callback
    if (syncCapable === false) {
        gaTrack(['_trackEvent', '/sync/ Page Interactions', 'load', state]);
    }

    var trackClick = function (gaArgs, element, event) {
        event.preventDefault();
        gaTrack(gaArgs, function() {
            window.location = element.href;
        });
    };

    // Setup GA tracking for misc links
    $('.ga-link').on('click', function(e) {
        trackClick(['_trackEvent', '/sync/ Page Interactions', 'outbound link click', this.href], this, e);
    });

    // Setup GA tracking for Firefox download button
    $('#cta-firefox, .download-button .download-link').on('click', function(e) {
        trackClick(['_trackEvent', 'Firefox Downloads', 'download click', 'Firefox'], this, e);
    });

    // Setup GA tracking for Firefox update button
    $('#cta-update').on('click', function(e) {
        trackClick(['_trackEvent', 'Firefox Downloads', 'update click', 'Firefox'], this, e);
    });

    // Setup GA tracking for Firefox for primary Android download button
    $('#cta-android').on('click', function(e) {
        trackClick(['_trackEvent', 'Firefox Downloads', 'top', 'Firefox for Android'], this, e);
    });

    // Setup GA tracking for Firefox for Android footer download button
    $('#cta-android-footer').on('click', function(e) {
        trackClick(['_trackEvent', 'Firefox Downloads', 'bottom', 'Firefox for Android'], this, e);
    });

    // Setup GA tracking for Sync button
    $('#cta-sync').on('click', function(e) {
        e.preventDefault();
        gaTrack(['_trackEvent', '/sync/ Page Interactions', 'button click', 'Sync CTA'],
            Mozilla.UITour.showFirefoxAccounts);
    });

    Mozilla.FxFamilyNav.init({ primaryId: 'desktop', subId: 'sync' });
})(window.jQuery, window.Mozilla);
