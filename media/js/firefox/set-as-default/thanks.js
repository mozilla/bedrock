/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function() {
    'use strict';

    var timer;

    function isDefaultBrowser() {
        return new window.Promise(function(resolve, reject) {
            Mozilla.UITour.getConfiguration('appinfo', function(details) {
                if (details.defaultBrowser) {
                    resolve();
                } else {
                    reject(details.canSetDefaultBrowserInBackground);
                }
            });
        });
    }

    function trySetDefaultBrowser() {
        Mozilla.UITour.setConfiguration('defaultBrowser');
    }

    function onDefaultSwitch() {
        document.querySelector('main').classList.add('is-firefox-default');
        trackEvent('default-changed', 'success');
    }

    function checkForDefaultSwitch() {
        isDefaultBrowser().then(function() {
            onDefaultSwitch();
            clearInterval(timer);
        }).catch(function() {
            // do nothing.
        });
    }

    function trackEvent(action, label) {
        window.dataLayer.push({
            'event': 'in-page-interaction',
            'eAction': action,
            'eLabel': label
        });
    }

    function isSupported() {
        return Mozilla.Client.isFirefoxDesktop && 'Promise' in window;
    }

    function onLoad() {
        if (!isSupported()) {
            return;
        }

        /**
         * Check to see if Firefox is the default browser.
         * If true show a success message.
         * If false prompt to switch the default browser.
         */
        isDefaultBrowser().then(function() {
            document.querySelector('main').classList.add('is-firefox-default');
            trackEvent('visited', 'firefox-default');

        }).catch(function(canSetDefaultBrowserInBackground) {
            /**
             * If we can set the default in the background without any user interaction,
             * then do so straight away, else poll for when the user sets it manually.
             */
            if (canSetDefaultBrowserInBackground) {
                trySetDefaultBrowser();
                onDefaultSwitch();
            } else {
                // Give a little time before opening system dialog when the page loads.
                window.setTimeout(function() {
                    trySetDefaultBrowser();
                    timer = setInterval(checkForDefaultSwitch, 1000);
                }, 1500);
            }
            trackEvent('visited', 'firefox-not-default');
        });
    }

    Mozilla.run(onLoad);

})(window.Mozilla);
