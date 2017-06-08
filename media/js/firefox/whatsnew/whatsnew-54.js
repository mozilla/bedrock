/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var appStoreURLs = {
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
    };

    var playStoreURLs = {
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
    };

    var form = new Mozilla.SendToDevice();

    form.geoCallback = function(countryCode) {
        // only take action on non-us country codes
        if (countryCode && countryCode !== 'us') {
            // make sure the user's countryCode is in our list
            if (appStoreURLs.hasOwnProperty(countryCode)) {
                $('#appStoreLink').attr('href', appStoreURLs[countryCode]);
            }

            if (playStoreURLs.hasOwnProperty(countryCode)) {
                $('#playStoreLink').attr('href', playStoreURLs[countryCode]);
            }
        }
    };

    form.init();
})(window.jQuery);
