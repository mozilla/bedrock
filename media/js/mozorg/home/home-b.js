/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Mozilla, dataLayer) {
    'use strict';

    var HomePageB = {
        body: document.getElementById('intro-promo-content-wrapper'),
        dataLayer: dataLayer,
        state: 'Unknown',
        syncCapable: false
    };

    HomePageB.setBodyClass = function(stateClass) {
        var classes = HomePageB.body.className;
        classes = classes.replace('state-default', stateClass);
        HomePageB.body.className = classes;
    };

    HomePageB.trackPageState = function(state) {
        HomePageB.dataLayer.push({
            'event': 'page-load',
            'browser': state
        });
    };

    HomePageB.ctaSyncClick = function() {
        HomePageB.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'Button Click',
            'eLabel': 'Sync Promo'
        });
    };

    HomePageB.ctaSyncClickFxA = function(e) {
        e.preventDefault();

        HomePageB.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'Button Click',
            'eLabel': 'Sync Promo'
        });

        Mozilla.UITour.showFirefoxAccounts(HomePageB.params.utmParamsFxA());
    };

    HomePageB.ctaPocketClick = function() {
        HomePageB.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': 'Button Click',
            'eLabel': 'Pocket Promo'
        });
    };

    HomePageB.init = function(config) {
        HomePageB.client = config.client;
        HomePageB.fxVersion = HomePageB.client.FirefoxMajorVersion;
        HomePageB.params = new window._SearchParams();

        HomePageB.ctaPocket;
        HomePageB.ctaSync = document.getElementById('fxa-sign-in');

        // default to standard click handler (GA only)
        // may change if on Fx desktop signed out of Sync
        HomePageB.ctaSync.addEventListener('click', HomePageB.ctaSyncClick, false);

        /* This shows five different content variations, depending on the browser/state
         * 1. Not Firefox (any other browser) <-- default
         * 2. Firefox 31+ (signed-in to Sync)
         * 3. Firefox 31+ (signed-out of Sync)
         * 4. Firefox for Android
         * 5. Firefox for iOS
         */

        // Variations 2-5 are Firefox
        if (HomePageB.client.isFirefox) {

            // Variation #4: Firefox for Android
            if (HomePageB.client.isFirefoxAndroid) {
                HomePageB.setBodyClass('state-fx-mobile');
                HomePageB.state = 'Firefox for Android';

            // Variation #5: Firefox for iOS
            } else if (HomePageB.client.isFirefoxiOS) {
                HomePageB.setBodyClass('state-fx-mobile');
                HomePageB.state = 'Firefox for iOS';

            // Variations #2-3: Firefox for Desktop
            } else if (HomePageB.client.isFirefoxDesktop) {

                if (HomePageB.fxVersion >= 31) {

                    // Set syncCapable so we know not to send tracking info
                    // again later
                    HomePageB.syncCapable = true;

                    // Query if the UITour API is working before we use the API
                    Mozilla.UITour.getConfiguration('sync', function (config) {

                        // Variation #2: Firefox 31+ signed IN to Sync (shows Pocket promo)
                        if (config.setup) {
                            HomePageB.setBodyClass('state-fx-signed-in');
                            HomePageB.state = 'Firefox 31 or Higher: Signed-In';

                            HomePageB.ctaPocket = document.getElementById('pocket-cta');
                            HomePageB.ctaPocket.addEventListener('click', HomePageB.ctaPocketClick, false);

                        // Variation #3: Firefox 31+ signed OUT of Sync
                        } else {
                            HomePageB.setBodyClass('state-fx-signed-out');
                            HomePageB.state = 'Firefox 31 or Higher: Signed-Out';

                            // De-activate standard click handler in favor of one that loads about:accounts
                            HomePageB.ctaSync.removeEventListener('click', HomePageB.ctaSyncClick, false);
                            HomePageB.ctaSync.addEventListener('click', HomePageB.ctaSyncClickFxA, false);
                        }

                        // Note - the above results in Nightly/Beta users having no way to download
                        // the release version on the home page. Should re-assess later.

                        // Call GA tracking here to ensure it waits for the
                        // getConfiguration async call
                        HomePageB.trackPageState(HomePageB.state);
                    });
                }
            }
        }

        // Send page state to GA if it hasn't already been sent in the
        // getConfiguration callback
        if (HomePageB.syncCapable === false) {
            HomePageB.trackPageState(HomePageB.state);
        }
    };

    window.Mozilla.HomePageB = HomePageB;
})(window.jQuery, window.Mozilla, window.dataLayer || []);
