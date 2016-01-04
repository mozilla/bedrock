/* This Source Code Form is subject to the terms of the Mozilla Public
* License, v. 2.0. If a copy of the MPL was not distributed with this
* file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

;(function($, Mozilla) {
    'use strict';

    var $html = $('html');
    var $body = $('body');

    // send-to-device form
    var $widget = $('#send-to-modal-container');
    var sendToDeviceForm = new Mozilla.SendToDevice();

    // Countries in which Firefox for iOS is available.
    // Add two-letter country codes (lowercase) to this array to
    // to expand the market. We'll remove this logic for wide release.
    // Note: This is the country code, NOT locale code; they often differ.
    var marketCountries = ['nz', 'au', 'at', 'ca'];

    var COUNTRY_CODE = '';
    var marketState = 'Unknown';

    // Sync instructions
    var $instructions = $('#sync-instructions');
    var $fill = $('<div id="modal" role="dialog" tabindex="-1"></div>');

    // initialize state - runs after geolocation has completed
    var initState = function() {
        var client = Mozilla.Client;
        var state = 'Unknown';
        var syncCapable = false;

        if (client.isFirefox) {
            // Firefox for Android
            if (client.isFirefoxAndroid) {
                swapState('state-fx-android');
                state = 'Firefox Android: ' + marketState;

            // Firefox for iOS
            } else if (client.isFirefoxiOS) {
                swapState('state-fx-ios');
                state = 'Firefox iOS: ' + marketState;

            // Firefox for Desktop
            } else {

                if (client.FirefoxMajorVersion >= 31) {

                    // Set syncCapable so we know not to send tracking info
                    // again later
                    syncCapable = true;

                    // Query if the UITour API is working before we use the API
                    Mozilla.UITour.getConfiguration('sync', function (config) {

                        // Variation #1: Firefox 31+ signed IN to Sync (default)
                        if (config.setup) {
                            swapState('state-fx-signed-in');
                            state = 'Firefox Desktop: Signed-In: ' + marketState;

                        // Variation #2: Firefox 31+ signed OUT of Sync
                        } else {
                            swapState('state-fx-signed-out');
                            state = 'Firefox Desktop: Signed-Out: ' + marketState;
                        }

                        // Call GA tracking here to ensure it waits for the
                        // getConfiguration async call
                        window.dataLayer.push({
                            event: 'ios-page-interactions',
                            interaction: 'page-load',
                            loadState: state
                        });
                    });
                }

            }

        // Not Firefox
        } else {
            swapState('state-not-fx');
            state = 'Not Firefox: ' + marketState;
        }

        // Send page state to GA if it hasn't already been sent
        if (syncCapable === false) {
            window.dataLayer.push({
                event: 'ios-page-interactions',
                interaction: 'page-load',
                loadState: state
            });
        }
    };

    var swapState = function(stateClass) {
        $body.removeClass('state-default');
        $body.addClass(stateClass);
    };

    // Get country code via geo-ip lookup
    var getGeoLocation = function() {
        // attempt to get country code
        try {
            COUNTRY_CODE = geoip_country_code().toLowerCase();
        } catch (e) {
            COUNTRY_CODE = '';
        }

        // if COUNTRY_CODE is one of the marketCountries, update page display
        if ($.inArray(COUNTRY_CODE, marketCountries) > -1) {
            $body.addClass('in-market');
            marketState = 'In Market';
        } else {
            marketState = 'Out of Market';
        }

        // initialize page state now that marketState is determined
        initState();
    };

    // load geolocation script
    $.getScript('https://geo.mozilla.org/country.js', function() {
        getGeoLocation();
    });

    // initialize send to device form
    sendToDeviceForm.init();

    // open send to device form in modal
    $('.send-to').on('click', function(e) {
        e.preventDefault();
        Mozilla.Modal.createModal(this, $widget);
    });

    // Firefox Sync sign in flow button
    $('.sync-button').on('click', function(e) {
        e.preventDefault();
        Mozilla.UITour.showFirefoxAccounts();
    });

    // Show Sync instructions in a modal doorhanger
    $('.sync-start-ios').on('click', function(e) {
        e.preventDefault();
        $html.addClass('noscroll');
        $fill.append($instructions);
        $body.append($fill);
    });

    // dismiss sync instructions
    $('#sync-instructions .btn-dismiss').on('click', function(e) {
        e.preventDefault();
        $html.removeClass('noscroll');
        $body.append($instructions);
        $fill.remove();
    });
})(jQuery, Mozilla);
