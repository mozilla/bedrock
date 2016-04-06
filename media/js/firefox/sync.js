/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($, Mozilla) {
    'use strict';

    window.dataLayer = window.dataLayer || [];

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

    var params = new window._SearchParams();
    var client = window.Mozilla.Client;
    var fxMasterVersion = client.FirefoxMajorVersion;
    var state = 'Unknown';
    var syncCapable = false;
    var body = $('body');
    var $fxaEmailForm = $('#fxa-email-form');
    var $fxaEmailElements = $('.fxa-email');
    var $fxaEmailField = $('#fxa-email');
    var fxaEmail;
    var hasSessionStorage = false;

    var swapState = function(stateClass) {
        body.removeClass('state-default');
        body.addClass(stateClass);

        if (stateClass === 'state-fx-31-signed-out') {
            initVariationsForm();
        }
    };

    // Variations 1-5 are Firefox
    if (client.isFirefox) {
        // Variation #5: Firefox for Android
        if (client.isFirefoxAndroid) {

            swapState('state-fx-android');
            state = 'Firefox for Android';

        // Variation #1-4: Firefox for Desktop
        } else if (client.isFirefoxDesktop) {

            if (fxMasterVersion >= 31) {

                // Set syncCapable so we know not to send tracking info
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
                    window.dataLayer.push({
                        'event': 'page-load',
                        'browser': state
                    });
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
        window.dataLayer.push({
            'event': 'page-load',
            'browser': state
        });
    }

    // Firefox Sync sign in flow button
    $('#cta-sync').on('click', function(e) {
        e.preventDefault();

        window.dataLayer.push({
            'event': 'sync-click',
            'browser': state
        });

        Mozilla.UITour.showFirefoxAccounts(params.utmParamsFxA());
    });

    // v2/3 variations only for Fx 31+ signed out of sync
    function initVariationsForm() {
        // only show email field if sessionStorage is available
        try {
            window.sessionStorage.setItem('moz-session-storage-check', true);
            window.sessionStorage.removeItem('moz-session-storage-check');

            $fxaEmailElements.addClass('active');
            $fxaEmailField.attr('required', 'required');

            hasSessionStorage = true;
        } catch(ex) {
            // empty block
        }

        $fxaEmailForm.on('submit', function(e) {
            e.preventDefault();

            $fxaEmailForm.off('submit');

            window.dataLayer.push({
                'event': 'sync-interactions',
                'interaction': 'form submit',
                'form-name': $.trim($('#cta-sync-variation').text()),
                'test-variation': $('#variation').val()
            });

            // store email in sessionStorage and clear the field
            if (hasSessionStorage) {
                fxaEmail = $fxaEmailField.val();

                // basic email validation
                if (/(.+)@(.+)\.(.+){2,}/.test(fxaEmail)) {
                    window.sessionStorage.setItem('fxa-email', $fxaEmailField.val());
                }

                $fxaEmailField.removeAttr('required').val('');
            }

            $fxaEmailForm.submit();
        });
    }
})(window.jQuery, window.Mozilla);
