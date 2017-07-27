/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

// create namespace
if (typeof window.Mozilla === 'undefined') {
    window.Mozilla = {};
}

(function(Mozilla) {
    'use strict';

    // these are essentially the same URLs from whatsnew-54.js, but with '_v2'
    // appended to the 'creative' query param
    Mozilla.WNP54.appStoreURLs = {
        'au': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_au_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fau%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'br': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_pt-br_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fbr%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'cn': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_cn_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fcn%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'de': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_de_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fde%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'es': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_es_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fes%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'fr': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_fr_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Ffr%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'gb': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_gb_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fgb%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'id': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_id_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fid%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'in': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_in_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fin%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'it': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_it_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fit%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'jp': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_jp_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fjp%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'mx': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_es-mx_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fmx%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'pl': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_pl_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fpl%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8',
        'ru': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=iOS_App_Store&creative=badge_ru_v2&fallback=https%3A%2F%2Fitunes.apple.com%2Fru%2Fapp%2Fapple-store%2Fid989804926%3Fpt%3D373246%26ct%3Dadjust_tracker%26mt%3D8'
    };

    Mozilla.WNP54.playStoreURLs = {
        'au': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_au_v2',
        'br': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_pt-br_v2',
        'cn': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_cn_v2',
        'de': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_de_v2',
        'es': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_es_v2',
        'fr': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_fr_v2',
        'gb': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_gb_v2',
        'id': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_id_v2',
        'in': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_in_v2',
        'it': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_it_v2',
        'jp': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_jp_v2',
        'mx': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_es-mx_v2',
        'pl': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_pl_v2',
        'ru': 'https://app.adjust.com/2uo1qc?campaign=whats_new&adgroup=Google_Play_Store&creative=badge_ru_v2'
    };
})(window.Mozilla);
