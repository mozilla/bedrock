/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function(Mozilla, $) {
    'use strict';

    var fxaEmail;
    var client = Mozilla.Client;
    var $main = $('main');

    // check for fxaEmail in sessionStorage or URL params
    try {
        fxaEmail = sessionStorage.getItem('fxa-email');
        sessionStorage.removeItem('fxa-email');
    } catch(ex) {
        // empty
    }

    function sendGAEvent(type) {
        var data = {
            'event': 'accounts',
            'interaction': type
        };

        window.dataLayer.push(data);
    }

    function loadFxAccountsForm() {
        Mozilla.FxaIframe.init({
            gaEventName: 'accounts',
            userEmail: fxaEmail
        });
    }

    function showFxAForm() {
        loadFxAccountsForm();

        // UITour is used only to show conditional messaging.
        Mozilla.UITour.getConfiguration('sync', function (config) {
            if (config.setup) {
                // Show signed-in messaging if user is already using Sync
                $('.signed-in').show();
            } else {
                // Show sign-up steps if user is not already using Sync
                $('.sign-up-instructions').show();
            }
        });
    }

    // Show FxA form for up to date Firefox desktop users.
    function showUpToDateFirefox() {
        $main.addClass('state-firefox-up-to-date');
        showFxAForm();
    }

    // Firefox iOS users get SUMO link
    function showFirefoxiOS() {
        $main.addClass('state-firefox-ios');
        sendGAEvent('firefox-ios');
    }

    // Firefox Android users get SUMO link
    function showFirefoxAndroid() {
        $main.addClass('state-firefox-android');
        sendGAEvent('firefox-android');
    }

    // Non-Firefox mobile users see app store badges
    function showMobileNonFirefox() {
        $main.addClass('state-mobile');
        sendGAEvent('mobile-non-firefox');
    }

    // Other Non-Firefox browsers get regular download button
    function showNonFirefox() {
        $main.addClass('state-non-firefox');
        sendGAEvent('non-firefox');
    }

    // Old Firefox browsers get regular download button
    function showOldFirefox() {
        $main.addClass('state-old-firefox');
        sendGAEvent('old-firefox');
    }

    function init() {
        if (client.isFirefoxDesktop) {
            // FxA iFrame supported on Firefox 39 and greater
            if (client.FirefoxMajorVersion >= 39) {
                showUpToDateFirefox();
            } else {
                showOldFirefox();
            }
        } else {
            if (client.isFirefoxiOS) {
                showFirefoxiOS();
            } else if (client.isFirefoxAndroid) {
                showFirefoxAndroid();
            } else if (client.isMobile) {
                showMobileNonFirefox();
            } else {
                showNonFirefox();
            }
        }
    }

    init();

    setTimeout(Mozilla.syncAnimation, 1000);

})(window.Mozilla, window.jQuery);
