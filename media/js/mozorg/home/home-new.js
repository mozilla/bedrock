/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Mozilla, dataLayer) {
    'use strict';

    var HomePage = {
        body: document.getElementById('intro-promo-content-wrapper'),
        dataLayer: dataLayer,
        state: 'Unknown',
        syncCapable: false
    };

    HomePage.setBodyClass = function(stateClass) {
        var classes = HomePage.body.className;
        classes = classes.replace('state-default', stateClass);
        HomePage.body.className = classes;
    };

    HomePage.trackPageState = function(state) {
        HomePage.dataLayer.push({
            'event': 'page-load',
            'browser': state
        });
    };

    HomePage.ctaSyncClick = function() {
        HomePage.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'Button Click',
            'eLabel': 'Sync Promo'
        });
    };

    HomePage.ctaSyncClickFxA = function(e) {
        e.preventDefault();

        HomePage.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'Button Click',
            'eLabel': 'Sync Promo'
        });

        Mozilla.UITour.showFirefoxAccounts(HomePage.params.utmParamsFxA());
    };

    HomePage.ctaPocketClick = function() {
        HomePage.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'Button Click',
            'eLabel': 'Pocket Promo'
        });
    };

    HomePage.init = function(config) {
        HomePage.client = config.client;
        HomePage.fxVersion = HomePage.client.FirefoxMajorVersion;
        HomePage.params = new window._SearchParams();

        HomePage.ctaPocket;
        HomePage.ctaSync = document.getElementById('fxa-sign-in');

        // default to standard click handler (GA only)
        // may change if on Fx desktop signed out of Sync
        HomePage.ctaSync.addEventListener('click', HomePage.ctaSyncClick, false);

        /* This shows five different content variations, depending on the browser/state
         * 1. Not Firefox (any other browser) <-- default
         * 2. Firefox 31+ (signed-in to Sync)
         * 3. Firefox 31+ (signed-out of Sync)
         * 4. Firefox for Android
         * 5. Firefox for iOS
         */

        // Variations 2-5 are Firefox
        if (HomePage.client.isFirefox) {

            // Variation #4: Firefox for Android
            if (HomePage.client.isFirefoxAndroid) {
                HomePage.setBodyClass('state-fx-mobile');
                HomePage.state = 'Firefox for Android';

            // Variation #5: Firefox for iOS
            } else if (HomePage.client.isFirefoxiOS) {
                HomePage.setBodyClass('state-fx-mobile');
                HomePage.state = 'Firefox for iOS';

            // Variations #2-3: Firefox for Desktop
            } else if (HomePage.client.isFirefoxDesktop) {

                if (HomePage.fxVersion >= 31) {

                    // Set syncCapable so we know not to send tracking info
                    // again later
                    HomePage.syncCapable = true;

                    // Query if the UITour API is working before we use the API
                    Mozilla.UITour.getConfiguration('sync', function (config) {

                        // Variation #2: Firefox 31+ signed IN to Sync (shows Pocket promo)
                        if (config.setup) {
                            HomePage.setBodyClass('state-fx-signed-in');
                            HomePage.state = 'Firefox 31 or Higher: Signed-In';

                            HomePage.ctaPocket = document.getElementById('pocket-cta');
                            HomePage.ctaPocket.addEventListener('click', HomePage.ctaPocketClick, false);

                        // Variation #3: Firefox 31+ signed OUT of Sync
                        } else {
                            HomePage.setBodyClass('state-fx-signed-out');
                            HomePage.state = 'Firefox 31 or Higher: Signed-Out';

                            // De-activate standard click handler in favor of one that loads about:accounts
                            HomePage.ctaSync.removeEventListener('click', HomePage.ctaSyncClick, false);
                            HomePage.ctaSync.addEventListener('click', HomePage.ctaSyncClickFxA, false);
                        }

                        // Note - the above results in Nightly/Beta users having no way to download
                        // the release version on the home page. Should re-assess later.

                        // Call GA tracking here to ensure it waits for the
                        // getConfiguration async call
                        HomePage.trackPageState(HomePage.state);
                    });
                }
            }
        }

        // Send page state to GA if it hasn't already been sent in the
        // getConfiguration callback
        if (HomePage.syncCapable === false) {
            HomePage.trackPageState(HomePage.state);
        }
    };

    window.Mozilla.HomePage = HomePage;
})(window.jQuery, window.Mozilla, window.dataLayer || []);
