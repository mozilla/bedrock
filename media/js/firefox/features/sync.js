/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// Create namespace
if (typeof Mozilla === 'undefined') {
    var Mozilla = {};
}

(function(dataLayer) {
    'use strict';

    var SyncPage = {
        body: document.getElementsByTagName('body')[0],
        dataLayer: dataLayer,
        state: 'Unknown',
        syncCapable: false
    };

    SyncPage.setBodyClass = function(stateClass) {
        var classes = SyncPage.body.className;
        classes = classes.replace('state-default', stateClass);
        SyncPage.body.className = classes;
    };

    SyncPage.trackPageState = function(state) {
        SyncPage.dataLayer.push({
            'event': 'page-load',
            'browser': state
        });
    };

    SyncPage.ctaSyncClick = function(e) {
        e.preventDefault();

        SyncPage.dataLayer.push({
            'event': 'sync-click',
            'browser': SyncPage.state
        });

        Mozilla.UITour.showFirefoxAccounts(SyncPage.params.utmParamsFxA());
    };

    SyncPage.init = function(config) {
        SyncPage.client = config.client;
        SyncPage.fxVersion = SyncPage.client.FirefoxMajorVersion;
        SyncPage.params = new window._SearchParams();

        SyncPage.ctaSync = document.getElementById('cta-sync');

        /* This shows five different content variations, depending on the browser/state
         * 1. Firefox 31+ (signed-in to Sync) <-- default
         * 2. Firefox 31+ (signed-out of Sync)
         * 3. Firefox 30 or older
         * 4. Firefox for Android
         * 5. Firefox for iOS
         * 6. Not Firefox (any other browser)
         */

        // Variations 1-5 are Firefox
        if (SyncPage.client.isFirefox) {

            // Variation #4: Firefox for Android
            if (SyncPage.client.isFirefoxAndroid) {
                SyncPage.setBodyClass('state-fx-android');
                SyncPage.state = 'Firefox for Android';

            // Variation #5: Firefox for iOS
            } else if (SyncPage.client.isFirefoxiOS) {
                SyncPage.setBodyClass('state-fx-ios');
                SyncPage.state = 'Firefox for iOS';

            // Variation #1-3: Firefox for Desktop
            } else if (SyncPage.client.isFirefoxDesktop) {

                if (SyncPage.fxVersion >= 31) {

                    // Set syncCapable so we know not to send tracking info
                    // again later
                    SyncPage.syncCapable = true;

                    // Query if the UITour API is working before we use the API
                    Mozilla.UITour.getConfiguration('sync', function (config) {

                        // Variation #1: Firefox 31+ signed IN to Sync (default)
                        if (config.setup) {
                            SyncPage.setBodyClass('state-fx-31-signed-in');
                            SyncPage.state = 'Firefox 31 or Higher: Signed-In';

                        // Variation #2: Firefox 31+ signed OUT of Sync
                        } else {
                            SyncPage.setBodyClass('state-fx-31-signed-out');
                            SyncPage.state = 'Firefox 31 or Higher: Signed-Out';

                            // Sync sign in flow button only visible for Fx31+ signed OUT of Sync
                            SyncPage.ctaSync.addEventListener('click', SyncPage.ctaSyncClick);
                        }

                        // Call GA tracking here to ensure it waits for the
                        // getConfiguration async call
                        SyncPage.trackPageState(SyncPage.state);
                    });

                // Variation #3: Firefox 30 or older
                } else if (SyncPage.fxVersion <= 30) {
                    SyncPage.setBodyClass('state-fx-30-older');
                    SyncPage.state = 'Firefox 30 or older';
                }
            }
        // Variation #5: Not Firefox
        } else {
            SyncPage.setBodyClass('state-not-fx');
            SyncPage.state = 'Not Firefox';
        }

        // Send page state to GA if it hasn't already been sent in the
        // getConfiguration callback
        // Called for all variations *except* Fx 31+
        if (SyncPage.syncCapable === false) {
            SyncPage.trackPageState(SyncPage.state);
        }
    };

    window.Mozilla.SyncPage = SyncPage;
})(window.dataLayer || []);
