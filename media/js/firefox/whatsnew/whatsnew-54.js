/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function($, Mozilla) {
    'use strict';

    var WNP54 = {
        appStoreURLs: {
            'au': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_au&fallback=https%3A%2F%2Fitunes.apple.com%2Fau%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'br': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_pt-br&fallback=https%3A%2F%2Fitunes.apple.com%2Fbr%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'cn': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_cn&fallback=https%3A%2F%2Fitunes.apple.com%2Fcn%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'de': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_de&fallback=https%3A%2F%2Fitunes.apple.com%2Fde%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'es': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_es&fallback=https%3A%2F%2Fitunes.apple.com%2Fes%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'fr': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_fr&fallback=https%3A%2F%2Fitunes.apple.com%2Ffr%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'gb': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_gb&fallback=https%3A%2F%2Fitunes.apple.com%2Fgb%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'id': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_id&fallback=https%3A%2F%2Fitunes.apple.com%2Fid%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'in': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_in&fallback=https%3A%2F%2Fitunes.apple.com%2Fin%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'it': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_it&fallback=https%3A%2F%2Fitunes.apple.com%2Fit%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'jp': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_jp&fallback=https%3A%2F%2Fitunes.apple.com%2Fjp%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'mx': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_es-mx&fallback=https%3A%2F%2Fitunes.apple.com%2Fmx%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'pl': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_pl&fallback=https%3A%2F%2Fitunes.apple.com%2Fpl%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
            'ru': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_ru&fallback=https%3A%2F%2Fitunes.apple.com%2Fru%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8'
        },
        playStoreURLs: {
            'au': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_au',
            'br': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_pt-br',
            'cn': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_cn',
            'de': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_de',
            'es': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_es',
            'fr': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_fr',
            'gb': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_gb',
            'id': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_id',
            'in': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_in',
            'it': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_it',
            'jp': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_jp',
            'mx': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_es-mx',
            'pl': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_pl',
            'ru': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_ru'
        },
        sendToDeviceForm: $('#send-to-device-form'),
        updateStoreLinks: function(country) {
            var newAppStoreURL = WNP54.getStoreURL(country, 'ios');
            var newPlayStoreURL = WNP54.getStoreURL(country, 'android');

            if (newAppStoreURL) {
                $('#appStoreLink').attr('href', newAppStoreURL);
            }

            if (newPlayStoreURL) {
                $('#playStoreLink').attr('href', newPlayStoreURL);
            }
        },
        getStoreURL: function(country, platform) {
            var newURL;

            // only update non-US
            if (country && country !== 'us') {
                switch(platform) {
                case 'ios':
                    if (WNP54.appStoreURLs.hasOwnProperty(country)) {
                        newURL = WNP54.appStoreURLs[country];
                    }

                    break;
                case 'android':
                    if (WNP54.playStoreURLs.hasOwnProperty(country)) {
                        newURL = WNP54.playStoreURLs[country];
                    }

                    break;
                }
            }

            return newURL;
        },
        init: function() {
            // initialize the form if it exists
            if (WNP54.sendToDeviceForm.length > 0) {
                var form = new Mozilla.SendToDevice();

                form.geoCallback = WNP54.updateStoreLinks;

                form.init();
            } else {
                // make the request
                fetch('/country-code.json', {
                    method: 'GET'
                }).then(function(response) {
                    if (response.ok) {
                        // convert response to JSON
                        return response.json();
                    } else {
                        // nothing breaks with a failure here, so just log the
                        // error
                        throw new Error('Invalid response from /country-code.json');
                    }
                }).then(function(jsonData) {
                    // send JSON data to the handler
                    WNP54.updateStoreLinks(jsonData.country_code.toLowerCase());
                });
            }
        }
    };

    Mozilla.WNP54 = WNP54;
})(window.jQuery, window.Mozilla);
